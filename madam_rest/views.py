from datetime import datetime
from flask import jsonify, url_for
from fractions import Fraction
from frozendict import frozendict

from madam_rest import app, asset_storage


def _serializable(value):
    """
    Utility function to convert data structures with immutable types to
    mutable, serializable data structures.
    :param value: data structure with immutable types
    :return: mutable, serializable data structure
    """
    if isinstance(value, (tuple, set, frozenset)):
        return [_serializable(v) for v in value]
    elif isinstance(value, frozendict):
        return {k: _serializable(v) for k, v in value.items()}
    elif isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, Fraction):
        return float(value)
    return value


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
        "meta": _serializable(asset.metadata)
    })
