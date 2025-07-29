from typing import Any


def flatten(data: Any) -> Any:
    def flatten_rec(data: Any, path: str) -> None:
        if isinstance(data, dict):
            for k, v in data.items():
                flatten_rec(v, path + (f".{k}" if path else k))
        elif isinstance(data, list):
            for i, v in enumerate(data):
                flatten_rec(v, path + f"[{i}]")
        else:
            flatten_dict[path or "."] = data

    flatten_dict: dict[str, Any] = {}
    flatten_rec(data, "")
    return flatten_dict
