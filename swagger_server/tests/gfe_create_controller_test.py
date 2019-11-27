
from swagger_server.tests import BaseTestCase
import json


class TestGfeCreation(BaseTestCase):

    def test_gfe_creation(self):
        """Test case for gfe_creation
        """
        locus = 'HLA-DQB1'
        imgt_version = '3.31.0'
        response = self.client.open(
            f'/gfe/create/{locus}/{imgt_version}',
            method='PUT',
            data=json.dumps(dict(sequence="AGAACGGGAAGGAGACGCTGCAGCGCACGGGTACCAGGGGCCACGGGGCGCCTCCCTGAT")),
            content_type='application/json'
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
