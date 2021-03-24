from api.tests import BaseTestCase


class TestAllReleasesController(BaseTestCase):
    """all releases controller test"""

    def test_all_releases(self):
        """Test case for all releases
        """
        response = self.client.open(
            '/gfe/locus/3.31.0',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
