class ValidationError(Exception):
    pass


class InvalidSourceError(ValidationError):
    pass


class InvalidModifiedError(ValidationError):
    pass
