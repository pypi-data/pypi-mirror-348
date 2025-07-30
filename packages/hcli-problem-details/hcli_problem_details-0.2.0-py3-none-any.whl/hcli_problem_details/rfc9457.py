# Base exception class for errors implementing RFC9457 (problem details).
class ProblemDetail(Exception):
    def __init__(self, title, status, detail=None, type_uri=None, instance=None, extensions=None):
        super().__init__(title)
        self.title = title
        self.status = status
        self.detail = detail
        self.type_uri = type_uri or "about:blank"
        self.instance = instance
        self.extensions = extensions or {}

    # Convert the error to a dictionary following RFC9457 format.
    def to_dict(self):
        problem_detail = {
            "type": self.type_uri,
            "title": self.title,
            "status": self.status,
        }
        if self.detail:
            problem_detail["detail"] = self.detail
        if self.instance:
            problem_detail["instance"] = self.instance
        problem_detail.update(self.extensions)
        return problem_detail

    # Create a ProblemDetail instance for the given HTTP status code.
    #
    # Args:
    #     status_code (int): The HTTP status code.
    #     detail (str, optional): A human-readable explanation of the error.
    #     instance (str, optional): A URI identifying the specific occurrence of the problem.
    #     type_uri (str, optional): A URI identifying the problem type.
    #     extensions (dict, optional): Additional problem detail fields.
    #
    # Returns:
    #     ProblemDetail: An instance of the appropriate ProblemDetail subclass.
    @classmethod
    def from_status_code(cls, status_code, detail=None, instance=None, type_uri=None, extensions=None):
        return ProblemDetailRegistry.from_status_code(
            status_code=status_code,
            detail=detail,
            instance=instance,
            type_uri=type_uri,
            extensions=extensions
        )

# 4xx Client Errors
class BadRequestError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Bad Request",
            status=400,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class AuthenticationError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Unauthorized",
            status=401,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class PaymentRequiredError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Payment Required",
            status=402,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class AuthorizationError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Forbidden",
            status=403,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class NotFoundError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Not Found",
            status=404,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class MethodNotAllowedError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Method Not Allowed",
            status=405,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class NotAcceptableError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Not Acceptable",
            status=406,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class ProxyAuthenticationError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Proxy Authentication Required",
            status=407,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class RequestTimeoutError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Request Timeout",
            status=408,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class ConflictError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Conflict",
            status=409,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class GoneError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Gone",
            status=410,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class LengthRequiredError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Length Required",
            status=411,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class PreconditionFailedError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Precondition Failed",
            status=412,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class PayloadTooLargeError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Payload Too Large",
            status=413,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class URITooLongError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="URI Too Long",
            status=414,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class UnsupportedMediaTypeError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Unsupported Media Type",
            status=415,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class RangeNotSatisfiableError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Range Not Satisfiable",
            status=416,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class ExpectationFailedError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Expectation Failed",
            status=417,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class TeapotError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="I'm a teapot",
            status=418,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class MisdirectedRequestError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Misdirected Request",
            status=421,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class UnprocessableEntityError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Unprocessable Entity",
            status=422,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class LockedError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Locked",
            status=423,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class FailedDependencyError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Failed Dependency",
            status=424,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class TooEarlyError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Too Early",
            status=425,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class UpgradeRequiredError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Upgrade Required",
            status=426,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class PreconditionRequiredError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Precondition Required",
            status=428,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class TooManyRequestsError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Too Many Requests",
            status=429,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class RequestHeaderFieldsTooLargeError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Request Header Fields Too Large",
            status=431,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class UnavailableForLegalReasonsError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Unavailable For Legal Reasons",
            status=451,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

# 5xx Server Errors
class InternalServerError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Internal Server Error",
            status=500,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class NotImplementedError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Not Implemented",
            status=501,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class BadGatewayError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Bad Gateway",
            status=502,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class ServiceUnavailableError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Service Unavailable",
            status=503,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class GatewayTimeoutError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Gateway Timeout",
            status=504,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class HTTPVersionNotSupportedError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="HTTP Version Not Supported",
            status=505,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class VariantAlsoNegotiatesError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Variant Also Negotiates",
            status=506,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class InsufficientStorageError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Insufficient Storage",
            status=507,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class LoopDetectedError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Loop Detected",
            status=508,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class NotExtendedError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Not Extended",
            status=510,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

class NetworkAuthenticationRequiredError(ProblemDetail):
    def __init__(self, detail=None, instance=None, type_uri=None, extensions=None):
        super().__init__(
            title="Network Authentication Required",
            status=511,
            detail=detail,
            type_uri=type_uri,
            instance=instance,
            extensions=extensions
        )

# Registry to map status codes to ProblemDetail subclasses
class ProblemDetailRegistry:
    _status_to_class = {
        400: BadRequestError,
        401: AuthenticationError,
        402: PaymentRequiredError,
        403: AuthorizationError,
        404: NotFoundError,
        405: MethodNotAllowedError,
        406: NotAcceptableError,
        407: ProxyAuthenticationError,
        408: RequestTimeoutError,
        409: ConflictError,
        410: GoneError,
        411: LengthRequiredError,
        412: PreconditionFailedError,
        413: PayloadTooLargeError,
        414: URITooLongError,
        415: UnsupportedMediaTypeError,
        416: RangeNotSatisfiableError,
        417: ExpectationFailedError,
        418: TeapotError,
        421: MisdirectedRequestError,
        422: UnprocessableEntityError,
        423: LockedError,
        424: FailedDependencyError,
        425: TooEarlyError,
        426: UpgradeRequiredError,
        428: PreconditionRequiredError,
        429: TooManyRequestsError,
        431: RequestHeaderFieldsTooLargeError,
        451: UnavailableForLegalReasonsError,
        500: InternalServerError,
        501: NotImplementedError,
        502: BadGatewayError,
        503: ServiceUnavailableError,
        504: GatewayTimeoutError,
        505: HTTPVersionNotSupportedError,
        506: VariantAlsoNegotiatesError,
        507: InsufficientStorageError,
        508: LoopDetectedError,
        510: NotExtendedError,
        511: NetworkAuthenticationRequiredError,
    }

    # Create a ProblemDetail instance for the given HTTP status code.
    #
    # Args:
    #     status_code (int): The HTTP status code.
    #     detail (str, optional): A human-readable explanation of the error.
    #     instance (str, optional): A URI identifying the specific occurrence of the problem.
    #     type_uri (str, optional): A URI identifying the problem type.
    #     extensions (dict, optional): Additional problem detail fields.
    #
    # Returns:
    #     ProblemDetail: An instance of the appropriate ProblemDetail subclass.
    #
    # Raises:
    #     ValueError: If the status code is not mapped to a ProblemDetail subclass.
    @classmethod
    def from_status_code(cls, status_code, detail=None, instance=None, type_uri=None, extensions=None):
        problem_class = cls._status_to_class.get(status_code)
        if not problem_class:
            # Fallback to generic ProblemDetail with a default title
            return ProblemDetail(
                title=f"HTTP Status {status_code}",
                status=status_code,
                detail=detail,
                type_uri=type_uri,
                instance=instance,
                extensions=extensions
            )
        return problem_class(
            detail=detail,
            instance=instance,
            type_uri=type_uri,
            extensions=extensions
        )

