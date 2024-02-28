from pathlib import Path
from exceptions import InvalidPathError
from tomllib import loads as toml_loads
from tomllib import TOMLDecodeError
from typing import Dict, Any
class Configuration:
    def __init__(self, path: Path, /):
        self.config_path: Path = path
        if self.file_exists():
            with open(str(self.config_path), "r+") as file:
                try:
                    self.content: Dict[str, Any] = toml_loads(file.read())
                except TOMLDecodeError:
                    print("[-] An invalid key-value pair has been detected on the configuration file")
                    exit(1)
        else:
            raise InvalidPathError("The path specified is not for a file and/or not exists")
    def file_exists(self) -> bool:
        if self.config_path.exists() and \
                self.config_path.is_file():
            return True
        else:
            return False

if __name__ == "__main__":
    conf_path: Path = Path(__file__).parent / "configuration.toml"
    conf: Configuration = Configuration(conf_path)
