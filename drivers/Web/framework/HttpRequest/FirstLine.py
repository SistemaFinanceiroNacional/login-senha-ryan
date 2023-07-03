import logging
from typing import Callable, Tuple, Dict
from drivers.Web.framework.HttpRequest import IncompleteHttpRequest
from drivers.Web.framework.HttpRequest.Resource import HttpResource

logger = logging.getLogger("drivers.Web.HttpRequest.FirstLine")


State = int
PushlineIncrementer = Tuple[bytes, bytes, bytes]
StateTransition = Callable[[bytes], Tuple[State, PushlineIncrementer]]
StateTransitionTable = Dict[State, StateTransition]
QueryMaker = Callable[[str], Dict[str, str]]
ResourceMaker = Callable[[str, QueryMaker], HttpResource]

# States
METHOD_STATE = 0
RESOURCE_STATE = 1
VERSION_STATE = 2
CARRIAGE_RETURN_STATE = 3
LINE_FINAL_STATE = 4


def method_state(b: bytes) -> Tuple[State, PushlineIncrementer]:
    if b == b' ':
        return RESOURCE_STATE, (b'', b'', b'')
    return METHOD_STATE, (b, b'', b'')


def resource_state(b: bytes) -> Tuple[State, PushlineIncrementer]:
    if b == b' ':
        return VERSION_STATE, (b'', b'', b'')
    return RESOURCE_STATE, (b'', b, b'')


def version_state(b: bytes) -> Tuple[State, PushlineIncrementer]:
    if b == b' ' or b in b'HTTP/':
        return VERSION_STATE, (b'', b'', b'')
    return VERSION_STATE, (b'', b'', b)


def carriage_return_state(b: bytes) -> Tuple[State, PushlineIncrementer]:
    if b == b'\n':
        return LINE_FINAL_STATE, (b'', b'', b'')
    return CARRIAGE_RETURN_STATE, (b'', b'', b'')


def get_first_line(socket, resource_mkr: ResourceMaker, query_mkr: QueryMaker):
    method, resource, version = b'', b'', b''
    state = 0

    transition_states: StateTransitionTable = {
        METHOD_STATE: method_state,
        RESOURCE_STATE: resource_state,
        VERSION_STATE: version_state,
        CARRIAGE_RETURN_STATE: carriage_return_state
    }

    while state != LINE_FINAL_STATE:
        next_byte = socket.recv(1)
        logger.debug(
            f"GetFirstLine: state = {state} & actual byte = {next_byte}"
        )

        if next_byte == b'':
            break

        elif next_byte == b'\r':
            state = CARRIAGE_RETURN_STATE

        elif state in transition_states:
            state, increments = transition_states[state](next_byte)
            (method_inc, resource_inc, version_inc) = increments
            method += method_inc
            resource += resource_inc
            version += version_inc

    if state != LINE_FINAL_STATE:
        raise IncompleteHttpRequest.IncompleteHttpRequest()

    decoded_method = method.decode("UTF-8")
    decoded_resource = resource_mkr(resource.decode("UTF-8"), query_mkr)
    decoded_version = version.decode("UTF-8")

    return decoded_method, decoded_resource, decoded_version
