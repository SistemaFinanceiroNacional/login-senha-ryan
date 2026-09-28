from typing import Dict
from urllib.parse import parse_qsl


def url_encoded(raw_resource: str) -> Dict[str, str]:
    """Decodes a query string or a form body (percent-encoding included);
    a field without a value is an empty string."""
    return dict(parse_qsl(raw_resource, keep_blank_values=True))
