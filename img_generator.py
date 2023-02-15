import requests
import yaml
import random
import json
from utils import get_config, reload_config

from prompt_generator import p_gen

class ImgGenerator:
    def __init__(self, url="http://127.0.0.1:7860"):
        self.url = f"{url}/sdapi/v1"
    
    def get_models(self):
        r = requests.get(f"{self.url}/sd-models")
        assert r.status_code == 200
        return json.loads(r.text)
    
    def set_model(self, info):
        r = requests.post(f"{self.url}/set-model", json={"info": info})
        assert r.status_code == 200

    def set_random_model(self):
        models = self.get_models()
        idx = random.randint(0, len(models)-1)
        name = models[idx]["model_name"]
        self.set_model(name)

        args = {"model_name": name} 

        return args
    
    def get_img(self, args):
        r = requests.post(f"{self.url}/txt2img", json=args)
        assert r.status_code == 200
        imgs = r.json()["images"]
        return imgs[0]

    def get_random_img(self):
        overwrite_args = self.set_random_model()
        args = get_config()["default_args"]

        for k in overwrite_args:
            args[k] = overwrite_args[k]

        args["prompt"] = p_gen.get_random_prompt()

        return self.get_img(args), args

if __name__ == "__main__":
    img = ImgGenerator()
    img.get_random_img()