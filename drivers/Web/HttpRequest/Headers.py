from drivers.Web.HttpRequest import IncompleteHttpRequest
from typing import NamedTuple, Callable
import logging


logger = logging.getLogger("drivers.Web.HttpRequest.Headers")


class HeaderBytes(NamedTuple):
    b: bytes
    name: bytes
    value: bytes


State = int
HeaderIncrementer = tuple[bytes, bytes, dict]
TransitionReturn = tuple[State, HeaderIncrementer]
StateHeaderTransition = Callable[[HeaderBytes], TransitionReturn]
StateHeaderTransitionTable = dict[State, StateHeaderTransition]
HeaderIncrements = tuple[State, HeaderIncrementer]


HEADER_NAME = 2
HEADER_VALUE_WITH_SPACE = 4
HEADER_VALUE = 5
HEADER_VALUE_CARRIAGE_RETURN = 6
NEW_HEADER_NAME = 7
MAYBE_FINAL_STATE = 9
FINAL_STATE = 10


def header_name(h_bytes: HeaderBytes) -> HeaderIncrements:
    if h_bytes.b == b'\r':
        return FINAL_STATE, (h_bytes.name, h_bytes.value, {})
    elif h_bytes.b == b':':
        return HEADER_VALUE_WITH_SPACE, (h_bytes.name, h_bytes.value, {})
    return HEADER_NAME, (h_bytes.name + h_bytes.b, h_bytes.value, {})


def header_value_space(h_bytes: HeaderBytes) -> HeaderIncrements:
    if h_bytes.b == b' ':
        return HEADER_VALUE, (h_bytes.name, h_bytes.value, {})
    return HEADER_VALUE_WITH_SPACE, (h_bytes.name, h_bytes.value, {})


def header_value(h_bytes: HeaderBytes) -> HeaderIncrements:
    if h_bytes.b == b'\r':
        return HEADER_VALUE_CARRIAGE_RETURN, (h_bytes.name, h_bytes.value, {})
    return HEADER_VALUE, (h_bytes.name, h_bytes.value + h_bytes.b, {})


def header_value_carriage(h_bytes: HeaderBytes) -> HeaderIncrements:
    if h_bytes.b == b'\n':
        name = h_bytes.name.decode("utf-8")
        value = h_bytes.value.decode("utf-8")
        return NEW_HEADER_NAME, (b'', b'', {name: value})
    return HEADER_VALUE_CARRIAGE_RETURN, (h_bytes.name, h_bytes.value, {})


def new_header_name(h_bytes: HeaderBytes) -> HeaderIncrements:
    if h_bytes.b == b'\r':
        return MAYBE_FINAL_STATE, (h_bytes.name, h_bytes.value, {})
    elif h_bytes.b != b':':
        return HEADER_NAME, (h_bytes.name + h_bytes.b, h_bytes.value, {})
    else:
        return NEW_HEADER_NAME, (h_bytes.name, h_bytes.value, {})


def maybe_final_state(h_bytes: HeaderBytes) -> HeaderIncrements:
    if h_bytes.b == b'\n':
        return FINAL_STATE, (h_bytes.name, h_bytes.value, {})
    else:
        return MAYBE_FINAL_STATE, (h_bytes.name, h_bytes.value, {})


def make_headers(socket):
    headers = {}
    state = NEW_HEADER_NAME
    headerName, headerValue = b'', b''

    transition_states: StateHeaderTransitionTable = {
        HEADER_NAME: header_name,
        HEADER_VALUE_WITH_SPACE: header_value_space,
        HEADER_VALUE: header_value,
        HEADER_VALUE_CARRIAGE_RETURN: header_value_carriage,
        NEW_HEADER_NAME: new_header_name,
        MAYBE_FINAL_STATE: maybe_final_state,
    }

    while state != FINAL_STATE:
        nextByte = socket.recv(1)
        logger.debug(f"GetHeaders: state = {state} & actual byte = {nextByte}")

        if nextByte == b'':
            break

        elif state in transition_states:
            h_bytes = HeaderBytes(nextByte, headerName, headerValue)
            state, new_values = transition_states[state](h_bytes)
            headerName, headerValue, new_headers = new_values
            headers = dict(**headers, **new_headers)
    if state != FINAL_STATE:
        raise IncompleteHttpRequest.IncompleteHttpRequest()

    return headers
