import json


class CommonUtils:
    @staticmethod
    def decode_request(data):
        body_unicode = data.decode('utf-8')
        return json.loads(body_unicode)
