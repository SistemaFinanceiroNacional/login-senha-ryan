from typing import Callable

from drivers.Web import IncompleteHttpRequest

import logging

logger = logging.getLogger("drivers.Web.httpRequest")
State = int
PushlineIncrementer = tuple[bytes, bytes, bytes]
StateTransition = Callable[[bytes], tuple[State, PushlineIncrementer]]
StateTransitionTable = dict[State, StateTransition]


class httpRequest:
    headers: dict[str, str]

    def __init__(self, header, body, method, resource, version):
        self.headers = header
        self.body = body
        self.method = method
        self.resource = resource
        self.version = version

    def getHeaders(self) -> dict[str, str]:
        return self.headers

    def getBody(self):
        return self.body

    def getMethod(self):
        return self.method

    def getResource(self):
        return self.resource

    def getVersion(self):
        return self.version


class http_resource:
    def __init__(self, endpoint, queryParameters):
        self.endpoint = endpoint
        self.queryParameters = queryParameters

    def getEndpoint(self):
        return self.endpoint

    def getQueryParameters(self):
        return self.queryParameters


def makeResource(rawResource: str) -> http_resource:
    splitRawResource = rawResource.split("?")
    endpoint = splitRawResource[0]

    if len(splitRawResource) > 1 and splitRawResource[1] != "":
        queryParameters = makeQueryParameters(splitRawResource[1])

    else:
        queryParameters = {}

    return http_resource(endpoint, queryParameters)


def makeQueryParameters(string):
    logger.debug(f"String: {string}")
    keysAndValues = string.split("&")
    queryParameters = {}
    for keyAndValue in keysAndValues:
        key, value = keyAndValue.split("=")
        queryParameters[key] = value

    return queryParameters


def getNextHttpRequest(socket):
    method, resource, version = getFirstLine(socket)
    logger.debug(f"Method: {method}; Resource: {resource}; Version: {version}")
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

    def method_state(b: bytes) -> tuple[State, PushlineIncrementer]:
        if b == b' ':
            return resourceState, (b'', b'', b'')
        return methodState, (b, b'', b'')

    def resource_state(b: bytes) -> tuple[State, PushlineIncrementer]:
        if b == b' ':
            return versionState, (b'', b'', b'')
        return resourceState, (b'', b, b'')

    def version_state(b: bytes) -> tuple[State, PushlineIncrementer]:
        if b == b' ' or b in b'HTTP/':
            return versionState, (b'', b'', b'')
        return versionState, (b'', b'', b)

    def carriageReturn_state(b: bytes) -> tuple[State, PushlineIncrementer]:
        if b == b'\n':
            return finalState, (b'', b'', b'')
        return carriageReturnState, (b'', b'', b'')

    transition_states: StateTransitionTable = {
        methodState: method_state,
        resourceState: resource_state,
        versionState: version_state,
        carriageReturnState: carriageReturn_state
    }

    while state != finalState:
        nextByte = socket.recv(1)
        logger.debug(
            f"GetFirstLine: state = {state} & actual byte = {nextByte}"
        )

        if nextByte == b'':
            break

        elif nextByte == b'\r':
            state = carriageReturnState

        elif state in transition_states:
            state, increments = transition_states[state](nextByte)
            (methodInc, resourceInc, versionInc) = increments
            method += methodInc
            resource += resourceInc
            version += versionInc

    if state != finalState:
        raise IncompleteHttpRequest.IncompleteHttpRequest()

    return method.decode("UTF-8"),\
        makeResource(resource.decode("UTF-8")),\
        version.decode("UTF-8")


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

        elif nextByte != b':' and state == NameOfHeader:
            headerName += nextByte

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
            headers[headerName.decode("utf-8")] = headerValue.decode("utf-8")
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
    defaultLength = '0'
    length = int(headers.get('Content-Length', defaultLength))
    body = socket.recv(length)
    howManyBytes = len(body)
    logger.debug(f"GetBody: length = {length}"
                 f" & actual body = {body}"
                 f" & actual body's size = {howManyBytes}"
                 )

    while howManyBytes < length:
        difference = length - howManyBytes
        rest = socket.recv(difference)
        logger.debug(f"GetBody: While statement: actual rest = {rest}"
                     f" & actual difference = {difference}"
                     )
        if rest == b'':
            raise IncompleteHttpRequest.IncompleteHttpRequest()

        else:
            body += rest
            howManyBytes = len(body)

    return body
