import yaml

def load_yaml(filename):
    return yaml.safe_load(open(filename, "r", encoding='utf8'))

def save_yaml(filename, obj):
    return yaml.safe_dump(obj, open(filename, "w", encoding='utf8'), allow_unicode=True)

def get_config():
    return config

reload_config_hooks = []
def reload_config():
    global config
    try:
        config = load_yaml("config/config.yaml")
    except FileNotFoundError:
        open("config/config.yaml", "w").write(open("config.default.yaml", "r").read())
        config = load_yaml("config/config.yaml")

    for hook in reload_config_hooks:
        hook()

def add_reload_config_hook(f):
    reload_config_hooks.append(f)

config = None
reload_config()