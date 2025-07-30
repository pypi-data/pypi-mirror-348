import time
import contextvars
import types
import inspect
import sys
import threading
import fnmatch
from typing import Any, Callable, Optional, Sequence, Union, Dict, List, Set
from pyeztrace.setup import Setup
from pyeztrace.custom_logging import Logging

# Marker attribute for wrapped functions
_TRACED_ATTRIBUTE = '_pyeztrace_wrapped'

# ContextVar to track functions currently being traced in the execution path
_currently_tracing = contextvars.ContextVar('_pyeztrace_currently_tracing', default=set())

def ensure_initialized():
    """Ensure EzTrace is initialized with sensible defaults if not already done."""
    try:
        if not Setup.is_setup_done():
            try:
                # Try to get main script name
                project_name = sys.argv[0].split('/')[-1].replace('.py', '') if sys.argv else None
                
                # If running in interactive mode or argv[0] is empty, try module name
                if not project_name or project_name == '' or project_name == '-c':
                    # Try to get calling module name
                    frame = inspect.currentframe()
                    if frame:
                        try:
                            frame = frame.f_back
                            if frame and frame.f_globals:
                                module_name = frame.f_globals.get('__name__')
                                if module_name and module_name != '__main__':
                                    project_name = module_name.split('.')[0]
                        finally:
                            del frame
                
                # Fallback 
                if not project_name or project_name == '':
                    project_name = "EzTrace"
                    
                Setup.initialize(project_name)
                Setup.set_setup_done()
            except Exception as e:
                # Last resort fallback
                Setup.initialize("EzTrace")
                Setup.set_setup_done()
                print(f"Warning: Error during tracer initialization: {str(e)}")
    except Exception as e:
        # Catastrophic failure - print and continue
        print(f"Critical error in EzTrace initialization: {str(e)}")
    return Logging()

logging = ensure_initialized()

def _safe_to_wrap(obj):
    """
    Check if an object is safe to wrap with our tracer.
    Returns False if:
    1. It's not a callable function/method
    2. It's already wrapped by our tracer
    """
    # Check if already wrapped
    if hasattr(obj, _TRACED_ATTRIBUTE):
        return False
    
    # Early return for None value
    if obj is None:
        return False
        
    # Only wrap python-level functions / coroutines / builtins / methods, skip everything else
    return (
        inspect.isfunction(obj)
        or inspect.iscoroutinefunction(obj)
        or inspect.ismethod(obj)  # Added support for methods
        or (inspect.isbuiltin(obj) and getattr(obj, "__module__", "") and getattr(obj, "__module__", "").startswith("builtins"))
    )

# ContextVar to indicate tracing is active
tracing_active = contextvars.ContextVar("tracing_active", default=False)

class trace_children_in_module:
    """
    Context manager to monkey-patch all functions in a module (or class) with a child-tracing decorator.
    Robust for concurrent tracing: uses per-thread and per-coroutine reference counting and locking.
    Only active when tracing_active is True.
    """
    _thread_local = threading.local()
    _coroutine_local = contextvars.ContextVar("trace_patch_ref", default=None)

    def __init__(self, module_or_class: Any, child_decorator: Callable[[Callable[..., Any]], Callable[..., Any]]) -> None:
        self.module_or_class = module_or_class
        self.child_decorator = child_decorator
        self.originals: Dict[str, Callable[..., Any]] = {}
        self._is_thread = threading.current_thread() is not None

    def _get_ref_counter(self) -> dict:
        # Prefer coroutine-local if inside a coroutine, else thread-local
        try:
            # If running in an event loop, use contextvar
            import asyncio
            if asyncio.get_event_loop().is_running():
                ref = trace_children_in_module._coroutine_local.get()
                if ref is None:
                    ref = {}
                    trace_children_in_module._coroutine_local.set(ref)
                return ref
        except Exception:
            pass
        # Fallback to thread-local
        if not hasattr(trace_children_in_module._thread_local, "ref"):
            trace_children_in_module._thread_local.ref = {}
        return trace_children_in_module._thread_local.ref

    def __enter__(self) -> None:
        ref_counter = self._get_ref_counter()
        key = id(self.module_or_class)
        if key not in ref_counter:
            # First entry for this context: patch
            ref_counter[key] = 1
            
            # Different handling for modules vs classes
            if isinstance(self.module_or_class, types.ModuleType):
                # For modules, use __dict__ directly
                items = self.module_or_class.__dict__.items()
            else:
                # For classes, we need to get all attributes including methods
                items = []
                # Add regular attributes
                for name, obj in self.module_or_class.__dict__.items():
                    items.append((name, obj))
                
                # Get all special methods we want to trace
                special_methods = ["__call__", "__init__", "__str__", "__repr__", 
                                  "__eq__", "__lt__", "__gt__", "__le__", "__ge__"]
                
                # Add any missing special methods
                for name in special_methods:
                    if hasattr(self.module_or_class, name) and name not in self.module_or_class.__dict__:
                        items.append((name, getattr(self.module_or_class, name)))
            
            # Now patch all applicable items
            for name, obj in items:
                if not _safe_to_wrap(obj):
                    continue
                
                if callable(obj):
                    # For regular methods, just patch
                    if not name.startswith("__") or name in ["__call__", "__init__", "__str__", "__eq__", "__lt__", "__gt__"]:
                        self.originals[name] = obj
                        setattr(self.module_or_class, name, self.child_decorator(obj))
        else:
            # Nested/concurrent: just increment
            ref_counter[key] += 1

    async def __aenter__(self) -> 'trace_children_in_module':
        self.__enter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__exit__(None, None, None)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        ref_counter = self._get_ref_counter()
        key = id(self.module_or_class)
        if key in ref_counter:
            ref_counter[key] -= 1
            if ref_counter[key] == 0:
                # Last exit for this context: restore
                for name, obj in self.originals.items():
                    setattr(self.module_or_class, name, obj)
                del ref_counter[key]

