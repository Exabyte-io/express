import re
import numpy as np
from typing import Dict, Optional, List
from express.properties.non_scalar import NonScalarProperty


class DielectricTensor(NonScalarProperty):
    """
    """

    def __init__(self, name, parser, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)

        self.tensors: Dict[str, Optional[np.ndarray]] = self.safely_invoke_parser_method("dielectric_tensor")

    def filename_to_tensor_type(self, name: str) -> dict:
        tensor_type = {}
        if name[0].lower() == "u":
            tensor_type["spin"] = 1/2
        elif name[0].lower() == "d":
            tensor_type["spin"] = -1 * 1/2

        if re.match(r"^[ud]?(epsr)(_.*)?\.dat$", name):
            tensor_type["part"] = "real"
        elif re.match(r"^[ud]?(epsi)(_.*)?\.dat$", name):
            tensor_type["part"] = "imaginary"
        return tensor_type

    def get_dielectric_tensors(self) -> List[dict]:
        values = []
        for key, data in self.tensors.items():
            tensor = {
                "frequencies": data["energy"].tolist(),
                "components": data["eps"].tolist()
            }
            tensor.update(self.filename_to_tensor_type(key))
            values.append(tensor)
        return sorted(values, key=lambda x: (-x.get("spin", 0), x.get("part") == "imaginary"))

    def _serialize(self):
        return {
            "name": self.name,
            "values": self.get_dielectric_tensors()
        }
