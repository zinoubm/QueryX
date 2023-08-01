class UnauthorizedException(Exception):
    def __init__(self, message="Unauthorized"):
        self.message = message
        super().__init__(self.message)


class RegistrationErrorException(Exception):
    def __init__(self, message="Couldn't Register"):
        self.message = message
        super().__init__(self.message)


class LogoutErrorException(Exception):
    def __init__(self, message="Couldn't Logout"):
        self.message = message
        super().__init__(self.message)


class DocumentUploadErrorException(Exception):
    def __init__(self, message="Couldn't Upload Document"):
        self.message = message
        super().__init__(self.message)


class GetDocumentsErrorException(Exception):
    def __init__(self, message="Couldn't Get Documents"):
        self.message = message
        super().__init__(self.message)


class QueryErrorException(Exception):
    def __init__(self, message="Couldn't Post Query"):
        self.message = message
        super().__init__(self.message)
