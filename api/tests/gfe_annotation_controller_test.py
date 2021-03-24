from api.tests import BaseTestCase
import json


class TestAnnotation(BaseTestCase):

    def test_annotation(self):
        """Test case for annotate_get
        """
        locus = 'HLA-DQB1'
        gene = False
        response = self.client.post(
            f'gfe/seq/annotate/{gene}/{locus}',
            data=json.dumps(dict(sequence="AGAACGGGAAGGAGACGCTGCAGCGCACGGGTACCAGGGGCCACGGGGCGCCTCCCTGAT")),
            content_type='application/json'
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
