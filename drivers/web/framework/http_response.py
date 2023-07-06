from drivers.web.framework.template import render_template


class HttpResponse:
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


def response_as_bytes(response):
    headers = response.get_headers()
    body = response.get_body()
    headers["Content-length"] = len(body)
    status = response.get_status()
    version = "1.1"
    mapping_status = {
        200: "OK",
        303: "See Other",
        404: "Not Found",
        405: "Method Not Allowed"
    }
    status_message = mapping_status.get(status, '')
    complete_status = f"{status} {status_message}"
    response_to_bytes = f"HTTP/{version} {complete_status}\r\n"
    for key in headers:
        response_to_bytes += f"{key}: {headers[key]}\r\n"

    response_to_bytes += "\r\n"+f"{body}"

    return response_to_bytes.encode("utf-8")


def template_http_response(
        template_name: str,
        context=None,
        headers=None,
        status=200
) -> HttpResponse:
    context = context or {}
    headers = headers or {}
    html_content = render_template(template_name, context)
    headers = {"Content-Type": "text/html", **headers}
    response = HttpResponse(headers, html_content, status)
    return response
