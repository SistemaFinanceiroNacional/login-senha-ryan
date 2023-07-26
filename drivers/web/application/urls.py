from drivers.web.application.controllers.home import HomeHandler
from drivers.web.application.controllers.logged import LoggedHandler
from drivers.web.application.controllers.logout import LogoutHandler
from drivers.web.application.controllers.register_client import (
    RegisterClientHandler
)


urlpatterns = [
    ("/", HomeHandler),
    ("/logout", LogoutHandler),
    ("/register", RegisterClientHandler),
    ("/selectaccount", LoggedHandler)
]
