
from swagger_server.tests import BaseTestCase
import json

class TestTyping(BaseTestCase):

    def test_typing(self):
        """Test case for typing
        """
        locus = 'HLA-DQB1'
        response = self.client.post(
            f'/gfe/typing/hla/{locus}',
            data=json.dumps(dict(sequence="AGAACGGGAAGGAGACGCTGCAGCGCACGGGTACCAGGGGCCACGGGGCGCCTCCCTGAT")),
            content_type='application/json'
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
