import doctest
import os
from typing import Any, List
import numpy as np
from serializer import Serializer

class Logger:
    def logCall(self, args: Any, kwargs: Any, log_file_path: str) -> None:
        """
        Logs function call details to a specified log file.

        Preconditions:
        - `log_file_path` must be a valid file path with write permissions.

        Postconditions:
        - `args` and `kwargs` are serialized using Serializer.
        - Writes the serialized function arguments and keyword arguments to the log file.
        - If there is an error during logging, prints an error message.

        >>> l = Logger()
        >>> import tempfile
        >>> temp_dir = tempfile.TemporaryDirectory()
        >>> log_file_path = os.path.join(temp_dir.name, 'test.log')
        >>> args = (1, 2, 3)
        >>> kwargs = {'a': 4, 'b': 5}
        >>> l.logCall(args, kwargs, log_file_path)
        >>> with open(log_file_path, 'rb') as log_file:
        ...     logged_data = log_file.read()
        >>> s = Serializer()
        >>> deserialized_data = s.deserialize(logged_data.strip())
        >>> deserialized_data == {'args': args, 'kwargs': kwargs}
        True

        """
        serializer = Serializer()
        try:
            with open(log_file_path, 'ab') as log_file:
                log_file.write(serializer.serialize({'args': args, 'kwargs': kwargs}) + b'\n')
        except Exception as e:
            print(f"Error logging call: {e}")

    def logReturn(self, result: Any, executionTime: float, log_file_path: str) -> None:
        """
        Logs function return details to the specified log file.

        Preconditions:
        - `result` is serialized using pickle.
        - `log_file_path` must be a valid file path with write permissions.

        Postconditions:
        - Appends the serialized result and execution time to the log file.
        - If there is an error during logging, prints an error message.

        >>> l = Logger()
        >>> import tempfile
        >>> temp_dir = tempfile.TemporaryDirectory()
        >>> log_file_path = os.path.join(temp_dir.name, 'test.log')
        >>> result = 42
        >>> execution_time = 0.123
        >>> l.logReturn(result, execution_time, log_file_path)
        >>> with open(log_file_path, 'rb') as log_file:
        ...     logged_data = log_file.read()
        >>> s = Serializer()
        >>> deserialized_data = s.deserialize(logged_data.strip())
        >>> deserialized_data == {'result': result, 'executionTime': execution_time}
        True

        """
        serializer = Serializer()
        try:
            with open(log_file_path, 'ab') as log_file:
                log_file.write(serializer.serialize({'result': result, 'executionTime': executionTime}) + b'\n')
        except Exception as e:
            print(f"Error logging return: {e}")

    def logError(self, error: str, log_file_path: str) -> None:
        """
        Logs an error message to the specified log file.

        Preconditions:
        - `log_file_path` must be a valid file path with write permissions.

        Postconditions:
        - Writes the error message to the log file.
        - If there is an error during logging, prints an error message.

        >>> l = Logger()
        >>> import tempfile
        >>> temp_dir = tempfile.TemporaryDirectory()
        >>> log_file_path = os.path.join(temp_dir.name, 'test.log')
        >>> error_message = "An error occurred"
        >>> l.logError(error_message, log_file_path)
        >>> with open(log_file_path, 'r') as log_file:
        ...     logged_data = log_file.read().strip()
        >>> logged_data == f"ERROR: {error_message}"
        True
        >>> temp_dir.cleanup()
        """
        try:
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"ERROR: {error}\n")
        except Exception as e:
            print(f"Error logging error: {e}")

    def loadLog(self, log_file_path: str) -> List[Any]:
        """
        Loads a logged dataset from a log file.

        Preconditions:
        - `log_file_path` must be a valid file path with read permissions.

        Postconditions:
        - Returns a LoggedDataset containing the logged inputs and output.
        - If there is an error during loading, returns an empty LoggedDataset.

        >>> l = Logger()
        >>> import tempfile
        >>> temp_dir = tempfile.TemporaryDirectory()
        >>> log_file_path = os.path.join(temp_dir.name, 'test.log')
        >>> s = Serializer()
        >>> args = (1, 2, 3)
        >>> kwargs = {'a': 4, 'b': 5}
        >>> l.logCall(args, kwargs, log_file_path)
        >>> result = 42
        >>> execution_time = 0.123
        >>> l.logReturn(result, execution_time, log_file_path)
        >>> dataset = l.loadLog(log_file_path)
        >>> dataset[0] == {'args': args, 'kwargs': kwargs}
        True
        >>> dataset[1] == {'result': result, 'executionTime': execution_time}
        True

        """
        serializer = Serializer()
        dataset = []
        try:
            with open(log_file_path, 'rb') as log_file:
                for line in log_file:
                    dataset.append(serializer.deserialize(line.strip()))
        except Exception as e:
            print(f"Error loading log: {e}")
        return dataset

    def searchLogDirectory(self, log_directory: str) -> List[str]:
        """
        Searches the log directory and returns all well-formed log file paths.

        Preconditions:
        - `log_directory` must be a valid directory path with read permissions.

        Postconditions:
        - Returns a list of well-formed log file paths ending with ".log".
        - If there is an error during searching, returns an empty list.

        >>> l = Logger()
        >>> import tempfile
        >>> temp_dir = tempfile.TemporaryDirectory()
        >>> log_file_path = os.path.join(temp_dir.name, 'test.log')
        >>> temp_dir.cleanup()
        """
        log_files = []
        try:
            for file_name in os.listdir(log_directory):
                if file_name.endswith('.log'):
                    log_files.append(os.path.join(log_directory, file_name))
        except Exception as e:
            print(f"Error searching log directory: {e}")
        return log_files

