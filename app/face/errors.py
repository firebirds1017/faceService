from flask import jsonify
from . import face


@face.app_errorhandler(404)
def page_not_found(e):
    """
    deal 404  error
    """

    return jsonify({'message': 'page not found', 'code': '40004', "errorinfo": True}), 404


@face.app_errorhandler(500)
def server_internal_error(e):
    """
    deal server internal error
    :param e:
    :return:
    """

    return jsonify({'message': 'server internal error', 'code': '50000', "errorinfo": True}), 500

