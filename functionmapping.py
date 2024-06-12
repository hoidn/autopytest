from typing import Callable, Optional
import importlib.util
import sys

class FunctionMapping:
    def __init__(self, log_directory: str = "logs"):
        self.log_directory = log_directory

    def get_log_file_path(self, func: Callable) -> str:
        """
        Retrieves the log file path for a given function.
        
        Preconditions:
        - `func` must be a callable.
        
        Postconditions:
        - Returns the log file path for the given function, formatted as `prefix/module.fname<suffix>.log`.

        >>> function_mapping = FunctionMapping(log_directory="test_logs")
        >>> def sample_function():
        ...     return "sample function executed"
        >>> function_mapping.get_log_file_path(sample_function)
        'test_logs/__main__.sample_function.log'
        """
        module_name = func.__module__
        func_name = func.__name__
        log_file_path = f"{self.log_directory}/{module_name}.{func_name}.log"
        return log_file_path

    def load_function(self, log_file_path: str = "", module_path: str = "") -> Optional[Callable]:
        """
        Loads a function given its log file path or module path.
        
        Preconditions:
        - `log_file_path` or `module_path` must be valid.
        
        Postconditions:
        - Returns the function object if successfully loaded.
        - If the function cannot be found or imported, returns None.

        >>> function_mapping = FunctionMapping(log_directory="test_logs")
        >>> def sample_function():
        ...     return "sample function executed"
        >>> log_file_path = function_mapping.get_log_file_path(sample_function)
        >>> module_path = function_mapping.get_module_path(sample_function)
        >>> loaded_func = function_mapping.load_function(log_file_path, module_path)
        """
        try:
            if log_file_path:
                parts = log_file_path.replace('.log', '').split('/')
                module_name, func_name = parts[-1].split('.')
            elif module_path:
                parts = module_path.split('.')
                module_name, func_name = parts[0], parts[1]
            else:
                return None
            
            if module_name == "__main__":
                return globals().get(func_name)
            else:
                spec = importlib.util.find_spec(module_name)
                if spec is None:
                    return None
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                return getattr(module, func_name, None)
        
        except Exception as e:
            print(f"Error loading function: {e}")
            return None

    def get_module_path(self, func: Callable) -> str:
        """
        Retrieves the module path for a given function.
        
        Preconditions:
        - `func` must be a callable.
        
        Postconditions:
        - Returns the module path for the given function, formatted as `module.fname`.

        >>> function_mapping = FunctionMapping(log_directory="test_logs")
        >>> def sample_function():
        ...     return "sample function executed"
        >>> function_mapping.get_module_path(sample_function)
        '__main__.sample_function'
        """
        module_name = func.__module__
        func_name = func.__name__
        module_path = f"{module_name}.{func_name}"
        return module_path


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

def sample_function():
    return "sample function executed"

def another_function():
    return "another function executed"

def test_get_log_file_path():
    function_mapping = FunctionMapping(log_directory="test_logs")
    path = function_mapping.get_log_file_path(sample_function)
    assert path == 'test_logs/__main__.sample_function.log', f"Expected 'test_logs/__main__.sample_function.log', got '{path}'"

def test_load_function():
    function_mapping = FunctionMapping(log_directory="test_logs")
    log_file_path = function_mapping.get_log_file_path(sample_function)
    
    loaded_func = function_mapping.load_function(log_file_path=log_file_path)
    assert loaded_func is not None, "Expected function to be loaded, but got None"
    assert loaded_func.__name__ == 'sample_function', f"Expected 'sample_function', got '{loaded_func.__name__}'"

def test_get_module_path():
    function_mapping = FunctionMapping(log_directory="test_logs")
    path = function_mapping.get_module_path(sample_function)
    assert path == '__main__.sample_function', f"Expected '__main__.sample_function', got '{path}'"

if __name__ == "__main__":
    test_get_log_file_path()
    test_load_function()
    test_get_module_path()
    print("All tests passed!")
