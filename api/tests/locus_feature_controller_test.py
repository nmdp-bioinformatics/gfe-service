from api.tests import BaseTestCase


class TestFeatureLocus(BaseTestCase):
    def test_feature(self):
        """Test case for features of locus
        """
        locus = 'HLA-DRA'
        response = self.client.open(
            f'/gfe/features/{locus}',
            method='GET',
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
