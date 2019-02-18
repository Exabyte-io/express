import importlib

from express import settings


class ExPrESS(object):
    """
    Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.
    """

    def get_parser_class(self, parser_name):
        """
        Returns parser class for a given parser name.

        Args:
            parser_name (str): parser name.

        Returns:

        """
        path = settings.PARSERS_REGISTRY[parser_name]
        return getattr(importlib.import_module('.'.join(path.split('.')[:-1])), path.split('.')[-1])

    def get_parser(self, parser_name, *args, **kwargs):
        """
        Initializes and returns a parser.

        Args:
            parser_name (str): parser name.
            args (list): args passed to the parser.
            kwargs (dict): kwargs passed to the parser.
                espresso and vasp parsers specific keys:
                    work_dir (str): path to the working directory.
                    stdout_file (str): path to the stdout file.
                pymatgen parser specific keys:
                    structure_string (str): structure string.
                    structure_format (str): structure format.
        """
        return self.get_parser_class(parser_name)(*args, **kwargs)

    def get_property_class(self, property_name):
        """
        Returns property class for a given property name.

        Args:
            property_name (str): property name.

        Returns:

        """
        reference = settings.PROPERTIES_MANIFEST[property_name]["reference"]
        cls_name = reference.split('.')[-1]
        mod_name = '.'.join(reference.split('.')[:-1])
        return getattr(importlib.import_module(mod_name), cls_name)

    def get_property(self, property_name, parser, *args, **kwargs):
        """
        Extracts a given property and validates it against its schema.

        Args:
            property_name (str): property name.
            parser (express.parsers.BaseParser): an instance of the parser.
            args (list): args passed to the underlying property method.
            kwargs (dict): kwargs passed to the underlying property method.

        Returns:
             dict
        """
        property_instance = self.get_property_class(property_name)(property_name, parser, *args, **kwargs)
        return property_instance.serialize_and_validate()
