from exceptions import InvalidPathError
from tomllib import loads as toml_loads
from tomllib import TOMLDecodeError
from typing import Dict, Any
from os.path import isfile

def load_configuration(path: str, /) -> Dict[str, Any]:
    if isfile(path):
        with open(path, "r+") as file:
            try:
                content: Dict[str, Any] = toml_loads(file.read())
                return content
            except TOMLDecodeError:
                print("[-] An invalid key-value pair has been detected on the configuration file")
                exit(1)
    else:
        raise InvalidPathError("The path specified is not for a file and/or not exists")