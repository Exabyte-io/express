import copy
import functools
import operator
import os
import unittest
from typing import List, Dict, Union

from express.parsers.apps.espresso.parser import EspressoLegacyParser
from express.parsers.apps.nwchem.parser import NwchemParser
from express.parsers.apps.vasp.parser import VaspParser
from tests.integration import IntegrationTestBase
import tests


def testApplicationParsers(self):
    if self.application_name:
        versions = self.manifest['applications'][self.application_name]
        for version, fixtures in versions.items():

            # Loop over fixtuers
            for fixture in fixtures:
                work_dir = os.path.join(self.rootDir, 'fixtures', self.application_name, version, fixture['path'])
                stdout_file = fixture['filename']
                assert os.path.exists(os.path.join(work_dir, stdout_file))
                # Loop over tests
                for property_name, assertion, places in map(generate_test_config, fixture['tests']):

                    with self.subTest(version=version,
                                      property=property_name,
                                      fixture=os.path.join(fixture['path'], stdout_file)):
                        parser = self.parser(work_dir = work_dir, stdout_file = stdout_file)
                        result_fun = getattr(parser, property_name)
                        result = result_fun()
                        print(result)

                    # for test_property, test_settings in self.manifest['tests'].items():
                    #     default_comparison_operator = self.__getattribute__(
                    #         test_settings.get('comparison', 'assertDeepAlmostEqual'))
                    #     default_precision = test_settings.get("places", 2)


class EspressoTestBase(IntegrationTestBase):
    application_name = "espresso"
    parser = EspressoLegacyParser
    testEspressoParser = testApplicationParsers

class VaspTestBase(IntegrationTestBase):
    application_name = "vasp"
    parser = VaspParser
    testVaspParser = testApplicationParsers


class NWChemTestBase(IntegrationTestBase):
    application_name = "nwchem"
    parser = NwchemParser
    testNWChemParser = testApplicationParsers


def get_application_config(cls):
    config = {}
    application_name = cls.application_name
    if application_name:
        for version_config in tests.get_test_manifest()['applications'][application_name]:
            config.update(version_config)
    return config


def create_test(cls,
                version: str,
                work_dir: str,
                stdout_file: str,
                properties_to_test: List[Union[str, Dict[str, str]]]):
    for test in properties_to_test:
        property_to_test, comparison, places = generate_test_config(test)
        fixture_dir = os.path.join(os.path.dirname(tests.__file__), "fixtures", cls.application_name, version, work_dir)

        def fun(self):
            parser = self.parser(work_dir=fixture_dir, stdout_file=stdout_file)
            result_fun = operator.attrgetter(property_to_test)(parser)

        fun_name = f"test_{cls.application_name}_{version}_{property_to_test}".replace(".", "-")

        setattr(cls, fun_name, copy.deepcopy(fun))


@functools.singledispatch
def generate_test_config(test, verbose=True):
    raise ValueError("Test type must be a member of Union[str, Dict]")


@generate_test_config.register
def _(test: dict):
    test_config = test
    property_to_test = test['name']
    default_test_config = tests.get_test_manifest()['tests'][property_to_test]
    comparison = test_config.get("comparison", default_test_config.get("comparison", "assertDeepAlmostEqual"))
    places = test_config.get("places", default_test_config.get("places", 2))
    return property_to_test, comparison, places


@generate_test_config.register
def _(test: str):
    property_to_test = test
    default_test_config = tests.get_test_manifest()['tests'][property_to_test]
    comparison = default_test_config.get("comparison", "assertDeepAlmostEqual")
    places = default_test_config.get("places", 2)
    return property_to_test, comparison, places

#
# for cls in (NWChemTestBase, EspressoTestBase, VaspTestBase):
#     application_config = get_application_config(cls)
#
#     for version, configs in application_config.items():
#         for config in configs:
#             work_dir = config['path']
#             stdout_file = config['filename']
#             properties_to_test = config['tests']
#             create_test(cls, version, work_dir, stdout_file, properties_to_test)
