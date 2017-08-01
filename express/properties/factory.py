import importlib

from express.properties import settings


class PropertyFactory(object):
    """
    Property factory class.
    """

    def __init__(self):
        self.classes = dict()
        for k, v in settings.PROPERTIES_MANIFEST.items():
            cls_name = v['reference'].split('.')[-1]
            mod_name = '.'.join(v['reference'].split('.')[:-1])
            self.classes[k] = getattr(importlib.import_module(mod_name), cls_name)

    def get_property_class(self, name):
        """
        Returns a property class for a given name.

        Args:
            name (str): property name.

        Returns:
             cls
        """
        return self.classes[name]
