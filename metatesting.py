import os
import shutil
import importlib.util
from typing import List
from logger import Logger
from testing import Testing, TestSummary

class MetaTesting:
    def __init__(self, logger: Logger, testing: Testing):
        self.logger = logger
        self.testing = testing

    def runSelfTests(self, test_directory: str) -> TestSummary:
        # Generate test functions and modules
        test_module_paths = self.generateTestModules(test_directory)
        
        # Run the generated test functions and log their outputs
        log_file_paths = self.runTestFunctions(test_module_paths)
        
        # Validate the test results against the logged outputs
        test_summary = self.testing.runTestSuite(log_file_paths)
        
        # Clean up the generated test artifacts
        self.cleanUpTestArtifacts(test_directory)
        
        return test_summary

    def generateTestModules(self, test_directory: str) -> List[str]:
        # Generate test function definitions
        test_function_definitions = self.generateTestFunctionDefinitions()
        
        # Create test modules with the generated function definitions
        test_module_paths = []
        for i, function_definitions in enumerate(test_function_definitions):
            module_path = self.createTestModule(f"{test_directory}/test_module_{i}.py", function_definitions)
            test_module_paths.append(module_path)
        
        return test_module_paths

    def generateTestFunctionDefinitions(self) -> List[List[str]]:
        # Generate test function definitions
        test_function_definitions = [
            [
                "def test_function_1(x, y):",
                "    return x + y",
                "",
                "def test_function_2(a, b):",
                "    return a * b"
            ],
            [
                "def test_function_3(s):",
                "    return s.upper()",
                "",
                "def test_function_4(lst):",
                "    return sorted(lst)"
            ]
        ]
        
        return test_function_definitions

    def createTestModule(self, module_path: str, function_definitions: List[str]) -> str:
        # Create a Python module at the specified path with the provided function definitions
        with open(module_path, "w") as file:
            file.write("\n".join(function_definitions))
        
        return module_path

    def runTestFunctions(self, test_module_paths: List[str]) -> List[str]:
        log_file_paths = []
        
        for module_path in test_module_paths:
            # Import the test module
            spec = importlib.util.spec_from_file_location("test_module", module_path)
            test_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test_module)
            
            # Run the test functions and log their outputs
            for function_name in dir(test_module):
                if function_name.startswith("test_function_"):
                    test_function = getattr(test_module, function_name)
                    
                    # Generate test inputs
                    test_inputs = self.generateTestInputs(function_name)
                    
                    # Run the test function and log its output
                    for inputs in test_inputs:
                        output = test_function(*inputs)
                        log_file_path = self.logger.logOutput(module_path, function_name, inputs, output)
                        log_file_paths.append(log_file_path)
        
        return log_file_paths

    def generateTestInputs(self, function_name: str) -> List[tuple]:
        # Generate test inputs based on the function name
        if function_name == "test_function_1":
            return [(1, 2), (3, 4), (5, 6)]
        elif function_name == "test_function_2":
            return [(2, 3), (4, 5), (6, 7)]
        elif function_name == "test_function_3":
            return [("hello",), ("world",), ("foo",)]
        elif function_name == "test_function_4":
            return [([3, 1, 2],), ([6, 4, 5],), ([9, 7, 8],)]
        else:
            return []

    def cleanUpTestArtifacts(self, path: str) -> None:
        # Delete the specified file or directory
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

