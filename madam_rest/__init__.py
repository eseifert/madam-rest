from flask import Flask
from madam import Madam

app = Flask(__name__)
app.from_object('config')

asset_manager = Madam()
asset_storage = app.config['ASSET_STORAGE']

from madam_rest import views
