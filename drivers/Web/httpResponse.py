
class httpResponse:
    def __init__(self, headers, body, status):
        self.headers = headers
        self.body = body
        self.status = status

    def getHeaders(self):
        return self.headers

    def getBody(self):
        return self.body

    def getStatus(self):
        return self.status


def responseAsBytes(response):
    headers = response.getHeaders()
    body = response.getBody()
    headers["Content-length"] = len(body)
    status = response.getStatus()
    version = "1.1"
    mappingStatus = {200: "OK"}
    responseToBytes = f"HTTP/{version} {status} {mappingStatus.get(status, '')}\r\n"
    for key in headers:
        responseToBytes += f"{key}: {headers[key]}\r\n"

    responseToBytes += "\r\n"+f"{body}"

    return responseToBytes.encode("utf-8")