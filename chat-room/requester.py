from commons import properties

import requests
import json

class Requester:
    def __init__(self, url):
        self.url = url

    def call(self, headers=None):
        r = requests.get(self.url, headers=headers)
        return r.text



