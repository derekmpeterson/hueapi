from colormath.color_objects import RGBColor, HSVColor
import requests
import json
import time
import random
from datetime import datetime

# The IP address of your Hue hub
IP_ADDRESS = ""
# The key given you when registering as a new app to your hub
API_KEY = ""

def get_hex(hsv_h, hsv_s, hsv_v):
    hsv = HSVColor(hsv_h=hsv_h/200, hsv_s=hsv_s/254, hsv_v=hsv_v/254)
    rgb = hsv.convert_to('rgb')
    return rgb.get_rgb_hex()

def change_color(light, hex, brightness=0, on=True):
    rgb = RGBColor()
    rgb.set_from_rgb_hex(hex)

    color = rgb.convert_to('hsv')

    bri = int(color.hsv_v * 254)
    hue = int(color.hsv_h * 200)
    sat = int(color.hsv_s * 254)

    if brightness > 0:
        bri = brightness

    params = {
        "on": on,
        "bri": bri,
        "hue": hue,
        "sat": sat,
    }
    params = json.dumps(params)

    send_data(light, params)

def light_switch(light, on):
    params = {
        "on": on,
    }
    params = json.dumps(params)
    send_data(light,params)

def send_data(light, params):
    try:
        r = requests.put(
            "http://%s/api/%s/lights/%d/state" % (IP_ADDRESS, API_KEY, light),
            params,
            timeout = 0.50)
    except requests.exceptions.Timeout:
        print "Timeout updating light. %s" % datetime.utcnow()

def brightness(light, bri):
    params = json.dumps({"bri": bri})
    send_data(light, params)

def lights():
    return hub_info()['lights']

def hub_info():
    try:
        r = requests.get(
            "http://%s/api/%s" % (IP_ADDRESS, API_KEY),
            timeout = 0.50)
    except requests.exceptions.Timeout:
        print "Timeout getting light info. %s" % datetime.utcnow()
    info = r.json
    return info

def state(light):
    try:
        r = requests.get(
            "http://%s/api/%s/lights/%d/" % (IP_ADDRESS, API_KEY, light),
            timeout = 0.50)
    except requests.exceptions.Timeout:
        print "Timeout getting light info. %s" % datetime.utcnow()
    state = r.json['state']
    state['hex_color'] = get_hex(float(state['hue']), float(state['sat']), float(state['bri']))

    return state