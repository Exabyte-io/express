from express.properties.non_scalar import NonScalarProperty


class Lattice(NonScalarProperty):
    """
    Lattice is an object that holds geometrical information about the 3d periodic structure. There are 14 lattice
    types in total (see Bravais lattice). Lattice can be specified either in explicit way, by giving 3 lattice
    vectors, or in implicit way, by specifying a lattice type, lengths and angles between lattice vectors.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(Lattice, self).__init__(name, raw_data, *args, **kwargs)
        self.lattice = self.raw_data["lattice"]

    def _serialize(self):
        serialized_data = self.lattice
        serialized_data.update({
            'name': self.name,
        })
        return serialized_data
