from datetime import datetime
from fractions import Fraction

from flask import Blueprint, jsonify, send_file, url_for
from frozendict import frozendict

from madam_rest import asset_storage


api = Blueprint('v1', __name__, url_prefix='/v1')


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


@api.route('/assets/')
def assets_retrieve():
    assets = [asset_key for asset_key in asset_storage]
    return jsonify({
        "data": assets,
        "meta": {
            "count": len(assets)
        }
    })


@api.route('/assets/<asset_key>/')
def asset_retrieve(asset_key):
    asset = asset_storage[asset_key]
    return jsonify({
        "links": {
            "self": url_for(asset_retrieve, asset_key=asset_key)
        },
        "meta": _serializable(asset.metadata)
    })
