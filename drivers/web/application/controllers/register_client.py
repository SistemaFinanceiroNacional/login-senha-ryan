from drivers.web.framework.http_response import (
    HttpResponse,
    template_response,
    redirect_response
)
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.routes import MethodDispatcher
from usecases.register_client import RegisterClientUseCase


class RegisterClientHandler(MethodDispatcher):
    def __init__(self, register_client_use_case: RegisterClientUseCase):
        self.register_use_case = register_client_use_case

    def get(self, request: HttpRequest) -> HttpResponse:
        response = template_response("register.html")
        return response

    def post(self, request: HttpRequest) -> HttpResponse:
        body = request.get_body().refine()
        new_username = body["newUsername"]
        new_password = body["newPassword"]
        opened = self.register_use_case.execute(new_username, new_password)
        destiny = "/"
        if not opened:
            destiny = "/register"
        return redirect_response(destiny)
