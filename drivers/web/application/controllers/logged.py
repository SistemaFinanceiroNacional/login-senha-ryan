from drivers.web.application.controllers.parsing import parse_int
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
from domain.commontypes.types import AccountID, ClientID
from maybe import Maybe
from usecases.get_accounts import GetAccountsUseCase
from usecases.get_balance import GetBalanceUseCase
from usecases.get_transactions import GetTransactionsUseCase


def not_found() -> HttpResponse:
    return HttpResponse({}, "", 404)


class LoggedHandler(MethodDispatcher):
    def __init__(self,
                 get_balance: GetBalanceUseCase,
                 get_transactions: GetTransactionsUseCase,
                 get_accounts: GetAccountsUseCase
                 ):
        self.get_balance = get_balance
        self.get_transactions = get_transactions
        self.get_accounts = get_accounts

    @auth_needed("client_id")
    @auth_needed("account_id")
    def get(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        client_id = session["client_id"]
        return parse_int(session["account_id"]).flat_map(
            lambda account_id: self._account_page(client_id, account_id)
        ).or_else(not_found)

    def _account_page(self,
                      client_id: ClientID,
                      account_id: AccountID
                      ) -> Maybe[HttpResponse]:
        balance = self.get_balance.execute(client_id, account_id)
        transactions = self.get_transactions.execute(client_id, account_id)
        return balance.map(lambda amount: template_response(
            "account.html",
            {"balance": amount, "transactions": transactions.or_else(list)}
        ))

    @auth_needed("client_id")
    def post(self, request: HttpRequest) -> HttpResponse:
        session = session_maker(request)
        form = request.get_body().refine()
        client_accounts = list(self.get_accounts.execute(session["client_id"]))
        return parse_int(form.get("account_id")).filter(
            lambda account_id: account_id in client_accounts
        ).run(
            lambda account_id: session.__setitem__("account_id", account_id)
        ).map(
            lambda _: redirect_response("/selectaccount")
        ).or_else(not_found)
