# Derek Peterson (derekmpeterson) Feb 7, 2013

from colormath.color_objects import RGBColor, HSVColor
import requests
import json
import time
import random
from datetime import datetime


class Hue:
    ip_address = None
    api_key = None

    def __init__(self, ip_address, api_key):
        self.ip_address = ip_address
        self.api_key = api_key

    def get_hex(self, hsv_h, hsv_s, hsv_v):
        hsv = HSVColor(hsv_h=hsv_h / 200, hsv_s=hsv_s / 254, hsv_v=hsv_v / 254)
        rgb = hsv.convert_to('rgb')
        return rgb.get_rgb_hex()

    def toggle_light(self, light, on):
        params = {
            "on": on,
        }
        params = json.dumps(params)
        self.send_data(light, params)

    def set_brightness(self, light, bri):
        params = json.dumps({"bri": bri})
        self.send_data(light, params)

    def get_lights(self):
        return self.get_hub_info()['lights']

    def get_hub_info(self):
        return self.api_call("")

    def get_light(self, light):
        state = self.api_call("lights/%d/" % light)['state']
        state['hex_color'] = self.get_hex(
            float(state['hue']),
            float(state['sat']),
            float(state['bri']))

        return state

    def set_light(self, light, hex, brightness=0, on=True):
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

        self.send_data(light, params)

    def api_call(self, endpoint, data=None):
        try:
            if data is None:
                r = requests.get(
                    ("http://%s/api/%s/%s"
                     % (self.ip_address, self.api_key, endpoint)),
                    timeout=1.0)
            else:
                r = requests.put(
                    ("http://%s/api/%s/%s"
                     % (self.ip_address, self.api_key, endpoint)),
                    data=data,
                    timeout=1.0)
            return r.json()
        except requests.exceptions.Timeout:
            print "API timeout: %s" % datetime.utcnow()
            return None

    def send_data(self, light, params):
        self.api_call("lights/%d/state" % (light), params)
