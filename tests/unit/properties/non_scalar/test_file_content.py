from tests.unit import UnitTestBase
from express.properties.non_scalar.file_content import FileContent
from tests.fixtures.data import FILE_CONTENT


class FileContentTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().setUp()

    def test_file_content(self):
        name = "file_content"
        parser = None
        args = []
        kwargs = {
            "basename": "my_parity_plot.png",
            "filetype": "image",
            "upload_dir": "/cluster-001-share/groups/exaorg-uy3burw0/exaorg-uy3burw0-default/job-python-python-ml-train-organization-jJ67E6JQ6DLyF9Q8z/",  # noqa: E501
            "object_storage_data": {
                "CONTAINER": "vagrant-cluster-001",
                "NAME": "",
                "PROVIDER": "aws",
                "REGION": "us-east-1",
            },
        }
        property_ = FileContent(name, parser, *args, **kwargs)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), FILE_CONTENT)
