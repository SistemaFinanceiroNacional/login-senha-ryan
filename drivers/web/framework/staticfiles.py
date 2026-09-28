import re
from pathlib import Path

from drivers.web.framework.http_response import HttpResponse
from drivers.web.framework.httprequest.http_request import HttpRequest

# Only plain file names: no directories, no "..", no hidden files.
FILE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*\.[a-z0-9]+$")
CONTENT_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".png": "image/png",
}


class StaticFiles:
    """Serves the files of one directory (stylesheets, scripts, images)
    under a URL prefix."""

    def __init__(self, directory: Path, prefix: str):
        self.directory = Path(directory)
        self.prefix = prefix

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.get_method().upper() not in ("GET", "HEAD"):
            return HttpResponse({"Allow": "GET, HEAD"}, "", 405)
        name = request.get_resource().get_endpoint()[len(self.prefix):]
        path = self.directory / name
        content_type = CONTENT_TYPES.get(path.suffix)
        if not FILE_NAME.match(name) or content_type is None \
                or not path.is_file():
            return HttpResponse({}, "", 404)
        return HttpResponse(
            {"Content-Type": content_type,
             "Cache-Control": "public, max-age=3600"},
            path.read_bytes(),
            200
        )
