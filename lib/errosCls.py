import flask
from lib.settings import application


class HttpErrors(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


# обработчик ошибок
@application.errorhandler(HttpErrors)
def http_err_handle(error):
    response = flask.jsonify({'message': error.message})
    response.status_code = error.status_code

    return response