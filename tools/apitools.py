from jwtcreate import *
from mongoDB import *
from flask import render_template, jsonify


def token_check(collection, username, token_user):
    if usertoken_check(collection, username, token_user) == None:
        return render_template('error.html', error_msg='使用者未登入！[MongoDBtokenError]')
    print('usertoken_check succeeded')
    if verifyJWT_user(username, token_user) == False:
        return render_template('error.html', error_msg='使用者未登入！[SessionTokenError]')
    return jsonify('token_fhir')
