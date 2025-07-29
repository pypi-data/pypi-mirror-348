from csv import DictWriter
from io import StringIO
from pathlib import Path
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


def json_to_csv(
    data: dict[str, dict[str, Any]] | list[dict[str, Any]],
    /,
    csv_path: Path | str | None = None,
    *,
    key_field_name: str = "_key",
) -> str:
    if isinstance(data, dict):
        data = [
            {
                # In case there is already a key field in each record,
                # the new key field will be overwritten.
                # It is okay though as the existing key field is likely
                # serving the purpose of containing keys.
                key_field_name: key,
                **value,
            }
            for key, value in data.items()
        ]

    fields: set[str] = set()
    for record in data:
        fields.update(record.keys())

    sio = StringIO()

    writer = DictWriter(sio, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)

    csv_str: str = sio.getvalue()

    if csv_path:
        Path(csv_path).write_text(csv_str)

    return csv_str
