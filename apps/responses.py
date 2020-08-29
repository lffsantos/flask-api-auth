from flask import jsonify

from .messages import MSG_INVALID_DATA, MSG_DOES_NOT_EXIST, MSG_EXCEPTION
from .messages import MSG_ALREADY_EXISTS


def resp_data_invalid(resource, errors, msg=MSG_INVALID_DATA):
    """
    Responses 422 Unprocessable Entity
    :param resource: str
    :param errors: sict
    :param msg: str
    :return: dict
    """

    if not isinstance(resource, str):
        raise ValueError('O recurso precisa ser uma string.')

    resp = jsonify({
        'resource': resource,
        'message': msg,
        'errors': errors,
    })

    resp.status_code = 422

    return resp


def resp_exception(resource, description='', msg=MSG_EXCEPTION):
    """
    Responses 500
    """

    if not isinstance(resource, str):
        raise ValueError('O recurso precisa ser uma string.')

    resp = jsonify({
        'resource': resource,
        'message': msg,
        'description': description
    })

    resp.status_code = 500

    return resp


def resp_does_not_exist(resource, description):
    """
    Responses 404 Not Found
    """

    if not isinstance(resource, str):
        raise ValueError('O recurso precisa ser uma string.')

    resp = jsonify({
        'resource': resource,
        'message': MSG_DOES_NOT_EXIST.format(description),
    })

    resp.status_code = 404

    return resp


def resp_already_exists(resource, description):
    """
    Responses 400
    """

    if not isinstance(resource, str):
        raise ValueError('O recurso precisa ser uma string.')

    resp = jsonify({
        'resource': resource,
        'message': MSG_ALREADY_EXISTS.format(description),
    })

    resp.status_code = 400

    return resp


def resp_ok(resource, message, data=None, **extras):
    """
    Responses 200
    """

    response = {'status': 200, 'message': message, 'resource': resource}

    if data:
        response['data'] = data

    response.update(extras)

    resp = jsonify(response)

    resp.status_code = 200

    return resp
