class ValidationError(Exception):
    pass


class InvalidChecksum(ValidationError):
    pass


class InvalidSourceError(InvalidChecksum):
    pass


class InvalidModifiedError(InvalidChecksum):
    pass
