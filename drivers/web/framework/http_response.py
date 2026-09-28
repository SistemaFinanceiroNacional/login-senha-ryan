import json

from drivers.web.framework.http_response_interface import HttpResponseInterface
from drivers.web.framework.template import render_template


class HttpResponse(HttpResponseInterface):
    def __init__(self, headers, body, status):
        self.headers = headers
        self.body = body
        self.status = status

    def get_headers(self):
        return self.headers

    def get_body(self):
        return self.body

    def get_status(self):
        return self.status


STATUS_MESSAGES = {
    200: "OK",
    303: "See Other",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    409: "Conflict",
    413: "Content Too Large",
    414: "URI Too Long",
    431: "Request Header Fields Too Large",
    500: "Internal Server Error"
}


def response_as_bytes(response):
    body = str(response.get_body()).encode("utf-8")
    # The length of what is sent: bytes, not characters.
    headers = {**response.get_headers(), "Content-length": len(body)}
    status = response.get_status()
    status_line = f"HTTP/1.1 {status} {STATUS_MESSAGES.get(status, '')}"
    head = [status_line] + [f"{key}: {value}"
                            for key, value in headers.items()]
    return ("\r\n".join(head) + "\r\n\r\n").encode("utf-8") + body


def template_response(
        template_name: str,
        context=None,
        headers=None,
        status=200
) -> HttpResponse:
    context = context or {}
    headers = headers or {}
    html_content = render_template(template_name, context)
    headers = {"Content-Type": "text/html; charset=utf-8", **headers}
    response = HttpResponse(headers, html_content, status)
    return response


def redirect_response(to: str) -> HttpResponse:
    return HttpResponse({"Location": to}, "", 303)


def json_response(data, status=200, headers=None) -> HttpResponse:
    headers = {"Content-Type": "application/json; charset=utf-8",
               **(headers or {})}
    return HttpResponse(headers, json.dumps(data), status)
