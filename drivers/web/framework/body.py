from typing import Dict

from drivers.web.framework.encodings import url_encoded


class BodyInterface:
    def raw(self):
        raise NotImplementedError()

    def refine(self):
        raise NotImplementedError()


class EmptyBody(BodyInterface):
    def raw(self):
        return b''

    def refine(self):
        return b''


class Body(BodyInterface):
    def __init__(self, content: bytes, content_type: str):
        self.content = content
        self.content_type = content_type

    def raw(self):
        return self.content

    def refine(self) -> Dict[str, str]:
        if self.content_type != "application/x-www-form-urlencoded":
            raise NotImplementedError()

        refined_content = url_encoded(self.content.decode('utf-8'))
        return refined_content