doctest.testmod(verbose=True)

#import os
#import base64
#import json
#from datetime import datetime
#from typing import Any, List, Tuple, Dict
#
#class Logger:
#    def logCall(self, args: Tuple[Any, ...], kwargs: Dict[str, Any], log_file_path: str) -> None:
#        args = tuple(base64.b64encode(arg).decode('utf-8') if isinstance(arg, bytes) else arg for arg in args)
#        kwargs = {k: base64.b64encode(v).decode('utf-8') if isinstance(v, bytes) else v for k, v in kwargs.items()}
#        log_entry = {
#            "timestamp": datetime.now().isoformat(),
#            "type": "CALL",
#            "args": args,
#            "kwargs": kwargs
#        }
#        self._writeLogEntry(log_entry, log_file_path)
#
#    def logReturn(self, result: Any, executionTime: float, log_file_path: str) -> None:
#        result = base64.b64encode(result).decode('utf-8') if isinstance(result, bytes) else result
#        log_entry = {
#            "timestamp": datetime.now().isoformat(),
#            "type": "RETURN",
#            "result": result,
#            "executionTime": executionTime
#        }
#        self._writeLogEntry(log_entry, log_file_path)
#
#    def logError(self, error: str, log_file_path: str) -> None:
#        log_entry = {
#            "timestamp": datetime.now().isoformat(),
#            "type": "ERROR",
#            "error": error
#        }
#        self._writeLogEntry(log_entry, log_file_path)
#
#    def loadLog(self, log_file_path: str) -> Tuple[List[Any], Any]:
#        try:
#            with open(log_file_path, 'r') as log_file:
#                log_entries = [json.loads(line) for line in log_file]
#                inputs = []
#                output = None
#                for entry in log_entries:
#                    if entry["type"] == "CALL":
#                        args = tuple(base64.b64decode(arg) if isinstance(arg, str) and arg.endswith('=') else arg for arg in entry["args"])
#                        kwargs = {k: base64.b64decode(v) if isinstance(v, str) and v.endswith('=') else v for k, v in entry["kwargs"].items()}
#                        inputs.append((args, kwargs))
#                    elif entry["type"] == "RETURN":
#                        result = entry["result"]
#                        if isinstance(result, str) and result.endswith('='):
#                            result = base64.b64decode(result)
#                        output = result
#                return inputs, output
#        except Exception as e:
#            print(f"Error loading log: {e}")
#            return [], None
#
#    def _writeLogEntry(self, log_entry: dict, log_file_path: str) -> None:
#        try:
#            with open(log_file_path, 'a') as log_file:
#                json.dump(log_entry, log_file)
#                log_file.write('\n')
#        except Exception as e:
#            print(f"Error writing log entry: {e}")
#
#    def searchLogDirectory(self, log_directory: str) -> List[str]:
#        log_files = []
#        try:
#            for filename in os.listdir(log_directory):
#                if filename.endswith(".log"):
#                    log_files.append(os.path.join(log_directory, filename))
#        except Exception as e:
#            print(f"Error searching log directory: {e}")
#        return log_files
#
## Test the Logger
#logger = Logger()
#test_log_path = "logs/test_logger.log"
#
## Simulate logging calls and returns
#logger.logCall((b"test bytes", 123), {'param1': b'another bytes'}, test_log_path)
#logger.logReturn(b"return bytes", 0.123, test_log_path)
#
##
##import os
##import pickle
##from datetime import datetime
##from typing import Any, List, Tuple, Dict
##
##import os
##import json
##from datetime import datetime
##from typing import Any, List, Tuple
##
##import base64
##class Logger:
##    def logCall(self, args: Tuple[Any, ...], kwargs: Dict[str, Any], log_file_path: str) -> None:
##        """
##        Logs function call details to a specified log file in JSON format.
##        
##        Args:
##            args (Tuple[Any, ...]): Function arguments.
##            kwargs (Dict[str, Any]): Function keyword arguments.
##            log_file_path (str): Path to the log file.
##        """
##        try:
##            log_entry = {
##                "timestamp": datetime.now().isoformat(),
##                "type": "CALL",
##                "args": args,
##                "kwargs": kwargs
##            }
##            self._writeLogEntry(log_entry, log_file_path)
##        except Exception as e:
##            print(f"Error logging call: {e}")
##    
##    def logReturn(self, result: Any, executionTime: float, log_file_path: str) -> None:
##        """
##        Logs function return details to the specified log file in JSON format.
##        
##        Args:
##            result (Any): Function result.
##            executionTime (float): Time taken for the function execution.
##            log_file_path (str): Path to the log file.
##        """
##        try:
##            log_entry = {
##                "timestamp": datetime.now().isoformat(),
##                "type": "RETURN",
##                "result": result,
##                "executionTime": executionTime
##            }
##            self._writeLogEntry(log_entry, log_file_path)
##        except Exception as e:
##            print(f"Error logging return: {e}")
##    
##    def logError(self, error: str, log_file_path: str) -> None:
##        """
##        Logs an error message to the specified log file in JSON format.
##        
##        Args:
##            error (str): Error message.
##            log_file_path (str): Path to the log file.
##        """
##        try:
##            log_entry = {
##                "timestamp": datetime.now().isoformat(),
##                "type": "ERROR",
##                "error": error
##            }
##            self._writeLogEntry(log_entry, log_file_path)
##        except Exception as e:
##            print(f"Error logging error: {e}")
##
##    def loadLog(self, log_file_path: str) -> Tuple[List[Any], Any]:
##        """
##        Loads a logged dataset from a JSON log file.
##        
##        Args:
##            log_file_path (str): Path to the log file.
##        
##        Returns:
##            Tuple[List[Any], Any]: A tuple containing the logged inputs and output.
##        """
##        try:
##            with open(log_file_path, 'r') as log_file:
##                log_entries = [json.loads(line) for line in log_file]
##                inputs = []
##                output = None
##                for entry in log_entries:
##                    if entry["type"] == "CALL":
##                        inputs.append((entry["args"], entry["kwargs"]))
##                    elif entry["type"] == "RETURN":
##                        output = entry["result"]
##                return inputs, output
##        except Exception as e:
##            print(f"Error loading log: {e}")
##            return [], None
##
##    def searchLogDirectory(self, log_directory: str) -> List[str]:
##        """
##        Searches the log directory and returns all well-formed JSON log file paths.
##        
##        Args:
##            log_directory (str): Path to the directory containing log files.
##        
##        Returns:
##            List[str]: A list of well-formed JSON log file paths.
##        """
##        log_files = []
##        try:
##            for filename in os.listdir(log_directory):
##                if filename.endswith(".log"):
##                    log_files.append(os.path.join(log_directory, filename))
##        except Exception as e:
##            print(f"Error searching log directory: {e}")
##        return log_files
##
##
##    def _writeLogEntry(self, log_entry: dict, log_file_path: str) -> None:
##        """
##        Writes a log entry to the specified log file in JSON format.
##        
##        Args:
##            log_entry (dict): Log entry to be written.
##            log_file_path (str): Path to the log file.
##        """
##        try:
##            # Convert byte objects to base64-encoded strings
##            for key, value in log_entry.items():
##                if isinstance(value, bytes):
##                    log_entry[key] = base64.b64encode(value).decode('utf-8')
##            
##            with open(log_file_path, 'a') as log_file:
##                json.dump(log_entry, log_file)
##                log_file.write('\n')
##        except Exception as e:
##            print(f"Error writing log entry: {e}")
###    def _writeLogEntry(self, log_entry: dict, log_file_path: str) -> None:
###        """
###        Writes a log entry to the specified log file in JSON format.
###        
###        Args:
###            log_entry (dict): Log entry to be written.
###            log_file_path (str): Path to the log file.
###        """
###        try:
###            with open(log_file_path, 'a') as log_file:
###                json.dump(log_entry, log_file)
###                log_file.write('\n')
###        except Exception as e:
###            print(f"Error writing log entry: {e}")
###class Logger:
###    def logCall(self, args: bytes, kwargs: bytes, log_file_path: str) -> None:
###        """
###        Logs function call details to a specified log file.
###        
###        Args:
###            args (bytes): Serialized function arguments.
###            kwargs (bytes): Serialized function keyword arguments.
###            log_file_path (str): Path to the log file.
###        
###        >>> logger = Logger()
###        >>> log_call_path = "logCallTest.log"
###        >>> logger.logCall(pickle.dumps(("arg1", "arg2")), pickle.dumps({"kw1": 1, "kw2": 2}), log_call_path)
###        >>> os.path.exists(log_call_path)
###        True
###        """
###        try:
###            with open(log_file_path, 'ab') as log_file:
###                log_file.write(f"CALL @ {datetime.now()}\n".encode())
###                log_file.write(b"ARGS_START\n" + args + b"\nARGS_END\n")
###                log_file.write(b"KWARGS_START\n" + kwargs + b"\nKWARGS_END\n")
###        except Exception as e:
###            print(f"Error logging call: {e}")
###    
###    def logReturn(self, result: bytes, executionTime: float, log_file_path: str) -> None:
###        """
###        Logs function return details to the specified log file.
###        
###        Args:
###            result (bytes): Serialized function result.
###            executionTime (float): Time taken for the function execution.
###            log_file_path (str): Path to the log file.
###        
###        >>> logger = Logger()
###        >>> log_return_path = "logReturnTest.log"
###        >>> logger.logReturn(pickle.dumps("result data"), 1.23, log_return_path)
###        >>> os.path.exists(log_return_path)
###        True
###        """
###        try:
###            with open(log_file_path, 'ab') as log_file:
###                log_file.write(f"RETURN @ {datetime.now()}\n".encode())
###                log_file.write(b"RESULT_START\n" + result + b"\nRESULT_END\n")
###                log_file.write(f"TIME: {executionTime}s\n".encode())
###        except Exception as e:
###            print(f"Error logging return: {e}")
###    
###    def logError(self, error: str, log_file_path: str) -> None:
###        """
###        Logs an error message to the specified log file.
###        
###        Args:
###            error (str): Error message.
###            log_file_path (str): Path to the log file.
###        
###        >>> logger = Logger()
###        >>> log_error_path = "logErrorTest.log"
###        >>> logger.logError("An error occurred", log_error_path)
###        >>> os.path.exists(log_error_path)
###        True
###        """
###        try:
###            with open(log_file_path, 'ab') as log_file:
###                log_file.write(f"ERROR @ {datetime.now()}\n".encode())
###                log_file.write(f"ERROR: {error}\n".encode())
###        except Exception as e:
###            print(f"Error logging error: {e}")
###
###    def loadLog(self, log_file_path: str) -> Tuple[List[Any], Any]:
###        """
###        Loads a logged dataset from a log file.
###        
###        Args:
###            log_file_path (str): Path to the log file.
###        
###        Returns:
###            Tuple[List[Any], Any]: A tuple containing the logged inputs and output.
###        
###        >>> logger = Logger()
###        >>> log_call_path = "logCallTest.log"
###        >>> logger.logCall(pickle.dumps(("arg1", "arg2")), pickle.dumps({"kw1": 1, "kw2": 2}), log_call_path)
###        >>> log_data = logger.loadLog(log_call_path)
###        >>> log_data[0] == [('arg1', 'arg2'), {'kw1': 1, 'kw2': 2}]
###        True
###        """
###        try:
###            with open(log_file_path, 'rb') as log_file:
###                lines = log_file.readlines()
###                inputs = []
###                output = None
###                buffer = []
###                reading_args = False
###                reading_kwargs = False
###                reading_result = False
###                args_data = None
###                kwargs_data = None
###                for line in lines:
###                    if line.startswith(b"ARGS_START"):
###                        reading_args = True
###                        buffer = []
###                        continue
###                    elif line.startswith(b"ARGS_END"):
###                        reading_args = False
###                        args_data = pickle.loads(b''.join(buffer))
###                        continue
###                    elif line.startswith(b"KWARGS_START"):
###                        reading_kwargs = True
###                        buffer = []
###                        continue
###                    elif line.startswith(b"KWARGS_END"):
###                        reading_kwargs = False
###                        kwargs_data = pickle.loads(b''.join(buffer))
###                        continue
###                    elif line.startswith(b"RESULT_START"):
###                        reading_result = True
###                        buffer = []
###                        continue
###                    elif line.startswith(b"RESULT_END"):
###                        reading_result = False
###                        output = pickle.loads(b''.join(buffer))
###                        continue
###                    
###                    if reading_args or reading_kwargs or reading_result:
###                        buffer.append(line.strip())
###                
###                if args_data and kwargs_data:
###                    inputs = [args_data, kwargs_data]
###                
###                return inputs, output
###        except Exception as e:
###            print(f"Error loading log: {e}")
###            return [], None
###
###    def searchLogDirectory(self, log_directory: str) -> List[str]:
###        """
###        Searches the log directory and returns all well-formed log file paths.
###        
###        Args:
###            log_directory (str): Path to the directory containing log files.
###        
###        Returns:
###            List[str]: A list of well-formed log file paths.
###        
###        >>> logger = Logger()
###        >>> log_files = logger.searchLogDirectory(".")
###        >>> all(log_file.endswith(".log") for log_file in log_files)
###        True
###        """
###        log_files = []
###        try:
###            for filename in os.listdir(log_directory):
###                if filename.endswith(".log"):
###                    log_files.append(os.path.join(log_directory, filename))
###        except Exception as e:
###            print(f"Error searching log directory: {e}")
###        return log_files
##
##import doctest
##doctest.testmod(verbose=True)
