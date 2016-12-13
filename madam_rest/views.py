from flask import jsonify, url_for

from madam_rest import app, asset_storage


@app.route('/assets/')
def assets_retrieve():
    assets = [asset_key for asset_key in asset_storage]
    return jsonify({
        "data": assets,
        "meta": {
            "count": len(assets)
        }
    })


@app.route('/assets/<asset_key>')
def asset_retrieve(asset_key):
    asset = asset_storage[asset_key]
    return jsonify({
        "links": {
            "self": url_for(asset_retrieve, asset_key=asset_key)
        },
        "meta": {}  # TODO: _mutable(asset.metadata)
    })
