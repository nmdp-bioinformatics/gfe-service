from api.tests import BaseTestCase


class TestKIRbyGFE(BaseTestCase):

    def test_kir_creation(self):
        """Test case for finding kir by gfe
        """

        gfe = "HLA-Aw1-1-7-20-10-32-7-1-1-1-6-1-5-3-5-1-1"
        response = self.client.open(
            f'/gfe/kir/{gfe}',
            method='GET',
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
