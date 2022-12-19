

import IncompleteHttpRequest

import logging

logger = logging.getLogger(__name__)

class httpRequest:
    def __init__(self, header, body, method, resource, version):
        self.headers = header
        self.body = body
        self.method = method
        self.resource = resource
        self.version = version

    def getHeaders(self):
        return self.headers

    def getBody(self):
        return self.body

    def getMethod(self):
        return self.method

    def getResource(self):
        return self.resource

    def getVersion(self):
        return self.version

def getNextHttpRequest(socket):
    method, resource, version = getFirstLine(socket)
    headers = getHeaders(socket)
    body = getBody(socket, headers)
    request = httpRequest(headers, body, method, resource, version)

    return request

def getFirstLine(socket):
    methodState = 0
    resourceState = 1
    versionState = 2
    carriageReturnState = 3
    finalState = 4
    method, resource, version = b'', b'', b''
    state = 0

    while state != finalState:
        nextByte = socket.recv(1)
        logger.debug(f"GetFirstLine: state = {state} & actual byte = {nextByte}")

        if nextByte == b'':
            break

        elif nextByte == b'\r':
            state = carriageReturnState

        elif nextByte == b'\n':
            state = finalState

        elif nextByte != b' ' and state == methodState:
            method += nextByte

        elif nextByte == b' ' and state == methodState:
            state = resourceState

        elif nextByte != b' ' and state == resourceState:
            resource += nextByte

        elif nextByte == b' ' and state == resourceState:
            state = versionState

        elif nextByte != b' ' and state == versionState:
            if nextByte not in b'HTTP/':
                version += nextByte

    if state != finalState:
        raise IncompleteHttpRequest.IncompleteHttpRequest()

    return method.decode("UTF-8"), resource.decode("UTF-8"), version.decode("UTF-8")


def getHeaders(socket):
    headers = {}
    NameOfHeader = 2
    NameOfHeaderWithCarriageReturn = 3
    ValueOfHeaderWithSpace = 4
    ValueOfHeader = 5
    ValueOfHeaderWithCarriageReturn = 6
    NewNameOfHeader = 7
    MaybeFinalState = 9
    FinalState = 10
    state = NewNameOfHeader

    headerName = b''
    headerValue = b''

    while state != FinalState:
        nextByte = socket.recv(1)
        logger.debug(f"GetHeaders: state = {state} & actual byte = {nextByte}")

        if nextByte == b'':
            break

        elif nextByte == b'\r' and state == NameOfHeader:
            state = FinalState

        elif nextByte != b':' and state == NameOfHeader:
            headerName += nextByte

        elif nextByte == b':' and state == NameOfHeader:
            state = ValueOfHeaderWithSpace

        elif nextByte == b'\r' and state == NameOfHeader:
            state = NameOfHeaderWithCarriageReturn

        elif nextByte == b'\n' and state == NameOfHeaderWithCarriageReturn:
            state = FinalState

        elif nextByte == b' ' and state == ValueOfHeaderWithSpace:
            state = ValueOfHeader

        elif nextByte != b'\r' and state == ValueOfHeader:
            headerValue += nextByte

        elif nextByte == b'\r' and state == ValueOfHeader:
            state = ValueOfHeaderWithCarriageReturn

        elif nextByte == b'\n' and state == ValueOfHeaderWithCarriageReturn:
            state = NewNameOfHeader
            headers[headerName] = headerValue
            headerName = b''
            headerValue = b''

        elif nextByte == b'\r' and state == NewNameOfHeader:
            state = MaybeFinalState

        elif nextByte == b'\n' and state == MaybeFinalState:
            state = FinalState

        elif nextByte != b':' and state == NewNameOfHeader:
            headerName += nextByte
            state = NameOfHeader

    if state != FinalState:
        raise IncompleteHttpRequest.IncompleteHttpRequest()

    return headers

def getBody(socket, headers):
    defaultLength = b'0'
    length = int(headers.get(b'Content-length', defaultLength))
    body = socket.recv(length)
    howManyBytes = len(body)
    logger.debug(f"GetBody: length = {length} & actual body = {body} & actual body's size = {howManyBytes}")

    while howManyBytes < length:
        difference = length - howManyBytes
        rest = socket.recv(difference)
        logger.debug(f"GetBody: While statement: actual rest = {rest} & actual difference = {difference}")
        if rest == b'':
            raise IncompleteHttpRequest.IncompleteHttpRequest()

        else:
            body += rest
            howManyBytes = len(body)

    return body

