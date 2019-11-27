from swagger_server.tests import BaseTestCase


class TestAllReleasesController(BaseTestCase):
    """all releases controller test"""
    def test_all_releasess(self):
        """Test case for all releases
        """
        response = self.client.open(
            '/gfe/locus/3.31.0',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
