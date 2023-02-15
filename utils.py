import yaml

def load_yaml(filename):
    return yaml.safe_load(open(filename, "r", encoding='utf8'))

def save_yaml(filename, obj):
    return yaml.safe_dump(obj, open(filename, "w", encoding='utf8'), allow_unicode=True)

def get_config():
    return config

def reload_config():
    global config
    config = load_yaml("config.yaml")

config = None
reload_config()