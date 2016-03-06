from flask import jsonify


def bad_request(message=None):
    response = jsonify({'error': 'invalid domain', 'message': message})
    response.status_code = 400
    return response
