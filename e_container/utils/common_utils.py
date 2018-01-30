import json
import pickle
import ast


class CommonUtils:
    @staticmethod
    def decode_request(data):
        body_unicode = data.decode('utf-8').replace('\'', "\"")
        return json.loads(body_unicode)

    @staticmethod
    def eval_type(data):
        return ast.literal_eval(data)

    @staticmethod
    def save_to_file(data, file):
        with open(file, "wb") as f:
            for d in data:
                pickle.dump(d, f)

    @staticmethod
    def read_from_file(file):
        with open(file, "rb") as f:
            data = pickle.load(f)
        return data
