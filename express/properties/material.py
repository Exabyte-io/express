from express.properties import BaseProperty


class Material(BaseProperty):
    """
    Material class.

    Args:
        raw_data (dict): raw data used to form the material.
        cell (str): either primitive or conventional.
        args (list): material-specific args.
        kwargs (dict): material-specific kwargs.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(Material, self).__init__(name, raw_data, *args, **kwargs)

    def _serialize(self):
        """
        Serialize a material.

        Returns:
             dict
        """
        return {
            "name": "",
            "_id": "",
            "exabyteId": "",
            "formula": self.raw_data["reduced_formula"],
            "unitCellFormula": self.raw_data["formula"],
            "lattice": self.raw_data["lattice_bravais"],
            "basis": self.raw_data["basis"],
            "derivedProperties": {
                "volume": {
                    "value": 0,
                    "units": "angstrom^3"
                },
                "density": {
                    "value": 0,
                    "units": "g/cm^3"
                },
                "symmetry": {
                    "spaceGroupSymbol": self.raw_data["space_group_symbol"],
                    "tolerance": {
                        "value": 0.3,
                        "units": "angstrom"
                    }
                }
            },
        }
