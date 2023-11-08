import abc
import json
import os
from typing import IO, Any, Dict, Optional


class Fixtures(abc.ABC):

    def __init__(self, entity: str, filename: str):
        self.entity: str = entity
        self.filename: str = filename
        self.json: Optional[Dict[str, Any]] = None

    def load_json(self) -> Dict[str, Any]:
        if self.json is not None:
            return self.json

        root_dir: str = os.path.dirname(os.path.abspath(__file__))
        file: IO = open(
            f'{root_dir}/{self.entity}/data/{self.filename}.json')

        self.json = json.load(file)

        file.close()

        return self.json

    @abc.abstractmethod
    def load_entity(self) -> Any:
        raise NotImplementedError
