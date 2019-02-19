from express.properties.scalar import ScalarProperty


class ElementalRatio(ScalarProperty):
    """
    Elemental ratio property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ElementalRatio, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.elemental_ratios()[kwargs["element"]]

    def _serialize(self):
        return {
            'name': self.name,
            'value': self.value,
            "element": self.kwargs["element"]
        }
