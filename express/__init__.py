from express.parsers.factory import ParserFactory
from express.properties.factory import PropertyFactory


class ExPrESS(object):
    """
    Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.

    Args:
        work_dir (str): path to the working directory.
        kwargs:
            app_name (str): application name.
            app_stdout (str): path to the application stdout file.

    Attributes:
        parser: application parser instance.
    """

    def __init__(self, work_dir, **kwargs):
        self.parser = ParserFactory().get_parser(kwargs["app_name"])(work_dir, **kwargs)

    def extract_property(self, name, *args, **kwargs):
        """
        Extracts a given property and validates it against its schema.

        Args:
            name (str): property name.
            args (list): args passed to the underlying property method.
            kwargs (dict): kwargs passed to the underlying property method.

        Returns:
             dict
        """
        property_instance = PropertyFactory().get_property_class(name)(name, self.parser, *args, **kwargs)
        return property_instance.serialize_and_validate()
