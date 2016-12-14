import madam
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

asset_manager = madam.Madam()
asset_storage = madam.core.ShelveStorage(app.config['ASSET_STORAGE_PATH'])

from madam_rest.api_v1 import api
app.register_blueprint(api)
