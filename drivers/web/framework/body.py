import json
from typing import Any

from drivers.web.framework.encodings import url_encoded

FORM = "application/x-www-form-urlencoded"
JSON = "application/json"


class BodyInterface:
    def raw(self):
        raise NotImplementedError()

    def refine(self) -> Any:
        raise NotImplementedError()


class EmptyBody(BodyInterface):
    def raw(self):
        return b''

    def refine(self) -> Any:
        return b''


class Body(BodyInterface):
    def __init__(self, content: bytes, content_type: str):
        self.content = content
        self.content_type = content_type

    def raw(self):
        return self.content

    def refine(self) -> Any:
        media_type = self.content_type.split(";")[0].strip().lower()
        text = self.content.decode('utf-8')
        if media_type == FORM:
            return url_encoded(text)
        if media_type == JSON:
            return json.loads(text)
        raise NotImplementedError()
