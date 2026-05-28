from typing import Any

from express.properties.non_scalar import NonScalarProperty


class FormationEnergyReferencesFromContext(NonScalarProperty):
    def __init__(self, name, parser, value: Any, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)
        self.value = value

    def _serialize(self):
        return {
            "name": self.name,
            "value": self.value,
        }
