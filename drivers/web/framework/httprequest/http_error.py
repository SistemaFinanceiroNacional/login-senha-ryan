MAX_REQUEST_LINE_BYTES = 8 * 1024
MAX_HEADERS_BYTES = 16 * 1024
MAX_HEADERS = 100
MAX_BODY_BYTES = 1024 * 1024


class HttpError(Exception):
    """A request the server refuses to read any further, with the status
    to answer before closing the connection."""

    def __init__(self, status: int, reason: str):
        super().__init__(reason)
        self.status = status


def too_long_request_line() -> HttpError:
    return HttpError(414, "request line too long")


def too_large_headers() -> HttpError:
    return HttpError(431, "request header fields too large")


def too_large_body() -> HttpError:
    return HttpError(413, "content too large")
