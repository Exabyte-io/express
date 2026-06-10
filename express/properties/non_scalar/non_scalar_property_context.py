from typing import Any, Type

from express.parsers import BaseParser
from express.properties.non_scalar import NonScalarProperty


class NonScalarPropertyFromContext(NonScalarProperty):
    def __init__(
        self,
        name: str,
        parser: Type[BaseParser],
        data: Any = None,
        context: dict[str, Any] | None = None,
        context_key: str | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(name, parser, *args, **kwargs)
        if data is not None:
            self.data = data
        elif "value" in kwargs:
            self.data = kwargs["value"]
        else:
            self.data = context[context_key or name]

    def _serialize(self):
        if isinstance(self.data, dict):
            return {"name": self.name, **self.data}
        return {"name": self.name, "values": self.data}
