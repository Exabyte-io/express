import os
import functools
from typing import Union, Any

from express.parsers.apps.espresso.parser import EspressoParser
from express.parsers.apps.vasp.parser import VaspParser
from express.parsers.apps.nwchem.parser import NwchemParser

import unittest
from tests import TestBase, get_test_manifest
from tests.fixtures.vasp import references as vasp_references
from tests.fixtures.espresso import references as espresso_references
from tests.fixtures.nwchem import references as nwchem_references


# Dynamically generate all our tests from these 3 objects
manifest = get_test_manifest()
parser_classes = {
    "espresso": EspressoParser,
    "nwchem": NwchemParser,
    "vasp": VaspParser,
}
references = {
    "espresso": espresso_references.REFERENCE_VALUES,
    "nwchem": nwchem_references.REFERENCE_VALUES,
    "vasp": vasp_references.REFERENCE_VALUES,
}


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
        expected = references[self.application][self.version][sub_path][self.property]
        reference_index = self.test_config.pop("reference_index", None)
        if reference_index is not None:
            return expected[reference_index]
        return expected


class IntegrationTest(IntegrationTestBase):
    pass


def create_test(params):
    def do_test(self):
        for k, v in params.items():
            setattr(self, k, v)
        work_dir = self.work_dir(self.version, self.subdir)
        # TODO: os.path.join(workdir, self.filename) should not be necessary
        parser = parser_classes[self.application](
            work_dir=work_dir, stdout_file=os.path.join(work_dir, self.filename)
        )
        actual = getattr(parser, self.property)()
        actual_index = self.test_config.pop("actual_index", None)
        if actual_index is not None:
            actual = actual[actual_index]
        expected = self.get_reference_value()
        comparison = self.test_config.pop("comparison")
        getattr(self, comparison)(actual, expected, **self.test_config)
    return do_test


for application, all_versions in manifest["applications"].items():
    for version, fixtures in all_versions.items():
        for fixture in fixtures:
            for test in fixture["tests"]:
                test_config = get_test_config(test)
                test_property = test_config.pop("property")
                test_method = create_test({
                    "application": application,
                    "version": version,
                    "subdir": fixture["subdir"],
                    "filename": fixture["filename"],
                    "property": test_property,
                    "test_config": test_config,
                })
                test_name = f"test_{application}_{version}_{test_property}"
                test_method.__name__ = test_name
                setattr(IntegrationTest, test_name, test_method)