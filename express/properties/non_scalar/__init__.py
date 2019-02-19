from express.properties import BaseProperty


class NonScalarProperty(BaseProperty):
    """
    Base non-scalar property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(NonScalarProperty, self).__init__(name, parser, *args, **kwargs)
