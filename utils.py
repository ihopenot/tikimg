import yaml
import random
from typing import Dict

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


class Prob:
    def __init__(self) -> None:
        pass

    def get(self):
        raise NotImplementedError


class NChoseProb(Prob):
    def __init__(self, v):
        if type(v) is list:
            self.values = v
        else:
            self.values = [v]
            
    def get(self):
        return random.choice(self.values)


def get_prob_result(probs: Dict[str, Prob]):
    ret = {}
    for k in probs:
        ret[k] = probs[k].get()
    print(ret)
    return ret


config = None
reload_config()