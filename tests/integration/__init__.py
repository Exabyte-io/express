import os
import functools

from typing import Union

from tests import TestBase


class IntegrationTestBase(TestBase):
    """
    Base class for express integration tests.
    """

    def setUp(self):
        super(IntegrationTestBase, self).setUp()

    def tearDown(self):
        super(IntegrationTestBase, self).setUp()

    def work_dir(self, version: str, subdir: str):
        return os.path.join(
            self.rootDir, "fixtures", self.application_name, version, subdir
        )

    def get_test_config(self, test_config: Union[str, dict]) -> dict:
        """If specified at the individual test level, construct a granular test
        configuration, otherwise provide a default test configuration from the
        manifest.yaml.
        """
        places = 2
        if isinstance(test_config, str):
            return {
                "property": test_config,
                "places": places,
                **self.manifest["tests"][test_config],
            }
        return {
            "property": test_config.pop("name"),
            "places": places,
            **self.manifest["tests"][test_config["name"]],
            **test_config,
        }

    def get_reference_value(self, version: str, path: str, property: str):
        sub_path = path.split("/")[-1]
        return self.references[version][sub_path][property]

    def testApplicationParsers(self):
        if getattr(self, "application_name", None) not in self.manifest["applications"]:
            return
        all_versions = self.manifest["applications"][self.application_name]
        for version, fixtures in all_versions.items():
            for fixture in fixtures:
                for test in fixture["tests"]:
                    test_config = self.get_test_config(test)
                    property = test_config.pop("property")
                    with self.subTest(
                        version=version,
                        property=property,
                        fixture=fixture["path"],
                    ):
                        parser = self.parser(
                            work_dir=self.work_dir(version, fixture["path"]),
                            stdout_file=fixture["filename"]
                        )
                        actual = getattr(parser, property)()
                        expected = self.get_reference_value(version, fixture["path"], property)
                        comparison = test_config.pop("comparison")
                        getattr(self, comparison)(actual, expected, **test_config)


from express.parsers.apps.espresso.parser import EspressoLegacyParser, EspressoParser
from express.parsers.apps.vasp.parser import VaspParser
from express.parsers.apps.nwchem.parser import NwchemParser

from tests.fixtures.vasp import references as vasp_references
from tests.fixtures.espresso import references as espresso_references
from tests.fixtures.nwchem import references as nwchem_references

class LegacyEspressoTest(IntegrationTestBase):
    application_name = "espresso"
    parser = EspressoLegacyParser
    references = espresso_references.REFERENCE_VALUES

class VaspTestBase(IntegrationTestBase):
    application_name = "vasp"
    parser = VaspParser
    references = vasp_references.REFERENCE_VALUES


class NWChemTestBase(IntegrationTestBase):
    application_name = "nwchem"
    parser = NwchemParser
    references = nwchem_references.REFERENCE_VALUES
