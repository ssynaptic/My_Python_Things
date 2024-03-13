from typing import Any, Dict
from tomllib import loads as toml_loads
def get_configuration(path: str, /) -> Dict[str, Any]:
    with open(path, "r+") as file:
        data = file.read()
        config = toml_loads(data)
        return config
