class DuplicateUserException(Exception):
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)

class UnauthorizedAccessException(Exception):
    def __init__(self, message="Unauthorized access"):
        self.message = message
        super().__init__(self.message)

class NoDataFoundException(Exception):
    def __init__(self, message="No Data found"):
        self.message = message
        super().__init__(self.message)
