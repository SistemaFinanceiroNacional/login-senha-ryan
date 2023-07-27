import importlib
import os
from functools import reduce
from typing import Protocol
from drivers.web.framework import settings
from drivers.web.framework.router import Router
from drivers.web.framework.routes import FixedRoute


class ClassResolver(Protocol):
    def __getitem__(self, item):
        pass


def get_application(di: ClassResolver):
    module_path = os.getenv('FRAMEWORK_SETTINGS_MODULE', '')
    settings_app = importlib.import_module(module_path)
    settings.app_settings = settings_app
    middlewares = settings.app_settings.MIDDLEWARES
    urlpatterns = settings.app_settings.ROOT_URLCONF.urlpatterns

    combined_middleware = reduce(
        lambda f, g: lambda x: f(g(x)),
        middlewares,
        lambda x: x
    )

    fixed_routes = [FixedRoute(path, di[clazz]) for path, clazz in urlpatterns]
    router = Router(*fixed_routes)
    return combined_middleware(router)
