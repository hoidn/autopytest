import os

class Configuration:
    def __init__(self, debug: bool = True, log_file_prefix: str = "logs"):
        self.debug = debug
        self.log_file_prefix = log_file_prefix

    def getDebugFlag(self) -> bool:
        return self.debug

    def getLogFilePrefix(self) -> str:
        return self.log_file_prefix

    def generateLogFilePath(self, module_path: str, function_name: str) -> str:
        if not module_path or not function_name:
            raise ValueError("Module path and function name must be non-empty strings.")
        log_file_name = f"{module_path}.{function_name}.log"
        log_file_path = os.path.join(self.log_file_prefix, log_file_name)
        return log_file_path
