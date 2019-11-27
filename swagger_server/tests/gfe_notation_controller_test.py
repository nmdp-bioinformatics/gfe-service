from swagger_server.tests import BaseTestCase
import json


class TestNotation(BaseTestCase):
    """all releases controller test"""

    def test_notation(self):
        """Test case for notation
        """
        locus = 'HLA-DQB1'
        gene = False
        response = self.client.post(
            f'gfe/{gene}/{locus}',
            data=json.dumps(dict(sequence="AGAACGGGAAGGAGACGCTGCAGCGCACGGGTACCAGGGGCCACGGGGCGCCTCCCTGAT")),
            content_type='application/json'
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
