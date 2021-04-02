#!/usr/bin/env python3

import connexion
from flask import redirect
from api import encoder

app = connexion.App(__name__, specification_dir='spec/')
app.app.json_encoder = encoder.JSONEncoder
app.app.config['MAX_CONTENT_LENGTH'] = 1600 * 1024 * 1024

api = app.add_api('gfe_service_api_spec.yaml', arguments={'title': 'GFE Services'})


@app.route("/")
def index():
    return redirect(api.base_path + "/ui")


if __name__ == '__main__':
    app.run(port=8080, debug=True)  # TODO Set to False when ready for prod
