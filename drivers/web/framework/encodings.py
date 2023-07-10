from typing import Dict


def url_encoded(raw_resource: str) -> Dict[str, str]:
    keys_and_values = raw_resource.split("&")
    query_parameters = {}
    for key_and_value in keys_and_values:
        key, value = key_and_value.split("=")
        query_parameters[key] = value

    return query_parameters
