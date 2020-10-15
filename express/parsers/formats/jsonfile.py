import json

class BaseJSONParser(object):
    """
    Base JSON parser class.

    Args:
        path (str): path to the JSON file.
    """

    def __init__(self, path):
        self.path = path
        self.doc = None
        if self.path and os.path.exists(self.path):
            with open(self.path, mode='rb') as file:
                self.doc = self.loads(file.read().decode('utf-8'))

    @staticmethod
    def loads(text):
        """Loads JSON from text."""
        return json.loads(text)
