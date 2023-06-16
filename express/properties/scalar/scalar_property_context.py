from typing import Type, Any
from express.properties.scalar import ScalarProperty
from express.parsers import BaseParser


class ScalarPropertyFromContext(ScalarProperty):
    def __init__(self, name: str, parser: Type[BaseParser], value: Any, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)
        self.value = value
