import importlib

from express import settings


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
            pymatgen parser specific keys:
                structure_string (str): structure string.
                structure_format (str): structure format.
    """

    def __init__(self, parser_name=None, *args, **kwargs):
        if parser_name: self._parser = self._get_parser_class(parser_name)(*args, **kwargs)

    def _get_property_class(self, property_name):
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

    def _get_parser_class(self, parser_name):
        """
        Returns parser class for a given parser name.

        Args:
            parser_name (str): parser name.

        Returns:

        """
        path = settings.PARSERS_REGISTRY[parser_name]
        return getattr(importlib.import_module('.'.join(path.split('.')[:-1])), path.split('.')[-1])

    def _get_raw_data(self, property_name):
        """
        Calls parser interfaces to obtain raw data.

        Returns:
             dict
        """
        data = dict()
        for mixin in settings.PROPERTIES_MANIFEST[property_name].get("mixins", []):
            cls_name = mixin.split('.')[-1]
            module_name = '.'.join(mixin.split('.')[:-1])
            cls = getattr(importlib.import_module(module_name), cls_name)
            for name in [f for f in dir(cls) if callable(getattr(cls, f)) and not f.startswith("__")]:
                try:
                    data[name] = getattr(self._parser, name)()
                except:
                    data[name] = None
        return data

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
        raw_data = self._get_raw_data(property_name)
        property_instance = self._get_property_class(property_name)(property_name, raw_data, *args, **kwargs)
        return property_instance.serialize_and_validate()
