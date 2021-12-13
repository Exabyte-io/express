import functools
import os
import yaml
import unittest
import numpy as np


def for_all_versions(version_map: dict, runtype_map: dict):
    """
    Given a dict of versions and runtypes, this decorator will automatically create subtests, allowing the same test to
    be run over multiple versions of the same software, and even multiple runtypes. This is useful, for example, if we
    want to make sure that all versions of a particular DFT software correctly extract the fermi energy, regardless of
    if it's an SCF optimization, geometry relaxation, molecular dynamics run, etc.

    Note:
        Technically, this is a decoratory factory, which takes in a few arguments and returns a decorator.

    Args:
        version_map (dict): Dictionary mapping version labels (keys) to some version-specific data (values). Keys are
                            used to name the test in the test report. Values are passed to the test function.
        runtype_map (dict): Dictioanry mapping runtype labels (keys) to some runtype-specific data (values). Keys are
                            used to name the test in the test report. Values are passed to the test function.

    Example:
        The below example uses this decorator as a way of passing in the location of fixture directories for the
        different versions and runtypes. In principle, anything (or Nonetype) could have been passed here. This is
        very helpful, for example, if we want the test to behave differently for different versions or runtypes.

        >>> version_map = {"1.0": "v1.0_fixture_dir", "1.5": "v1.5_fixture_dir"}
        >>> runtype_map = {"scf": "scf_test_fixture_dir", "phonons": "phonon_test_fixture_dir"}
        >>> class MyTestClass(unittest.TestCase)
        ...     @for_all_versions(version_map, runtype_map)
        ...     def test_some_property(self, version, runtype):
        ...         ... # Test stuff here based on the version and runtype

        This will result in subtests being created under `test_some_property` with the following labels:
            - version_number="1.0", job_type="scf"
            - version_number="1.0", job_type="phonons"
            - version_number="1.5", job_type="scf"
            - version_number="1.5", job_type="phonons"

    Returns:
        Callable: A decorator function.
    """

    def decorator(test_function):
        @functools.wraps(test_function)
        def inner(self):
            for version_test_label, version in version_map.items():
                for job_test_label, jobtype in runtype_map.items():
                    with self.subTest(version_number=version_test_label, job_type=job_test_label):
                        test_function(self, version, jobtype)

        return inner

    return decorator


class TestBase(unittest.TestCase):
    """
    Base class for express tests.
    """

    def setUp(self):
        super(TestBase, self).setUp()
        self.rootDir = os.path.dirname(__file__)

    def tearDown(self):
        super(TestBase, self).tearDown()

    def getManifest(self):
        """
        Returns test's manifest.

        Returns:
            dict
        """
        with open(os.path.join(self.rootDir, "manifest.yaml")) as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)[self._testMethodName]

    def assertDeepAlmostEqual(self, expected, actual, *args, **kwargs):
        """
        Asserts that two complex structures have almost equal contents. Compares lists, dicts and tuples recursively.
        Checks numeric values using assertAlmostEqual() and checks all other values with assertEqual(). Accepts
        additional positional and keyword arguments and passes those intact to assertAlmostEqual().

        Notes:
            Based on: http://stackoverflow.com/a/23550280

        Args:
            expected (dict|list|tuple): expected complex object.
            actual (dict|list|tuple): actual complex object.
        """
        is_root = '__trace' not in kwargs
        trace = kwargs.pop('__trace', 'ROOT')
        try:
            if isinstance(expected, (int, float, complex)):
                self.assertAlmostEqual(expected, actual, *args, **kwargs)
            elif isinstance(expected, (str)):
                self.assertEqual(expected, actual)
            elif isinstance(expected, (list, tuple, np.ndarray)):
                self.assertEqual(len(expected), len(actual))
                for index in range(len(expected)):
                    v1, v2 = expected[index], actual[index]
                    self.assertDeepAlmostEqual(v1, v2, __trace=repr(index), *args, **kwargs)
            elif isinstance(expected, dict):
                self.assertEqual(set(expected), set(actual))
                for key in expected:
                    self.assertDeepAlmostEqual(expected[key], actual[key], __trace=repr(key), *args, **kwargs)
        except AssertionError as exc:
            exc.__dict__.setdefault('traces', []).append(trace)
            if is_root:
                trace = ' -> '.join(reversed(exc.traces))
                exc = AssertionError("%s\nTRACE: %s" % (str(exc), trace))
            raise exc
