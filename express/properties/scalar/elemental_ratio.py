from express.properties.scalar import ScalarProperty


class ElementalRatio(ScalarProperty):
    """
    Elemental ratio property class.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(ElementalRatio, self).__init__(name, raw_data, *args, **kwargs)
        self.value = self.raw_data["elemental_ratios"][kwargs["element"]]

    def _serialize(self):
        return {
            'name': self.name,
            'value': self.value,
            "element": self.kwargs["element"]
        }
