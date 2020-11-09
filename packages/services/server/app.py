from flask import Flask, request
from flask import jsonify
from packages.services.server.auth_handler import AuthHandler, auth_require
from packages.services.server.services import Services, SecurityEvent
import os
import time

app = Flask(__name__)
services = Services()


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
        services.security.send_event(SecurityEvent.LOGIN_FAIL_ATTEMPT)
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
# @auth_require
def door():
    services.door()
    return jsonify({
        "message": "door unlocked"
    })

@app.route('/system/led', endpoint='led')
# @auth_require
def led():
    color = request.args.get('color')
    if color == 'red':
        services.led_strip.turn_red()
    elif color == 'green':
        services.led_strip.turn_green()
    elif color == 'blue':
        services.led_strip.turn_blue()
    elif color == 'off':
        services.led_strip.turn_off()

    return jsonify({
        "message": "led color set successfuly."
    })

@app.route('/system/autolight', endpoint='autolight')
# @auth_require
def autolight():
    state = request.args.get('state')
    if state == 'on':
        services.is_auto_light = True
        return jsonify({
            'message': 'autolight on'
        })
    elif state == 'off':
        services.is_auto_light = False
        return jsonify({
            'message': 'autoligh off'
        })
    else:
        return jsonify({
            "message": "state parameter should be on or off only"
        }), 406


@app.route('/system/lamp', endpoint='lamp')
# @auth_require
def lamp():
    state = request.args.get('state')
    if state == 'switch':
        services.lamp(is_on=(not services.hardware.is_lamp_on))
        return jsonify({
            'message': 'lamp switched'
        })
    elif state == 'on':
        services.lamp(is_on=True)
        return jsonify({
            'message': 'lamp turned on'
        })
    elif state == 'off':
        services.lamp(is_on=False)
        return jsonify({
            'message': 'lamp turned off'
        })
    else:
        return jsonify({
            "message": "state parameter should be switch, on or off only"
        }), 406

@app.route('/system/lamp/state', endpoint='lamp_state')
# @auth_require
def lamp_state():
    if services.hardware.is_lamp_on:
        return "1"
    else:
        return "0"

@app.route('/system/security', endpoint='security')
# @auth_require
def security():
    state = request.args.get('state')
    if state == 'on':
        services.security.send_event(SecurityEvent.SECURITY_ON)
        return jsonify({
            'message': 'security on'
        })
    elif state == 'off':
        services.security.send_event(SecurityEvent.SECURITY_OFF)
        return jsonify({
            'message': 'security off'
        })
    else:
        return jsonify({
            "message": "state parameter should be on or off only"
        }), 406

### ---- disposable system actions
@app.route('/ota/door/<token>')
def disposable_door(token):
    if AuthHandler().validate(token):
        services.door()
        return jsonify({
            "message": "door unlocked"
        })
    else:
        services.security.send_event(SecurityEvent.BAD_TOKEN_ATTEMPT)
        return jsonify({
            'message': 'access denied'
        }), 401

@app.route('/ota/lamp/<token>')
def disposable_lamp(token):
    if AuthHandler().validate(token):
        services.lamp(is_on=(not services.is_lamp_on()))
        return jsonify({
            'message': 'lamp switched'
        })
    else:
        services.security.send_event(SecurityEvent.BAD_TOKEN_ATTEMPT)
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
    services.push.send_message('System Status', 'System is up and run successfully')
    app.run(debug=False, port=80, host='0.0.0.0')