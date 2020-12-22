import json


def get_config():
    path = 'nb_helper_config_empty.json'
    path = '../docker/helper_dummy/nb_helper_config_empty.json'
    with open(path, 'r') as cfg:
        return json.load(cfg)
