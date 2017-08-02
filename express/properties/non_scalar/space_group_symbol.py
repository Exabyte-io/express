import pymatgen as mg

from express.properties.non_scalar import NonScalarProperty


class SpaceGroupSymbol(NonScalarProperty):
    """
    Defines elemental and geometrical constitution of the unit cell.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(SpaceGroupSymbol, self).__init__(name, raw_data, *args, **kwargs)

    def _serialize(self):
        structure = mg.Structure.from_str(self.kwargs["structure_str"], self.kwargs["fmt"])
        symmetry = mg.symmetry.analyzer.SpacegroupAnalyzer(structure).get_spacegroup_symbol()
        return {
            "name": self.name,
            "value": symmetry
        }
