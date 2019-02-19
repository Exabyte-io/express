from express.properties import BaseProperty


class ScalarProperty(BaseProperty):
    """
    Base scalar property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ScalarProperty, self).__init__(name, parser, *args, **kwargs)
        self.value = None
        self.units = None

    def _serialize(self):
        return {
            'name': self.name,
            'units': self.manifest["defaults"]["units"],
            'value': self.value,
        }
