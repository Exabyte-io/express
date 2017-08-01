import importlib

from abc import abstractmethod

from esse import ESSE
from express.properties import settings


class BaseProperty(object):
    """
    Base Property class.

    Args:
        name (str): property name.
        parser (rupy.exapex.parsers.apps.BaseParser): parser instance.
        args (list): property-specific args.
        kwargs (dict): property-specific kwargs.

    Attributes:
        name (str): property name.
        parser (rupy.exapex.parsers.apps.BaseParser): parser instance.
        args (list): property-specific args.
        kwargs (dict): property-specific kwargs.
        mixins_data (dict): raw data obtained from mixins.
    """

    def __init__(self, name, parser, *args, **kwargs):
        self.name = name
        self.parser = parser
        self.args, self.kwargs = args, kwargs
        self.manifest = settings.PROPERTIES_MANIFEST[name]
        self.parser_data = self._get_data_from_parsers()
        self.esse = ESSE()

    @abstractmethod
    def _serialize(self):
        pass

    def _get_data_from_parsers(self):
        """
        Calls parser interfaces to obtain data.

        Returns:
             dict
        """
        data = dict()
        for mixin in self.manifest["mixins"]:
            cls_name = mixin.split('.')[-1]
            module_name = '.'.join(mixin.split('.')[:-1])
            cls = getattr(importlib.import_module(module_name), cls_name)
            for name in [f for f in dir(cls) if callable(getattr(cls, f)) and not f.startswith("__")]:
                try:
                    data[name] = getattr(self.parser, name)()
                except:
                    pass
        return data

    def serialize_and_validate(self):
        """
        Serialize the property and validates it against the schema.

        Returns:
            dict
        """
        instance = self._serialize()
        self.esse.validate(instance, self.esse.get_schema(self.name))
        return instance
