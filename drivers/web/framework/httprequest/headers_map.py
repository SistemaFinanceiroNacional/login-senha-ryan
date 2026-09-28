from typing import Dict, Iterable, Mapping, Tuple, Union


class Headers(Dict[str, str]):
    """HTTP header fields. Their names are case-insensitive (RFC 9110):
    they are kept in lower case and looked up in lower case."""

    def __init__(self,
                 fields: Union[Mapping[str, str],
                               Iterable[Tuple[str, str]]] = ()
                 ):
        super().__init__()
        items = fields.items() if isinstance(fields, Mapping) else fields
        for name, value in items:
            self[name] = value

    def __setitem__(self, name: str, value: str) -> None:
        super().__setitem__(name.lower(), value)

    def __getitem__(self, name: str) -> str:
        return super().__getitem__(name.lower())

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and super().__contains__(name.lower())

    def get(self, name: str, default=None):  # type: ignore[override]
        return super().get(name.lower(), default)
