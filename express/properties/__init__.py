from esse import ESSE
from abc import abstractmethod


class BaseProperty(object):
    """
    Base Property class.

    Args:
        name (str): property name.
        parser: an instance of parser class.
        args (list): property-specific args.
        kwargs (dict): property-specific kwargs.
    """

    def __init__(self, name, parser, *args, **kwargs):
        self.name, self.parser = name, parser
        self.args, self.kwargs = args, kwargs
        self.esse = ESSE()
        self.manifest = self.esse.get_property_manifest(self.name)

    @abstractmethod
    def _serialize(self):
        pass

    @property
    def schema(self):
        return self.esse.get_schema_by_id(self.manifest["schemaId"])

    def serialize_and_validate(self):
        """
        Serialize the property and validates it against the schema.

        Returns:
            dict
        """
        instance = self._serialize()
        self.esse.validate(instance, self.schema)
        return instance

    def safely_invoke_parser_method(self, method_name, *args, **kwargs):
        if hasattr(self.parser, method_name):
            return getattr(self.parser, method_name)(*args, **kwargs)
