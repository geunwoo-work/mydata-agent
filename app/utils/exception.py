class CustomException(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class BuildingStoreException(CustomException):
    def __init__(self, message):
        super().__init__(message)

class InitializationException(CustomException):
    def __init__(self, message):
        super().__init__(message)
