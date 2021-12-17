import os
import functools
from typing import Union, Any

import unittest
from tests import TestBase, get_test_manifest


manifest = get_test_manifest()


class IntegrationTestBase(TestBase):
    """
    Test class for express integration tests.
    """

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


def get_test_config(test_config: Union[str, dict]) -> dict:
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
            **manifest["tests"][test_config],
        }
    return {
        **manifest["tests"][test_config["name"]],
        "property": test_config.pop("name"),
        "places": places,
        **test_config,
    }


def create_test(params: dict):
    """Function factory that generates a uniquely named TestCase method
    based on the required input parameters:

    Args:
        params(dict): {
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
    clean = lambda s: s.replace(".", "_").replace("/", "_").replace("-", "_")
    test_names = ["test"]
    for k, v in params.items():
        if isinstance(v, str):
            if k == "version":
                test_names.append(clean(v.replace(".", "")))
            else:
                test_names.append(clean(v))
    def do_test(self):
        for k, v in params.items():
            setattr(self, k, v)
        work_dir = self.work_dir(self.version, self.subdir)
        # TODO: os.path.join(workdir, self.filename) should not be necessary
        parser = self.parser(
            work_dir=work_dir, stdout_file=os.path.join(work_dir, self.filename)
        )
        actual = getattr(parser, self.property)()
        actual_index = self.test_config.pop("actual_index", None)
        if actual_index is not None:
            actual = actual[actual_index]
        expected = self.get_reference_value()
        comparison = self.test_config.pop("comparison")
        getattr(self, comparison)(actual, expected, **self.test_config)
    do_test.__name__ = "_".join(test_names)
    return do_test


def add_tests(cls: IntegrationTestBase, application_name: str):
    """Centralize create_test addition for application parser
    test classes. Just provide the named subclass of IntegrationTestBase
    and an application specified in the manifest.yaml and this should
    do the rest.
    """
    for application, all_versions in manifest["applications"].items():
        if application != application_name:
            continue
        for version, fixtures in all_versions.items():
            for fixture in fixtures:
                subdir = fixture["subdir"]
                filename = fixture["filename"]
                for test in fixture["tests"]:
                    test_config = get_test_config(test)
                    test_property = test_config.pop("property")
                    params = {
                        "application": application,
                        "version": version,
                        "subdir": subdir,
                        "filename": filename,
                        "property": test_property,
                        "test_config": test_config,
                    }
                    test_method = create_test(params)
                    setattr(cls, test_method.__name__, test_method)
