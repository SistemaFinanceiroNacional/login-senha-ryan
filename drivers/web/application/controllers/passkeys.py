from typing import Callable, Tuple, Type, TypeVar

from drivers.web.framework.http_response import HttpResponse, json_response
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.session import session_maker
from drivers.web.framework.routes import MethodDispatcher
from maybe import Just, Maybe, Nothing
from usecases.passkeys.authentication import (
    FinishPasskeyAuthentication,
    StartPasskeyAuthentication
)
from usecases.passkeys.ceremony import CeremonyOptions, SignedInClient
from usecases.passkeys.registration import (
    FinishPasskeyRegistration,
    StartPasskeyRegistration
)

T = TypeVar("T")

CANNOT_REGISTER = "This login cannot be registered. Choose another one."
REGISTRATION_FAILED = "Could not create the passkey."
SIGN_IN_FAILED = "Could not sign in."


def of_type(kind: Type[T]) -> Callable[[object], Maybe[T]]:
    def checked(value: object) -> Maybe[T]:
        if isinstance(value, kind):
            return Just(value)
        return Nothing()
    return checked


def json_object(request: HttpRequest) -> Maybe[dict]:
    try:
        body = request.get_body().refine()
    except (ValueError, NotImplementedError, UnicodeDecodeError):
        return Nothing()
    return of_type(dict)(body)


def text(body: dict, name: str) -> Maybe[str]:
    return of_type(str)(body.get(name))


def ceremony_answer(body: dict) -> Maybe[Tuple[str, dict]]:
    """The ceremony id and the credential the authenticator produced."""
    return text(body, "ceremony").flat_map(
        lambda ceremony: of_type(dict)(body.get("credential")).map(
            lambda credential: (ceremony, credential)
        )
    )


def login_of(request: HttpRequest) -> Maybe[str]:
    return json_object(request).flat_map(lambda body: text(body, "login"))


def ceremony_response(ceremony: CeremonyOptions) -> HttpResponse:
    return json_response({
        "ceremony": ceremony.ceremony_id,
        "publicKey": ceremony.public_key,
    })


def error(message: str, status: int) -> Callable[[], HttpResponse]:
    return lambda: json_response({"error": message}, status)


def signed_in(request: HttpRequest, client: SignedInClient) -> HttpResponse:
    session = session_maker(request)
    session["client_id"] = client.id
    session["login"] = client.login
    return json_response({"redirect": "/"})


class PasskeyRegistrationOptionsHandler(MethodDispatcher):
    def __init__(self, start: StartPasskeyRegistration):
        self.start = start

    def post(self, request: HttpRequest) -> HttpResponse:
        return login_of(request).flat_map(self.start.execute)\
            .map(ceremony_response)\
            .or_else(error(CANNOT_REGISTER, 409))


class PasskeyRegistrationHandler(MethodDispatcher):
    def __init__(self, finish: FinishPasskeyRegistration):
        self.finish = finish

    def post(self, request: HttpRequest) -> HttpResponse:
        return json_object(request).flat_map(ceremony_answer).flat_map(
            lambda answer: self.finish.execute(*answer)
        ).map(
            lambda client: signed_in(request, client)
        ).or_else(error(REGISTRATION_FAILED, 400))


class PasskeyAuthenticationOptionsHandler(MethodDispatcher):
    def __init__(self, start: StartPasskeyAuthentication):
        self.start = start

    def post(self, request: HttpRequest) -> HttpResponse:
        return login_of(request).flat_map(self.start.execute)\
            .map(ceremony_response)\
            .or_else(error(SIGN_IN_FAILED, 401))


class PasskeyAuthenticationHandler(MethodDispatcher):
    def __init__(self, finish: FinishPasskeyAuthentication):
        self.finish = finish

    def post(self, request: HttpRequest) -> HttpResponse:
        return json_object(request).flat_map(ceremony_answer).flat_map(
            lambda answer: self.finish.execute(*answer)
        ).map(
            lambda client: signed_in(request, client)
        ).or_else(error(SIGN_IN_FAILED, 401))
