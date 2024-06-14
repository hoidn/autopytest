import unittest
from unittest.mock import MagicMock, patch
from debug import Debug
from configuration import Configuration
from serializer import Serializer
from logger import Logger
from functionmapping import FunctionMapping

class TestDebug(unittest.TestCase):
    def setUp(self):
        self.configuration = Configuration(debug=True)
        self.serializer = Serializer()
        self.logger = Logger()
        self.function_mapping = FunctionMapping()
        self.debug = Debug(self.configuration, self.serializer, self.logger, self.function_mapping)

    def test_decorate_debugging_disabled(self):
        self.configuration.debug = False
        
        @self.debug.decorate
        def test_function(x):
            return x * 2

        result = test_function(5)
        self.assertEqual(result, 10)
    @patch('builtins.print')
    def test_decorate_debugging_enabled(self, mock_print):
        @self.debug.decorate
        def test_function(x):
            return x * 2

        with patch.object(self.serializer, 'serialize', return_value=b'serialized_data'):
            with patch.object(self.logger, 'logCall') as mock_logCall:
                with patch.object(self.logger, 'logReturn') as mock_logReturn:
                    result = test_function(5)
                    self.assertEqual(result, 10)
                    mock_logCall.assert_called_once()
                    mock_logReturn.assert_called_once()
                    mock_print.assert_any_call('<__main__.test_function.test_function>CALL')
                    mock_print.assert_any_call('5')
                    mock_print.assert_any_call('</__main__.test_function.test_function>RETURN 10')

    @patch('builtins.print')
    def test_decorate_debugging_enabled_exception(self, mock_print):
        @self.debug.decorate
        def test_function(x):
            raise ValueError('Test exception')

        with patch.object(self.serializer, 'serialize', return_value=b'serialized_data'):
            with patch.object(self.logger, 'logCall') as mock_logCall:
                with patch.object(self.logger, 'logError') as mock_logError:
                    with self.assertRaises(ValueError):
                        test_function(5)
                    mock_logCall.assert_called_once()
                    mock_logError.assert_called_once()
                    mock_print.assert_any_call('<__main__.test_function.test_function>CALL')
                    mock_print.assert_any_call('5')
                    mock_print.assert_any_call('<__main__.test_function.test_function>ERROR Test exception')

    def test_format_console_log_array_type(self):
        data = (MagicMock(shape=(2, 3), dtype='int64'),)
        formatted_log = self.debug._formatConsoleLog(data)
        self.assertEqual(formatted_log, "type=<class 'unittest.mock.MagicMock'>, shape=(2, 3), dtype=int64")
    @patch('builtins.print')

    def test_decorate_debugging_enabled_limit_invocations(self):
        @self.debug.decorate
        def test_function(x):
            return x * 2

        with patch.object(self.serializer, 'serialize', return_value=b'serialized_data'):
            with patch.object(self.logger, 'logCall') as mock_logCall:
                with patch.object(self.logger, 'logReturn') as mock_logReturn:
                    test_function(5)
                    test_function(10)
                    test_function(15)
                    self.assertEqual(mock_logCall.call_count, 2)
                    self.assertEqual(mock_logReturn.call_count, 2)

    def test_format_console_log(self):
        data = (5, 'hello')
        formatted_log = self.debug._formatConsoleLog(data)
        self.assertEqual(formatted_log, '5, hello')

if __name__ == '__main__':
    unittest.main()
#import unittest
#import os
#import shutil
#from debug import Debug
#from configuration import Configuration
#from serializer import Serializer
#from logger import Logger
#from functionmapping import FunctionMapping
#
#def sample_function(arg1, arg2):
#    return arg1 + arg2
#
#class DebugTests(unittest.TestCase):
#    def setUp(self):
#        self.configuration = Configuration(debug=True, log_file_prefix="test_logs")
#        self.serializer = Serializer()
#        self.logger = Logger()
#        self.function_mapping = FunctionMapping(log_directory="test_logs")
#        self.debug = Debug(self.configuration, self.serializer, self.logger, self.function_mapping)
#
#    def tearDown(self):
#        # Clean up the test logs directory
#        if os.path.exists("test_logs"):
#            shutil.rmtree("test_logs")
#
#    def test_decorate_debugging_disabled(self):
#        self.configuration.debug = False
#        decorated_function = self.debug.decorate(sample_function)
#        result = decorated_function(1, 2)
#        self.assertEqual(result, 3)
#        self.assertFalse(os.path.exists("test_logs"))
#
#    def test_decorate_debugging_enabled(self):
#        self.configuration.debug = True
#        decorated_function = self.debug.decorate(sample_function)
#        result = decorated_function(1, 2)
#        self.assertEqual(result, 3)
#        module_path = self.function_mapping.get_module_path(sample_function)
#        log_file_path = self.configuration.generateLogFilePath(module_path, sample_function.__name__)
#        print(f"Checking log file path: {log_file_path}")
#        self.assertTrue(os.path.exists(log_file_path))
#
#    def test_decorate_debugging_enabled_exception(self):
#        self.configuration.debug = True
#        
#        @self.debug.decorate
#        def exception_function(arg1, arg2):
#            raise ValueError("Test exception")
#
#        with self.assertRaises(ValueError):
#            exception_function(1, 2)
#        module_path = self.function_mapping.get_module_path(exception_function)
#        log_file_path = self.configuration.generateLogFilePath(module_path, exception_function.__name__)
#        print(f"Checking log file path: {log_file_path}")
#        self.assertTrue(os.path.exists(log_file_path))
#
#if __name__ == '__main__':
#    unittest.main()
