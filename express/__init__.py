import warnings
import importlib
import numpy as np

try:
    from ._version import version as __version__
except ModuleNotFoundError:
    __version__ = None

from express import settings
from express.properties import BaseProperty
from express.parsers import BaseParser
from typing import Type, Optional, Union

# disable pymatgen warnings
warnings.filterwarnings("ignore")


class ExPrESS(object):
    """
    Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.

    Args:
        parser_name (str): parser name.
        args (list): args passed to the parser.
        kwargs (dict): kwargs passed to the parser.
            espresso, vasp and nwchem parsers specific keys:
                work_dir (str): path to the working directory.
                stdout_file (str): path to the stdout file.
            structure parser specific keys:
                structure_string (str): structure string.
                structure_format (str): structure format, poscar or espresso-in, or nwchem-in.
    """

    def __init__(self, parser_name=None, *args, **kwargs):
        parser_class = self._get_parser_class(parser_name) if parser_name else None

        # Look up the parser class, if it exists
        if parser_class is not None:
            self.parser = parser_class(*args, **kwargs)
        else:
            self.parser = None

    def _get_parser_class(self, parser_name: str) -> Optional[Type[BaseParser]]:
        """
        Returns parser class for a given parser name.

        Args:
            parser_name (str): parser name.

        Returns:
            class
        """
        # If-statement will return None for parser class if the parser is missing from the registry
        if parser_name in settings.PARSERS_REGISTRY:
            reference = settings.PARSERS_REGISTRY[parser_name]
            parser_class = self._get_class_by_reference(reference)
        else:
            parser_class = None

        return parser_class

    def _get_class_by_reference(self, reference: str) -> Union[Type[BaseProperty], Type[BaseParser]]:
        """
        Returns class by reference.

        Args:
            reference (str): reference, e.g. express.parsers.apps.vasp.parser.VaspParser

        Returns:
             class
        """
        class_name = reference.split(".")[-1]
        module_name = ".".join(reference.split(".")[:-1])
        return getattr(importlib.import_module(module_name), class_name)

    def _get_property_class(self, property_name: str) -> Type[BaseProperty]:
        """
        Returns property class for a given property name.

        Args:
            property_name (str): property name.

        Returns:
            class
        """
        reference: str = settings.PROPERTIES_MANIFEST[property_name]["reference"]
        return self._get_class_by_reference(reference)

    def property(self, property_name: str, *args, **kwargs) -> dict:
        """
        Extracts a given property and validates it against its schema.

        Args:
            property_name (str): property name.
            args (list): args passed to the underlying property method.
            kwargs (dict): kwargs passed to the underlying property method.

        Returns:
             dict
        """
        Property_Class = self._get_property_class(property_name)
        property_instance = Property_Class(property_name, self.parser, *args, **kwargs)
        return property_instance.serialize_and_validate()
