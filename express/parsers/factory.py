import importlib

from express.parsers import settings


class ParserFactory(object):
    """
    Parser factory class.
    """

    def __init__(self):
        self.parsers = dict()
        for name, path in settings.PARSERS_REGISTRY.items():
            self.parsers[name] = getattr(importlib.import_module('.'.join(path.split('.')[:-1])), path.split('.')[-1])

    def get_parser(self, name):
        """
        Returns a parser class for a given application name.

        Args:
            name (str): application name such as vasp and espresso.

        Returns:
             cls: application parser class.
        """
        return self.parsers[name]
