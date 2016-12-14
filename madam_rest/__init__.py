import madam
from flask import Flask

app = Flask(__name__)
app.from_object('config')

asset_manager = madam.Madam()
asset_storage = madam.core.ShelveStorage(app.config['ASSET_STORAGE_PATH'])

from madam_rest import views
