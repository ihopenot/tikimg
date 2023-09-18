import requests
import random
import json
from utils import *

from prompt_generator import *

class ImgGenerator:
    def __init__(self, url="http://127.0.0.1:7860"):
        self.url = f"{url}/sdapi/v1"
    
    def get_models(self):
        r = requests.get(f"{self.url}/sd-models")
        assert r.status_code == 200
        return json.loads(r.text)
    
    def set_model(self, info, isXL):
        conf_json = {"sd_model_checkpoint": info}
        if isXL:
            conf_json["sd_vae"] = get_config()["xl_vae"]
        else:
            conf_json["sd_vae"] = get_config()["default_vae"]
        r = requests.post(f"{self.url}/options", json=conf_json)
        assert r.status_code == 200

    def set_random_model(self):
        models = self.get_models()
        idx = random.randint(0, len(models)-1)
        name = models[idx]["title"]
        isXL = models[idx]["model_name"] in get_config()["sdxl_models"]
        self.set_model(name, isXL)

        args = {"sd_model_checkpoint": name} 

        return args, isXL
    
    def get_img(self, args):
        r = requests.post(f"{self.url}/txt2img", json=args)
        assert r.status_code == 200
        imgs = r.json()["images"]
        return imgs[0]

    def get_random_img(self):
        reload_config()
        overwrite_args, isXL = self.set_random_model()
        if isXL:
            args = get_config()["xl_default_args"]
        else:
            args = get_config()["default_args"]

        for k in overwrite_args:
            args[k] = overwrite_args[k]

        args["prompt"] = get_random_prompt()

        return self.get_img(args), args

if __name__ == "__main__":
    img = ImgGenerator()
    img.get_random_img()