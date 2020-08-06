import uuid
import hashlib
from flask import jsonify, request
from singleton_decorator import singleton
from disposable_token import DisposableToken
from config import *

@singleton
class AuthHandler:
    __token = uuid.uuid4().hex
    __tokenSessions = []

    @property
    def token(self):
        return self.__token

    def validate_password(self, password):
        hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        return hashed_password == PASSWORD

    def renew_token(self):
        self.__token = uuid.uuid4().hex
        return self.token

    def make_disposable_key(self, disposeCount=1):
        newKey = DisposableToken(disposeCounts=disposeCount, value=uuid.uuid4().hex)
        self.__tokenSessions.append(newKey)
        return newKey

    def validate(self, token):
        if token == self.token:
            return True

        for index, item in enumerate(self.__tokenSessions):
            if item.value == token:
                if item.counts < 1:
                    self.__tokenSessions.remove(item)
                    return False

                self.__tokenSessions[index].counts -= 1
                return True

        return False


def auth_require(func):
    def check_token(*args, **kwargs):
        # Check to see if it's in their session
        if request.headers.get('x-token') != AuthHandler().token:
            return jsonify({
                "message": "Access denied"
            }), 401

        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)

    return check_token