import functools
from typing import List, Dict, Union

from express.parsers.apps.espresso.parser import EspressoParser
from express.parsers.apps.nwchem.parser import NwchemParser
from express.parsers.apps.vasp.parser import VaspParser
from tests.integration import IntegrationTestBase
from tests import get_test_manifest


class ApplicationTestsBase(IntegrationTestBase):
    application_name = None


class EspressoTestBase(ApplicationTestsBase):
    application_name = "espresso"
    parser = EspressoParser


class VaspTestBase(ApplicationTestsBase):
    application_name = "vasp"
    parser = VaspParser


class NWChemTestBase(ApplicationTestsBase):
    application_name = "nwchem"
    parser = NwchemParser


def get_application_config(cls):
    config = {}
    application_name = cls.application_name
    if application_name:
        for version_config in get_test_manifest()['applications'][application_name]:
            config.update(version_config)
    return config


def create_test(cls,
                version: str,
                work_dir: str,
                stdout_file: str,
                properties_to_test: List[Union[str, Dict[str, str]]]):
    for test in properties_to_test:
        property_to_test, comparison, places = generate_test_config(test)

        def fun(self):
            parser = self.parser(work_dir=work_dir, stdout_file = stdout_file)
            raise NotImplementedError

        fun_name = f"test_{cls.application_name}_{version}_{property_to_test}".replace(".", "-")
        setattr(cls, fun_name, fun)


@functools.singledispatch
def generate_test_config(test, verbose=True):
    raise ValueError("Test type must be a member of Union[str, Dict]")


@generate_test_config.register
def _(test: dict):
    test_config = test
    property_to_test = test['name']
    default_test_config = get_test_manifest()['tests'][property_to_test]
    comparison = test_config.get("comparison", default_test_config.get("comparison", "assertDeepAlmostEqual"))
    places = test_config.get("places", default_test_config.get("places", 2))
    return property_to_test, comparison, places


@generate_test_config.register
def _(test: str):
    property_to_test = test
    default_test_config = get_test_manifest()['tests'][property_to_test]
    comparison = default_test_config.get("comparison", "assertDeepAlmostEqual")
    places = default_test_config.get("places", 2)
    return property_to_test, comparison, places


for cls in (NWChemTestBase, EspressoTestBase, VaspTestBase):
    application_config = get_application_config(cls)

    for version, configs in application_config.items():
        for config in configs:
            work_dir = config['path']
            stdout_file = config['filename']
            properties_to_test = config['tests']
            create_test(cls, version, work_dir, stdout_file, properties_to_test)
