import os
from typing import Union

from tests import TestBase

class IntegrationTestBase(TestBase):
    pass

class ApplicationTestBase(TestBase):
    """
    Base class for express application parser tests.
    """

    def __init__(
        self,
        *args,
        application=None,
        version=None,
        subdir=None,
        filename=None,
        property=None,
        test_config=None,
        **kwargs
    ):
        super(ApplicationTestBase, self).__init__(*args, **kwargs)
        self.application = application
        self.version = version
        self.subdir = subdir
        self.filename = filename
        self.property = property
        self.test_config = test_config

    def work_dir(self, version: str, subdir: str):
        return os.path.join(
            self.rootDir, "fixtures", self.application, version, subdir
        )

    def get_reference_value(self):
        """Obtain the appropriate reference value to use as an expected value for the
        parser extraction."""
        sub_path = self.subdir.split("/")[-1]
        expected = self.references[self.version][sub_path][self.property]
        reference_index = self.test_config.pop("reference_index", None)
        if reference_index is not None:
            return expected[reference_index]
        return expected

    def get_actual_value(self):
        """Obtain the output value from a parser extraction to be compared
        with a reference value."""
        work_dir = self.work_dir(self.version, self.subdir)
        # TODO: os.path.join(workdir, self.filename) should not be necessary
        parser = self.parser(
            work_dir=work_dir, stdout_file=os.path.join(work_dir, self.filename)
        )
        actual = getattr(parser, self.property)()
        actual_index = self.test_config.pop("actual_index", None)
        if actual_index is not None:
            actual = actual[actual_index]
        return actual

    def get_test_config(self, test_config: Union[str, dict]) -> dict:
        """If specified at the individual test level, construct a granular test
        configuration, otherwise provide a default test configuration from the
        manifest.yaml.

        Note:
            See also the test_config_schema in the manifest.yaml file and
            example test_configs for usage. Test config keys that are not recognized
            as keyword args to comparison methods must be popped during processing
            or the comparison method will throw an unrecognized argument error.
        """
        places = 2
        if isinstance(test_config, str):
            return {
                "property": test_config,
                "places": places,
                **self.manifest["tests"][test_config],
            }
        return {
            **self.manifest["tests"][test_config["name"]],
            "property": test_config.pop("name"),
            "places": places,
            **test_config,
        }

    @staticmethod
    def get_test_name(test_params: dict):
        """Construct a unique test name based on the parameters of the test."""
        def clean(s: str):
            return s.replace(".", "").replace("/", "_").replace("-", "_")
        test_names = [
            clean(value) for value in test_params.values()
            if isinstance(value, str)
        ]
        return "_".join(["test"] + test_names)

    @staticmethod
    def create_test(test_params: dict):
        """Function factory that generates a uniquely named TestCase method
        based on the required input parameters:

        Args:
            test_params(dict): {
                "application": application name,
                "version": version string,
                "subdir": subdir to fixture,
                "filename": test filename,
                "property": test property,
                "test_config": test config from manifest,
            }

        Returns:
            func(function): a unittest.TestCase.test_method

        """
        def do_test(self):
            for k, v in test_params.items():
                setattr(self, k, v)
            expected = self.get_reference_value()
            actual = self.get_actual_value()
            comparison = self.test_config.pop("comparison")
            getattr(self, comparison)(actual, expected, **self.test_config)
        return do_test

def add_tests_from_manifest(cls: ApplicationTestBase):
    """Class decorator for ApplicationTestBase subclasses to leverage
    the test manifest specification. Just decorate the named subclass
    of ApplicationTestBase and fill in the manifest.yaml.

    Note: subclasses must specify the following attributes
        application(str): name of the application
        parser(cls): application parser class
        references(dict): reference values

    """
    test_manifest = cls.manifest["applications"][cls.application]
    for version, fixtures in test_manifest.items():
        for fixture in fixtures:
            for test in fixture["tests"]:
                test_config = cls.get_test_config(cls, test)
                test_params = {
                    "application": cls.application,
                    "version": version,
                    "subdir": fixture["subdir"],
                    "filename": fixture["filename"],
                    "property": test_config.pop("property"),
                    "test_config": test_config,
                }
                test_method = cls.create_test(test_params)
                test_name = cls.get_test_name(test_params)
                test_method.__name__ = test_name
                setattr(cls, test_name, test_method)
    return cls
