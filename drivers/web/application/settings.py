from pathlib import Path

from drivers.web.framework.httprequest.session import session_middleware
from drivers.web.application import urls


TEMPLATES = "templates"
AUTH_REDIRECT = "index.html"
MIDDLEWARES = [session_middleware]
ROOT_URLCONF = urls
BASE_DIR = Path(__file__).resolve().parent
