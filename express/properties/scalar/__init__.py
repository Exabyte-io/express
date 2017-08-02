from express.properties import BaseProperty


class ScalarProperty(BaseProperty):
    """
    Base scalar property class.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(ScalarProperty, self).__init__(name, raw_data, *args, **kwargs)
        self.value = None
        self.units = None

    def _serialize(self):
        return {
            'name': self.name,
            'units': self.esse.get_schema_default_values(self.name)["units"],
            'value': self.value,
        }
