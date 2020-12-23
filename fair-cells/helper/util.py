import json


def get_config():
    with open('nb_helper_config.json', 'r') as cfg:
        return json.load(cfg)
