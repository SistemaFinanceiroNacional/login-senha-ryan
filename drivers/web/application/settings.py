from pathlib import Path

from drivers.web.framework.httprequest.csrf import CsrfMiddleware
from drivers.web.framework.httprequest.session import SessionMiddleware
from drivers.web.application import urls


TEMPLATES = "templates"
AUTH_REDIRECT = "index.html"
MIDDLEWARES = [SessionMiddleware, CsrfMiddleware]
ROOT_URLCONF = urls
BASE_DIR = Path(__file__).resolve().parent
STATIC_URL = "/static/"
STATIC_DIR = BASE_DIR / "static"
