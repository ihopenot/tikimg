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
        if r.status_code != 200:
            raise Exception(f"return with code {r.status_code}")
        return json.loads(r.text)
    
    def set_model(self, info, isXL):
        conf_json = {"sd_model_checkpoint": info}
        if isXL:
            conf_json["sd_vae"] = get_config()["xl_vae"]
        else:
            conf_json["sd_vae"] = get_config()["default_vae"]
        r = requests.post(f"{self.url}/options", json=conf_json)
        if r.status_code != 200:
            raise Exception(f"return with code {r.status_code}")

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
        if r.status_code != 200:
            raise Exception(f"return with code {r.status_code}, resp {r.text}")
        imgs = r.json()["images"]
        return imgs[0]

    def get_random_img(self):
        while True:
            try:
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
            except Exception as e:
                print(e)

if __name__ == "__main__":
    img = ImgGenerator()
    img.get_random_img()