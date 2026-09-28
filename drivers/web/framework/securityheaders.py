from drivers.web.framework.http_response import HttpResponse
from drivers.web.framework.http_response_interface import HttpResponseInterface
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.types import Handler

CONTENT_SECURITY_POLICY = "; ".join([
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self'",
    "img-src 'self'",
    "connect-src 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "base-uri 'none'",
    "object-src 'none'",
])

SECURITY_HEADERS = {
    # Only this site's own scripts, styles and images; no framing.
    "Content-Security-Policy": CONTENT_SECURITY_POLICY,
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "same-origin",
    # Browsers only honour it over HTTPS, where it pins the site to HTTPS.
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    # Pages show balances and statements: never store them. Responses
    # that may be cached (static files) say so themselves.
    "Cache-Control": "no-store",
}


class SecurityHeadersMiddleware:
    def __call__(self, app: Handler) -> Handler:
        def wrapper(request: HttpRequest) -> HttpResponseInterface:
            response = app(request)
            headers = {**SECURITY_HEADERS, **response.get_headers()}
            return HttpResponse(headers, response.get_body(),
                                response.get_status())

        return wrapper
