import os
import pickle
from datetime import datetime
from typing import Any, List, Tuple

class Logger:
    def logCall(self, args: bytes, kwargs: bytes, log_file_path: str) -> None:
        """
        Logs function call details to a specified log file.
        
        Args:
            args (bytes): Serialized function arguments.
            kwargs (bytes): Serialized function keyword arguments.
            log_file_path (str): Path to the log file.
        
        >>> logger = Logger()
        >>> log_call_path = "logCallTest.log"
        >>> logger.logCall(pickle.dumps(("arg1", "arg2")), pickle.dumps({"kw1": 1, "kw2": 2}), log_call_path)
        >>> os.path.exists(log_call_path)
        True
        """
        try:
            with open(log_file_path, 'ab') as log_file:
                log_file.write(f"CALL @ {datetime.now()}\n".encode())
                log_file.write(b"ARGS_START\n" + args + b"\nARGS_END\n")
                log_file.write(b"KWARGS_START\n" + kwargs + b"\nKWARGS_END\n")
        except Exception as e:
            print(f"Error logging call: {e}")
    
    def logReturn(self, result: bytes, executionTime: float, log_file_path: str) -> None:
        """
        Logs function return details to the specified log file.
        
        Args:
            result (bytes): Serialized function result.
            executionTime (float): Time taken for the function execution.
            log_file_path (str): Path to the log file.
        
        >>> logger = Logger()
        >>> log_return_path = "logReturnTest.log"
        >>> logger.logReturn(pickle.dumps("result data"), 1.23, log_return_path)
        >>> os.path.exists(log_return_path)
        True
        """
        try:
            with open(log_file_path, 'ab') as log_file:
                log_file.write(f"RETURN @ {datetime.now()}\n".encode())
                log_file.write(b"RESULT_START\n" + result + b"\nRESULT_END\n")
                log_file.write(f"TIME: {executionTime}s\n".encode())
        except Exception as e:
            print(f"Error logging return: {e}")
    
    def logError(self, error: str, log_file_path: str) -> None:
        """
        Logs an error message to the specified log file.
        
        Args:
            error (str): Error message.
            log_file_path (str): Path to the log file.
        
        >>> logger = Logger()
        >>> log_error_path = "logErrorTest.log"
        >>> logger.logError("An error occurred", log_error_path)
        >>> os.path.exists(log_error_path)
        True
        """
        try:
            with open(log_file_path, 'ab') as log_file:
                log_file.write(f"ERROR @ {datetime.now()}\n".encode())
                log_file.write(f"ERROR: {error}\n".encode())
        except Exception as e:
            print(f"Error logging error: {e}")

    def loadLog(self, log_file_path: str) -> Tuple[List[Any], Any]:
        """
        Loads a logged dataset from a log file.
        
        Args:
            log_file_path (str): Path to the log file.
        
        Returns:
            Tuple[List[Any], Any]: A tuple containing the logged inputs and output.
        
        >>> logger = Logger()
        >>> log_call_path = "logCallTest.log"
        >>> logger.logCall(pickle.dumps(("arg1", "arg2")), pickle.dumps({"kw1": 1, "kw2": 2}), log_call_path)
        >>> log_data = logger.loadLog(log_call_path)
        >>> log_data[0] == [('arg1', 'arg2'), {'kw1': 1, 'kw2': 2}]
        True
        """
        try:
            with open(log_file_path, 'rb') as log_file:
                lines = log_file.readlines()
                inputs = []
                output = None
                buffer = []
                reading_args = False
                reading_kwargs = False
                reading_result = False
                args_data = None
                kwargs_data = None
                for line in lines:
                    if line.startswith(b"ARGS_START"):
                        reading_args = True
                        buffer = []
                        continue
                    elif line.startswith(b"ARGS_END"):
                        reading_args = False
                        args_data = pickle.loads(b''.join(buffer))
                        continue
                    elif line.startswith(b"KWARGS_START"):
                        reading_kwargs = True
                        buffer = []
                        continue
                    elif line.startswith(b"KWARGS_END"):
                        reading_kwargs = False
                        kwargs_data = pickle.loads(b''.join(buffer))
                        continue
                    elif line.startswith(b"RESULT_START"):
                        reading_result = True
                        buffer = []
                        continue
                    elif line.startswith(b"RESULT_END"):
                        reading_result = False
                        output = pickle.loads(b''.join(buffer))
                        continue
                    
                    if reading_args or reading_kwargs or reading_result:
                        buffer.append(line.strip())
                
                if args_data and kwargs_data:
                    inputs = [args_data, kwargs_data]
                
                return inputs, output
        except Exception as e:
            print(f"Error loading log: {e}")
            return [], None

    def searchLogDirectory(self, log_directory: str) -> List[str]:
        """
        Searches the log directory and returns all well-formed log file paths.
        
        Args:
            log_directory (str): Path to the directory containing log files.
        
        Returns:
            List[str]: A list of well-formed log file paths.
        
        >>> logger = Logger()
        >>> log_files = logger.searchLogDirectory(".")
        >>> all(log_file.endswith(".log") for log_file in log_files)
        True
        """
        log_files = []
        try:
            for filename in os.listdir(log_directory):
                if filename.endswith(".log"):
                    log_files.append(os.path.join(log_directory, filename))
        except Exception as e:
            print(f"Error searching log directory: {e}")
        return log_files

import doctest
doctest.testmod(verbose=True)
