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
        inputs, expected_output = logged_data
        print(f"Loaded inputs: {inputs}")
        print(f"Expected output: {expected_output}")

        # Invoke the function with the logged inputs
        if len(inputs) == 2:
            actual_output = func(*inputs[0], **inputs[1])
        elif len(inputs) == 1:
            actual_output = func(*inputs[0])
        else:
            actual_output = func()

        print(f"Actual output: {actual_output}")

        # Compare the actual output with the expected output
        return actual_output == expected_output
#    def testCallable(self, log_file_path: str, func: Callable) -> bool:
#        print(f"Testing callable for log file: {log_file_path}")
#        # Load the logged inputs and expected output from the log file
#        logged_data = self.logger.loadLog(log_file_path)
#        inputs, expected_output = logged_data
#        print(f"Loaded inputs: {inputs}")
#        print(f"Expected output: {expected_output}")
#
#        # Invoke the function with the logged inputs
#        actual_output = func(*inputs[0], **inputs[1])
#        print(f"Actual output: {actual_output}")
#
#        # Compare the actual output with the expected output
#        result = actual_output == expected_output
#        print(f"Test result: {result}")
#        return result

    def createTestCase(self, log_file_path: str) -> Optional[Tuple[List[Any], Any, Callable]]:
        print(f"Creating test case for log file: {log_file_path}")
        # Load the logged inputs and output from the log file
        logged_data = self.logger.loadLog(log_file_path)
        inputs, expected_output = logged_data
        print(f"Loaded inputs: {inputs}")
        print(f"Expected output: {expected_output}")

        # Load the function object from the log file path
        func = self.function_mapping.load_function(log_file_path=log_file_path)
        print(f"Loaded function: {func}")

        if func is None:
            print("Function not found. Skipping test case.")
            return None

        # Construct and return the test case tuple
        test_case = (inputs, expected_output, func)
        print(f"Created test case: {test_case}")
        return test_case

    def runTestSuite(self, log_file_paths: List[str]) -> TestSummary:
        print("Running test suite...")
        passed_count = 0
        failed_count = 0
        skipped_count = 0

        for log_file_path in log_file_paths:
            print(f"Processing log file: {log_file_path}")
            # Create a test case from the log file
            test_case = self.createTestCase(log_file_path)

            if test_case is None:
                skipped_count += 1
                print("Test case skipped.")
                continue

            inputs, expected_output, func = test_case
            print(f"Executing test case: {test_case}")

            # Execute the test case
            if self.testCallable(log_file_path, func):
                passed_count += 1
                print("Test case passed.")
            else:
                failed_count += 1
                print("Test case failed.")

        # Construct and return the test summary
        test_summary = TestSummary(passed_count, failed_count, skipped_count)
        print(f"Test summary: {test_summary.__dict__}")
        return test_summary

if __name__ == '__main__':
    logdir = 'logs'
    # Instantiate configuration with debugging enabled
    configuration = Configuration(debug=True, log_file_prefix=logdir)
    print(f"Configuration: {configuration.__dict__}")

    # Instantiate Logger and FunctionMapping with new configuration
    test_logger = Logger()
    test_function_mapping = FunctionMapping(logdir)
    print(f"Logger: {test_logger}")
    print(f"FunctionMapping: {test_function_mapping}")

    testing = Testing(test_logger, test_function_mapping)
    test_log_paths = test_logger.searchLogDirectory(logdir)
    print(f"Test log paths: {test_log_paths}")

    # Example test: Assume we have valid log paths and functions are available
    #test_log_paths = [f"{logdir}/__main__.valid_function.log", f"{logdir}/__main__.invalid_function.log"]
    test_summary = testing.runTestSuite(test_log_paths)
    print(f"Final test summary: {test_summary.__dict__}")
