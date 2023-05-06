from typing import Callable
from drivers.Web.HttpRequest import IncompleteHttpRequest
from drivers.Web.HttpRequest.Resource import http_resource
import logging

logger = logging.getLogger("drivers.Web.HttpRequest.FirstLine")

# Types
State = int
PushlineIncrementer = tuple[bytes, bytes, bytes]
StateTransition = Callable[[bytes], tuple[State, PushlineIncrementer]]
StateTransitionTable = dict[State, StateTransition]
QueryMaker = Callable[[str], dict[str, str]]
ResourceMaker = Callable[[str, QueryMaker], http_resource]

# States
METHOD_STATE = 0
RESOURCE_STATE = 1
VERSION_STATE = 2
CARRIAGE_RETURN_STATE = 3
LINE_FINAL_STATE = 4


def method_state(b: bytes) -> tuple[State, PushlineIncrementer]:
    if b == b' ':
        return RESOURCE_STATE, (b'', b'', b'')
    return METHOD_STATE, (b, b'', b'')


def resource_state(b: bytes) -> tuple[State, PushlineIncrementer]:
    if b == b' ':
        return VERSION_STATE, (b'', b'', b'')
    return RESOURCE_STATE, (b'', b, b'')


def version_state(b: bytes) -> tuple[State, PushlineIncrementer]:
    if b == b' ' or b in b'HTTP/':
        return VERSION_STATE, (b'', b'', b'')
    return VERSION_STATE, (b'', b'', b)


def carriageReturn_state(b: bytes) -> tuple[State, PushlineIncrementer]:
    if b == b'\n':
        return LINE_FINAL_STATE, (b'', b'', b'')
    return CARRIAGE_RETURN_STATE, (b'', b'', b'')


def getFirstLine(socket, resource_mkr: ResourceMaker, query_mkr: QueryMaker):
    method, resource, version = b'', b'', b''
    state = 0

    transition_states: StateTransitionTable = {
        METHOD_STATE: method_state,
        RESOURCE_STATE: resource_state,
        VERSION_STATE: version_state,
        CARRIAGE_RETURN_STATE: carriageReturn_state
    }

    while state != LINE_FINAL_STATE:
        nextByte = socket.recv(1)
        logger.debug(
            f"GetFirstLine: state = {state} & actual byte = {nextByte}"
        )

        if nextByte == b'':
            break

        elif nextByte == b'\r':
            state = CARRIAGE_RETURN_STATE

        elif state in transition_states:
            state, increments = transition_states[state](nextByte)
            (methodInc, resourceInc, versionInc) = increments
            method += methodInc
            resource += resourceInc
            version += versionInc

    if state != LINE_FINAL_STATE:
        raise IncompleteHttpRequest.IncompleteHttpRequest()

    decoded_method = method.decode("UTF-8")
    decoded_resource = resource_mkr(resource.decode("UTF-8"), query_mkr)
    decoded_version = version.decode("UTF-8")

    return decoded_method, decoded_resource, decoded_version
