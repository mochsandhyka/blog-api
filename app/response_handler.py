from http import HTTPStatus
from flask import make_response,jsonify

def ok(data):
    return make_response(jsonify(data)),HTTPStatus.OK.value

def created(data):
    return make_response(jsonify(data)),HTTPStatus.CREATED.value

def bad_request(data):
    return make_response(jsonify(data)),HTTPStatus.BAD_REQUEST.value

def bad_gateway(data):
    return make_response(jsonify(data)),HTTPStatus.BAD_GATEWAY.value

def forbidden(data):
    return make_response(jsonify(data)),HTTPStatus.FORBIDDEN.value

def unautorized(data):
    return make_response(jsonify(data)),HTTPStatus.UNAUTHORIZED.value

def not_found(data):
    return make_response(jsonify(data)),HTTPStatus.NOT_FOUND.value