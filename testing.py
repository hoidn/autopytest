from logger import Logger
from functionmapping import FunctionMapping
from configuration import Configuration

from typing import List, Tuple, Any, Optional, Callable

class TestSummary:
    def __init__(self, passed: int, failed: int, skipped: int):
        self.passed = passed
        self.failed = failed
        self.skipped = skipped

class Testing:
    def __init__(self, logger: Logger, function_mapping: FunctionMapping):
        self.logger = logger
        self.function_mapping = function_mapping

    def testCallable(self, log_file_path: str, func: Callable) -> bool:
        # Load the logged inputs and expected output from the log file
        logged_data = self.logger.loadLog(log_file_path)
        inputs, expected_output = logged_data.inputs, logged_data.output
        
        # Invoke the function with the logged inputs
        actual_output = func(*inputs[0], **inputs[1])
        
        # Compare the actual output with the expected output
        return actual_output == expected_output

    def createTestCase(self, log_file_path: str) -> Optional[Tuple[List[Any], Any, Callable]]:
        # Load the logged inputs and output from the log file
        logged_data = self.logger.loadLog(log_file_path)
        inputs, expected_output = logged_data
        
        # Load the function object from the log file path
        func = self.function_mapping.loadFunction(log_file_path=log_file_path)
        
        if func is None:
            return None
        
        # Construct and return the test case tuple
        return inputs, expected_output, func

    def runTestSuite(self, log_file_paths: List[str]) -> TestSummary:
        passed_count = 0
        failed_count = 0
        skipped_count = 0
        
        for log_file_path in log_file_paths:
            # Create a test case from the log file
            test_case = self.createTestCase(log_file_path)
            
            if test_case is None:
                skipped_count += 1
                continue
            
            inputs, expected_output, func = test_case
            
            # Execute the test case
            if self.testCallable(log_file_path, func):
                passed_count += 1
            else:
                failed_count += 1
        
        # Construct and return the test summary
        test_summary = TestSummary(passed_count, failed_count, skipped_count)
        return test_summary

if __name__ == '__main__':
    # Instantiate configuration with debugging enabled
    configuration = Configuration(debug=True, log_file_prefix="test_logs")

    # Instantiate Logger and FunctionMapping with new configuration
    test_logger = Logger()
    test_function_mapping = FunctionMapping('test_logs')
    testing = Testing(test_logger, test_function_mapping)

    # Example test: Assume we have valid log paths and functions are available
    test_log_paths = ["test_logs/__main__.valid_function.log", "test_logs/__main__.invalid_function.log"]
    test_summary = testing.runTestSuite(test_log_paths)
    test_summary.__dict__  # Display the results of the test summary
