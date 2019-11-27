from swagger_server.tests import BaseTestCase


class TestReleasesByLocus(BaseTestCase):
    def test_relaeases_by_locus(self):
        """Test case for releases by locus
        """
        locus = 'HLA-DRA'
        imgt_releases = '3.31.0'
        response = self.client.open(
            f'/gfe/{locus}/{imgt_releases}',
            method='GET',
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

