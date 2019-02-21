import warnings
import importlib

from express import settings

# disable pymatgen warnings
warnings.filterwarnings("ignore")


class ExPrESS(object):
    """
    Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.

    Args:
        parser_name (str): parser name.
        args (list): args passed to the parser.
        kwargs (dict): kwargs passed to the parser.
            espresso and vasp parsers specific keys:
                work_dir (str): path to the working directory.
                stdout_file (str): path to the stdout file.
            structure parser specific keys:
                structure_string (str): structure string.
                structure_format (str): structure format, poscar or espresso-in.
    """

    def __init__(self, parser_name=None, *args, **kwargs):
        self.parser = self._get_parser_class(parser_name)(*args, **kwargs) if parser_name else None

    def _get_parser_class(self, parser_name):
        """
        Returns parser class for a given parser name.

        Args:
            parser_name (str): parser name.

        Returns:

        """
        reference = settings.PARSERS_REGISTRY[parser_name]
        return self._get_class_by_reference(reference)

    def _get_class_by_reference(self, reference):
        """
        Returns class by reference.

        Args:
            reference (str): reference, e.g. express.parsers.apps.vasp.parser.VaspParser

        Returns:
             class
        """
        class_name = reference.split('.')[-1]
        module_name = '.'.join(reference.split('.')[:-1])
        return getattr(importlib.import_module(module_name), class_name)

    def _get_property_class(self, property_name):
        """
        Returns property class for a given property name.

        Args:
            property_name (str): property name.

        Returns:
            class
        """
        reference = settings.PROPERTIES_MANIFEST[property_name]["reference"]
        return self._get_class_by_reference(reference)

    def property(self, property_name, *args, **kwargs):
        """
        Extracts a given property and validates it against its schema.

        Args:
            property_name (str): property name.
            args (list): args passed to the underlying property method.
            kwargs (dict): kwargs passed to the underlying property method.

        Returns:
             dict
        """
        property_instance = self._get_property_class(property_name)(property_name, self.parser, *args, **kwargs)
        return property_instance.serialize_and_validate()
