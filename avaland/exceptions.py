class AvalandException(Exception):
    pass


class SourceNotRegisteredException(AvalandException):
    pass


class SourceException(AvalandException):
    pass


class SourceNetworkError(SourceException):
    pass


class GatewayInvalidError(SourceException):
    pass
