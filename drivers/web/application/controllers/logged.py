from drivers.web.framework.http_response import (
    HttpResponse,
    template_response,
    redirect_response
)
from drivers.web.framework.httprequest.http_request import HttpRequest
from drivers.web.framework.httprequest.session import (
    auth_needed,
    session_maker
)
from drivers.web.framework.routes import MethodDispatcher
from usecases.get_balance import GetBalanceUseCase
from usecases.get_transactions import GetTransactionsUseCase


class LoggedHandler(MethodDispatcher):
    def __init__(self,
                 get_balance: GetBalanceUseCase,
                 get_transactions: GetTransactionsUseCase
                 ):
        self.get_balance = get_balance
        self.get_transactions = get_transactions

    @auth_needed("client_id")
    @auth_needed("account_id")
    def get(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        client_id = session["client_id"]
        account_id = int(session["account_id"])
        balance = self.get_balance.execute(client_id, account_id)\
            .or_else(lambda: 0)
        transactions = self.get_transactions.execute(client_id, account_id)\
            .or_else(lambda: [])

        context = {"balance": balance, "transactions": transactions}
        response = template_response("account.html", context)
        return response

    def post(self, request: HttpRequest) -> HttpResponse:
        body = request.get_body().refine()
        account_id = body["account_id"]

        session = session_maker(request)
        session["account_id"] = account_id
        return redirect_response("/selectaccount")
