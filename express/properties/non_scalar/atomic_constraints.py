from express.properties.utils import to_array_with_ids
from express.properties.non_scalar import NonScalarProperty


class AtomicConstraints(NonScalarProperty):
    """
    Atomic constraints property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(AtomicConstraints, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            'name': self.name,
            "values": to_array_with_ids(self.parser.atomic_constraints())
        }
