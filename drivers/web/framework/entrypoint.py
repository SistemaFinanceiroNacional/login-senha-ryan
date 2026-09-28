import importlib
import os
from functools import reduce
from typing import List, Protocol
from drivers.web.framework import settings
from drivers.web.framework.route_interface import Route
from drivers.web.framework.router import Router
from drivers.web.framework.routes import EndPointRoute, FixedRoute
from drivers.web.framework.staticfiles import StaticFiles


class ClassResolver(Protocol):
    def __getitem__(self, item):
        pass


def get_application(di: ClassResolver):
    module_path = os.getenv('FRAMEWORK_SETTINGS_MODULE', '')
    settings_app = importlib.import_module(module_path)
    settings.app_settings = settings_app
    # A middleware given as a class is built by the DI container, so it
    # can depend on application services (e.g. a session store).
    middlewares = [
        di[middleware] if isinstance(middleware, type) else middleware
        for middleware in settings.app_settings.MIDDLEWARES
    ]
    urlpatterns = settings.app_settings.ROOT_URLCONF.urlpatterns

    combined_middleware = reduce(
        lambda f, g: lambda x: f(g(x)),
        middlewares,
        lambda x: x
    )

    routes: List[Route] = [
        FixedRoute(path, di[clazz]) for path, clazz in urlpatterns
    ]
    static_dir = getattr(settings.app_settings, "STATIC_DIR", None)
    if static_dir is not None:
        prefix = settings.app_settings.STATIC_URL
        routes.append(EndPointRoute(prefix, StaticFiles(static_dir, prefix)))
    router = Router(*routes)
    return combined_middleware(router)
