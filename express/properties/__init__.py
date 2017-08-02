from esse import ESSE
from abc import abstractmethod


class BaseProperty(object):
    """
    Base Property class.

    Args:
        name (str): property name.
        raw_data (dict): raw data used to calculate the property.
        args (list): property-specific args.
        kwargs (dict): property-specific kwargs.

    Attributes:
        name (str): property name.
        parser (rupy.exapex.parsers.apps.BaseParser): parser instance.
        args (list): property-specific args.
        kwargs (dict): property-specific kwargs.
        mixins_data (dict): raw data obtained from mixins.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        self.name = name
        self.raw_data = raw_data
        self.args, self.kwargs = args, kwargs
        self.esse = ESSE()

    @abstractmethod
    def _serialize(self):
        pass

    def serialize_and_validate(self):
        """
        Serialize the property and validates it against the schema.

        Returns:
            dict
        """
        instance = self._serialize()
        self.esse.validate(instance, self.esse.get_schema(self.name))
        return instance
