import importlib

from express import settings


class ExPrESS(object):
    """
    Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.

    Args:
        work_dir (str): path to the working directory.
        app_name (str): application name.
        app_stdout_file (str): path to the application stdout file.
    """

    def __init__(self, work_dir=None, app_name=None, app_stdout_file=None):
        self._parser = self._get_parser_class(app_name)(work_dir, app_stdout_file) if app_name else None

    def _get_property_class(self, name):
        reference = settings.PROPERTIES_MANIFEST[name]["reference"]
        cls_name = reference.split('.')[-1]
        mod_name = '.'.join(reference.split('.')[:-1])
        return getattr(importlib.import_module(mod_name), cls_name)

    def _get_parser_class(self, name):
        path = settings.PARSERS_REGISTRY[name]
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
                    pass
        return data

    def extract_property(self, property_name, raw_data=None, *args, **kwargs):
        """
        Extracts a given property and validates it against its schema.

        Args:
            property_name (str): property name.
            raw_data (dict): raw data passed to the property class to calculate the property.
            args (list): args passed to the underlying property method.
            kwargs (dict): kwargs passed to the underlying property method.

        Returns:
             dict
        """
        raw_data = self._get_raw_data(property_name) if not raw_data else raw_data
        property_instance = self._get_property_class(property_name)(property_name, raw_data, *args, **kwargs)
        return property_instance.serialize_and_validate()
