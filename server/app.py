from flask import Flask, request
from flask import jsonify
from auth_handler import AuthHandler, auth_require
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "message": "page not found."
    }), 404


### ---- authentications
@app.route('/auth/token', methods=['POST'])
def generateToken():
    request_body = request.get_json()
    if request_body != None and AuthHandler().validate_password(request_body["password"]):
        return jsonify({
            "token": AuthHandler().renew_token()
        })
    else:
        return jsonify({
            'message': 'password did not match'
        }), 401

@app.route('/auth/key', methods=['POST'], endpoint='makeKey')
@auth_require
def makeKey():
    request_body = request.get_json()
    dispose_count = 1
    if request_body != None:
        dispose_count = int(request_body["count"])

    one_time_token = AuthHandler().make_disposable_key(dispose_count).value

    return jsonify({
        'token': one_time_token,
        'links': [
            'http://192.168.1.80/ota/door/{}'.format(one_time_token),
            'http://192.168.1.80/ota/lamp/{}'.format(one_time_token)
        ]
    })

@app.route('/auth/test', endpoint='test')
@auth_require
def test():
    return jsonify({
        "foo": "foo"
    })


### ---- system actions
@app.route('/system/door', endpoint='door')
@auth_require
def door():
    os.system('hws door')
    return jsonify({
        "message": "door unlocked"
    })

@app.route('/system/lamp', endpoint='lamp')
@auth_require
def lamp():
    state = request.args.get('state')
    if state == 'switch':
        os.system('hws lampSwitch')
        return jsonify({
            'message': 'lamp switched'
        })
    elif state == 'on':
        os.system('hws lampOn')
        return jsonify({
            'message': 'lamp turned on'
        })
    elif state == 'off':
        os.system('hws lampOff')
        return jsonify({
            'message': 'lamp turned off'
        })
    else:
        return jsonify({
            "message": "state parameter should be switch, on or off only"
        }), 406


### ---- disposable system actions
@app.route('/ota/door/<token>')
def disposable_door(token):
    if AuthHandler().validate(token):
        os.system('hws door')
        return jsonify({
            "message": "door unlocked"
        })
    else:
        return jsonify({
            'message': 'access denied'
        }), 401

@app.route('/ota/lamp/<token>')
def disposable_lamp(token):
    if AuthHandler().validate(token):
        os.system('hws lampSwitch')
        return jsonify({
            'message': 'lamp switched'
        })
    else:
        return jsonify({
            'message': 'access denied'
        }), 401


### ---- errors
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        'message': 'page not exists'
    }), 404

if __name__ == "__main__":
    app.run(debug=False, port=80, host='0.0.0.0')