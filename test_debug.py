import unittest
import os
import shutil
from debug import Debug
from configuration import Configuration
from serializer import Serializer
from logger import Logger
from functionmapping import FunctionMapping

def sample_function(arg1, arg2):
    return arg1 + arg2

class DebugTests(unittest.TestCase):
    def setUp(self):
        self.configuration = Configuration(debug=True, log_file_prefix="test_logs")
        self.serializer = Serializer()
        self.logger = Logger()
        self.function_mapping = FunctionMapping(log_directory="test_logs")
        self.debug = Debug(self.configuration, self.serializer, self.logger, self.function_mapping)

    def tearDown(self):
        # Clean up the test logs directory
        if os.path.exists("test_logs"):
            shutil.rmtree("test_logs")

    def test_decorate_debugging_disabled(self):
        self.configuration.debug = False
        decorated_function = self.debug.decorate(sample_function)
        result = decorated_function(1, 2)
        self.assertEqual(result, 3)
        self.assertFalse(os.path.exists("test_logs"))

    def test_decorate_debugging_enabled(self):
        self.configuration.debug = True
        decorated_function = self.debug.decorate(sample_function)
        result = decorated_function(1, 2)
        self.assertEqual(result, 3)
        module_path = self.function_mapping.get_module_path(sample_function)
        log_file_path = self.configuration.generateLogFilePath(module_path, sample_function.__name__)
        print(f"Checking log file path: {log_file_path}")
        self.assertTrue(os.path.exists(log_file_path))

    def test_decorate_debugging_enabled_exception(self):
        self.configuration.debug = True
        
        @self.debug.decorate
        def exception_function(arg1, arg2):
            raise ValueError("Test exception")

        with self.assertRaises(ValueError):
            exception_function(1, 2)
        module_path = self.function_mapping.get_module_path(exception_function)
        log_file_path = self.configuration.generateLogFilePath(module_path, exception_function.__name__)
        print(f"Checking log file path: {log_file_path}")
        self.assertTrue(os.path.exists(log_file_path))

if __name__ == '__main__':
    unittest.main()
