from drivers.web.application.controllers.parsing import parse_float, parse_int
from drivers.web.framework.http_response import (
    HttpResponse,
    redirect_response
)
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.session import (
    auth_needed,
    session_maker
)
from drivers.web.framework.routes import MethodDispatcher
from usecases.deposit import DepositUseCase


class DepositHandler(MethodDispatcher):
    def __init__(self, deposit: DepositUseCase):
        self.deposit = deposit

    @auth_needed("client_id")
    @auth_needed("account_id")
    def post(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        client_id = session["client_id"]
        form = request.get_body().refine()

        deposited = parse_int(session["account_id"]).flat_map(
            lambda account_id: parse_float(form.get("amount")).map(
                lambda amount: self.deposit.execute(
                    client_id, account_id, amount
                )
            )
        ).or_else(lambda: False)

        if deposited:
            return redirect_response("/selectaccount")
        return HttpResponse({}, "", 400)
