class CompileError(BaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class BuildError(BaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
