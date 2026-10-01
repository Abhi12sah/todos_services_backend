class AppException(Exception):
    """Base exception for application errors."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str
    ):
        self.status_code = status_code
        self.code = code
        self.message = message

        super().__init__(message)


class UserNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            status_code=404,
            code="USER_NOT_FOUND",
            message="User not found"
        )


class TodoNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            status_code=404,
            code="TODO_NOT_FOUND",
            message="Todo not found"
        )


class EmailAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            status_code=409,
            code="EMAIL_ALREADY_EXISTS",
            message="Email already registered"
        )


class ForeignKeyViolationException(AppException):
    def __init__(
        self,
        message: str = "Referenced resource does not exist"
    ):
        super().__init__(
            status_code=400,
            code="FOREIGN_KEY_VIOLATION",
            message=message
        )