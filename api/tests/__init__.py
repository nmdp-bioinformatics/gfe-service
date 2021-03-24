import logging

import connexion
from flask_testing import TestCase
from api.encoder import JSONEncoder


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../../spec/')
        app.app.json_encoder = JSONEncoder
        app.add_api('gfe_service_api_spec.yaml')
        return app.app
