import json
from pydantic_core import to_jsonable_python


def json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does.
    """
    return json.dumps(*args, default=to_jsonable_python, **kwargs)