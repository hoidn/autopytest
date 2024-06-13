from configuration import Configuration
from serializer import Serializer
from logger import Logger
from functionmapping import FunctionMapping

import os
import time
from typing import Callable, Any

def make_invocation_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

class Debug:
    def __init__(self, configuration: Configuration, serializer: Serializer, logger: Logger, function_mapping: FunctionMapping):
        self.configuration = configuration
        self.serializer = serializer
        self.logger = logger
        self.function_mapping = function_mapping

    def decorate(self, func: Callable) -> Callable:
        increment_count = make_invocation_counter()
        if not self.configuration.getDebugFlag():
            return func

        else:
            module_path = self.function_mapping.get_module_path(func)
            function_name = func.__name__
            print(f"Decorating function: {module_path}.{function_name}")

            def wrapper(*args: Any, **kwargs: Any) -> Any:
                invocation_count = increment_count()
                if  invocation_count > 2:
                    return func(*args, **kwargs)
                
                log_file_path = self.function_mapping.get_log_file_path(func)
                print(f"Log file path: {log_file_path}")
                
                log_directory = os.path.dirname(log_file_path)
                print(f"Log directory: {log_directory}")
                os.makedirs(log_directory, exist_ok=True)

                serialized_args = self.serializer.serialize(args)
                serialized_kwargs = self.serializer.serialize(kwargs)
                self.logger.logCall(serialized_args, serialized_kwargs, log_file_path)

                console_log_start = f"<{module_path}.{function_name}>CALL"
                console_log_args = self._formatConsoleLog(args)
                console_log_kwargs = self._formatConsoleLog(kwargs)
                print(console_log_start)
                print(console_log_args)
                print(console_log_kwargs)

                start_time = time.time()

                try:
                    result = func(*args, **kwargs)
                    serialized_result = self.serializer.serialize(result)
                    self.logger.logReturn(serialized_result, time.time() - start_time, log_file_path)

                    console_log_end = f"</{module_path}.{function_name}>RETURN"
                    console_log_result = self._formatConsoleLog(result)
                    print(console_log_end + " " + console_log_result)

                    return result
                except Exception as e:
                    self.logger.logError(str(e), log_file_path)
                    print(f"<{module_path}.{function_name}>ERROR {str(e)}")
                    raise e

            return wrapper

    def _formatConsoleLog(self, data: Any) -> str:
        if not isinstance(data, tuple):
            data = (data,)

        formatted_data = []
        for item in data:
            if hasattr(item, 'shape') and hasattr(item, 'dtype'):
                formatted_data.append(f"shape={item.shape}, dtype={item.dtype}")
            else:
                formatted_data.append(str(item))
        return ", ".join(formatted_data)
#    def _formatConsoleLog(self, *data: Any) -> str:
#        formatted_data = []
#        for item in data:
#            if hasattr(item, 'shape') and hasattr(item, 'dtype'):
#                formatted_data.append(f"shape={item.shape}, dtype={item.dtype}")
#            else:
#                formatted_data.append(str(item))
#        return ", ".join(formatted_data)

obj = Debug(Configuration(), Serializer(), Logger(), FunctionMapping())
debug = obj.decorate

#@debug
#def hello(x):
#    return 2 * x