def child_trace_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator for child functions: only logs if tracing_active is True.
    """
    import functools
    
    # Skip decoration entirely if we know we're not in a tracing context
    # This avoids the additional function call overhead
    if not tracing_active.get():
        return func
        
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not tracing_active.get():
                return await func(*args, **kwargs)
                
            # Get the function ID
            func_id = id(func)
            
            # Get the current set of functions being traced in this execution path
            currently_tracing = _currently_tracing.get()
            
            # Check if already tracing this function in this execution path
            if func_id in currently_tracing:
                # Already being traced - avoid double tracing
                return await func(*args, **kwargs)
                
            # Add to currently tracing set
            new_tracing = currently_tracing.copy()
            new_tracing.add(func_id)
            token = _currently_tracing.set(new_tracing)
            
            # Normal tracing logic
            Setup.increment_level()
            logging.log_info(f"called...", fn_type="child", function=func.__qualname__)
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                end = time.time()
                duration = end - start
                logging.log_info(f"Ok.", fn_type="child", function=func.__qualname__, duration=duration)
                logging.record_metric(func.__qualname__, duration)
                return result
            except Exception as e:
                logging.log_error(f"Error: {str(e)}", fn_type="child", function=func.__qualname__)
                logging.raise_exception_to_log(e, str(e), stack=False)
                raise
            finally:
                Setup.decrement_level()
                _currently_tracing.reset(token)
        
        # Mark as wrapped
        setattr(wrapper, _TRACED_ATTRIBUTE, True)
        return wrapper
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not tracing_active.get():
                return func(*args, **kwargs)
                
            # Get the function ID
            func_id = id(func)
            
            # Get the current set of functions being traced in this execution path
            currently_tracing = _currently_tracing.get()
            
            # Check if already tracing this function in this execution path
            if func_id in currently_tracing:
                # Already being traced - avoid double tracing
                return func(*args, **kwargs)
                
            # Add to currently tracing set
            new_tracing = currently_tracing.copy()
            new_tracing.add(func_id)
            token = _currently_tracing.set(new_tracing)
            
            # Normal tracing logic
            Setup.increment_level()
            logging.log_info(f"called...", fn_type="child", function=func.__qualname__)
            start = time.time()
            try:
                result = func(*args, **kwargs)
                end = time.time()
                duration = end - start
                logging.log_info(f"Ok.", fn_type="child", function=func.__qualname__, duration=duration)
                logging.record_metric(func.__qualname__, duration)
                return result
            except Exception as e:
                logging.log_error(f"Error: {str(e)}", fn_type="child", function=func.__qualname__)
                logging.raise_exception_to_log(e, str(e), stack=False)
                raise
            finally:
                Setup.decrement_level()
                _currently_tracing.reset(token)
        
        # Mark as wrapped
        setattr(wrapper, _TRACED_ATTRIBUTE, True)
        return wrapper

def trace(
    message: Optional[str] = None,
    stack: bool = False,
    modules_or_classes: Optional[Union[Any, Sequence[Any]]] = None,
    include: Optional[Sequence[str]] = None,
    exclude: Optional[Sequence[str]] = None,
    recursive_depth: int = 0,  # 0 = only direct module, 1+ = levels of imports to trace
    module_pattern: Optional[str] = None  # e.g., "myapp.*" to limit recursion scope
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator for parent function. Enables tracing for all child functions in the given modules or classes.
    
    If modules_or_classes is None, it will automatically patch the module where the parent function is defined.
    Accepts a single module/class or a list of modules/classes for cross-module tracing.
    Handles both sync and async parent functions.
    Supports selective tracing via include/exclude patterns (function names).
    
    Parameters:
        message: Optional message to include in error logs
        stack: Whether to show stack trace for errors
        modules_or_classes: Modules or classes to trace
        include: Function names to include (glob patterns)
        exclude: Function names to exclude (glob patterns)
        recursive_depth: How many levels of imports to trace (0 = only direct module)
        module_pattern: Pattern to match module names for recursive tracing (e.g., "myapp.*")
    """
    def _should_trace(func_name: str) -> bool:
        if include:
            if not any(fnmatch.fnmatch(func_name, pat) for pat in include):
                return False
        if exclude:
            if any(fnmatch.fnmatch(func_name, pat) for pat in exclude):
                return False
        return True

    def make_child_decorator(orig_decorator):
        def selective_decorator(func):
            if _safe_to_wrap(func) and hasattr(func, "__name__") and _should_trace(func.__name__):
                return orig_decorator(func)
            return func
        return selective_decorator
        
    def _get_recursive_modules(module, depth, pattern=None, visited=None):
        """Recursively collect modules based on depth and pattern."""
        if visited is None:
            visited = set()
            
        if depth <= 0 or id(module) in visited:
            return []
            
        # Track visited modules to prevent circular references
        visited.add(id(module))
            
        imported_modules = []
        try:
            # Look for imported modules
            for name, obj in module.__dict__.items():
                # Only process modules
                if not isinstance(obj, types.ModuleType):
                    continue
                    
                # Skip standard library and critical system modules
                if obj.__name__.startswith(('_', 'builtins', 'sys', 'os', 'logging', 'asyncio', 'threading')):
                    continue
                    
                # Skip the tracer module itself to prevent circular tracing
                if obj.__name__ == 'pyeztrace.tracer':
                    continue
                    
                # Apply pattern filter if provided
                if pattern and not fnmatch.fnmatch(obj.__name__, pattern):
                    continue
                    
                # Skip if already visited
                if id(obj) in visited:
                    continue
                    
                imported_modules.append(obj)
                
                # Recurse with reduced depth
                if depth > 1:
                    sub_modules = _get_recursive_modules(obj, depth-1, pattern, visited)
                    imported_modules.extend(sub_modules)
        except (AttributeError, ImportError) as e:
            # Skip modules we can't process
            logging.log_debug(f"Error processing module {getattr(module, '__name__', 'unknown')}: {str(e)}")
            
        return imported_modules

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def _get_targets() -> List[Any]:
            """Get modules to trace based on parameters and recursive settings."""
            # Start with directly specified modules
            targets = []
            base_modules = []
            
            # Handle directly specified modules
            if modules_or_classes is None:
                # Default to the module containing the decorated function
                mod = sys.modules.get(func.__module__)
                if mod is not None:
                    base_modules.append(mod)
            elif isinstance(modules_or_classes, (list, tuple, set)):
                base_modules.extend(modules_or_classes)
            else:
                base_modules.append(modules_or_classes)
                
            # Always include directly specified modules
            targets.extend(base_modules)
            
            # If recursive_depth > 0, add imports from the base modules
            if recursive_depth > 0:
                visited = set()  # Track modules we've seen to avoid duplicates
                for base_module in base_modules:
                    if isinstance(base_module, types.ModuleType):
                        recursive_mods = _get_recursive_modules(
                            base_module, 
                            recursive_depth, 
                            module_pattern,
                            visited
                        )
                        # Add unique modules
                        for mod in recursive_mods:
                            if id(mod) not in [id(t) for t in targets]:
                                targets.append(mod)
                
                # Log the modules being traced if in debug mode
                if hasattr(logging, 'log_debug'):
                    mod_names = [getattr(m, '__name__', str(m)) for m in targets]
                    logging.log_debug(
                        f"Recursive tracing activated with depth={recursive_depth}. "
                        f"Tracing {len(targets)} modules: {', '.join(mod_names[:5])}" + 
                        (f"... and {len(mod_names)-5} more" if len(mod_names) > 5 else "")
                    )
                    
            return targets

        # Special case: decorator applied to a class
        if inspect.isclass(func):
            # For classes, we need to wrap all methods
            class_name = func.__name__
            
            # Copy the class dictionary to avoid modifying during iteration
            attrs = dict(func.__dict__)
            
            # Wrap each method with trace
            for name, attr in attrs.items():
                if callable(attr) and not hasattr(attr, _TRACED_ATTRIBUTE):
                    # Skip special methods that shouldn't be traced
                    if name.startswith('__') and name not in ['__init__', '__call__']:
                        continue
                    
                    # When a method is called, we need to make sure the method name includes the class name
                    method_trace = trace(
                        message=message,
                        stack=stack,
                        include=include,
                        exclude=exclude
                    )
                    
                    # Apply trace to the method and update it in the class
                    wrapped_method = method_trace(attr)
                    setattr(func, name, wrapped_method)
            
            # Mark the class as traced
            setattr(func, _TRACED_ATTRIBUTE, True)
            
            return func

        import functools
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    # Initialize if not already done
                    ensure_initialized()
                    token = tracing_active.set(True)
                    Setup.increment_level()
                    
                    # Get the function ID
                    func_id = id(func)
                    
                    # Get the current set of functions being traced
                    currently_tracing = _currently_tracing.get()
                    
                    # Add to currently tracing set
                    new_tracing = currently_tracing.copy()
                    new_tracing.add(func_id)
                    tracing_token = _currently_tracing.set(new_tracing)
                    
                    logging.log_info(f"called...", fn_type="parent", function=func.__qualname__)
                    start = time.time()
                    
                    targets = _get_targets()
                    managers = []
                    try:
                        if targets:
                            managers = [trace_children_in_module(t, make_child_decorator(child_trace_decorator)) for t in targets]
                            for m in managers:
                                await m.__aenter__()
                        result = await func(*args, **kwargs)
                        end = time.time()
                        duration = end - start
                        logging.log_info(f"Ok.", fn_type="parent", function=func.__qualname__, duration=duration)
                        logging.record_metric(func.__qualname__, duration)
                        return result
                    except Exception as e:
                        logging.log_error(f"Error: {str(e)}", fn_type="parent", function=func.__qualname__)
                        error_message = f"{message} -> {str(e)}" if message else str(e)
                        logging.raise_exception_to_log(e, error_message, stack)
                        raise
                    finally:
                        # Clean up context managers even if an exception occurs
                        for m in reversed(managers):
                            try:
                                await m.__aexit__(None, None, None)
                            except Exception:
                                pass  # Prevent cleanup exceptions from masking the original error
                except Exception as e:
                    # Fallback for catastrophic failures in the tracing setup
                    print(f"TRACE ERROR: {func.__qualname__} - {str(e)}")
                    import traceback
                    traceback.print_exc()
                    return await func(*args, **kwargs)
                finally:
                    try:
                        Setup.decrement_level()
                        tracing_active.reset(token)
                        if 'tracing_token' in locals():
                            _currently_tracing.reset(tracing_token)
                    except Exception:
                        pass  # Last-resort exception handling
            
            # Mark as wrapped            
            setattr(async_wrapper, _TRACED_ATTRIBUTE, True)
            return async_wrapper
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    # Initialize if not already done
                    ensure_initialized()
                    token = tracing_active.set(True)
                    Setup.increment_level()
                    
                    # Get the function ID
                    func_id = id(func)
                    
                    # Get the current set of functions being traced
                    currently_tracing = _currently_tracing.get()
                    
                    # Add to currently tracing set
                    new_tracing = currently_tracing.copy()
                    new_tracing.add(func_id)
                    tracing_token = _currently_tracing.set(new_tracing)
                    
                    logging.log_info(f"called...", fn_type="parent", function=func.__qualname__)
                    start = time.time()
                    
                    targets = _get_targets()
                    managers = []
                    try:
                        if targets:
                            managers = [trace_children_in_module(t, make_child_decorator(child_trace_decorator)) for t in targets]
                            for m in managers:
                                m.__enter__()
                        result = func(*args, **kwargs)
                        end = time.time()
                        duration = end - start
                        logging.log_info(f"Ok.", fn_type="parent", function=func.__qualname__, duration=duration)
                        logging.record_metric(func.__qualname__, duration)
                        return result
                    except Exception as e:
                        logging.log_error(f"Error: {str(e)}", function=func.__qualname__)
                        error_message = f"{message} -> {str(e)}" if message else str(e)
                        logging.raise_exception_to_log(e, error_message, stack)
                        raise
                    finally:
                        # Clean up context managers even if an exception occurs
                        for m in reversed(managers):
                            try:
                                m.__exit__(None, None, None)
                            except Exception:
                                pass  # Prevent cleanup exceptions from masking the original error
                except Exception as e:
                    # Fallback for catastrophic failures in the tracing setup
                    print(f"TRACE ERROR: {func.__qualname__} - {str(e)}")
                    import traceback
                    traceback.print_exc()
                    return func(*args, **kwargs)
                finally:
                    try:
                        Setup.decrement_level()
                        tracing_active.reset(token)
                        if 'tracing_token' in locals():
                            _currently_tracing.reset(tracing_token)
                    except Exception:
                        pass  # Last-resort exception handling
            
            # Mark as wrapped
            setattr(wrapper, _TRACED_ATTRIBUTE, True)
            return wrapper
    return decorator