import requests
import random
import json

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
        if not "Orange" in name and not "anything" in name and not "Counterfeit" in name and not "pastelmix" in name:
            pass

        return args
    
    def get_img(self, args):
        r = requests.post(f"{self.url}/txt2img", json=args)
        assert r.status_code == 200
        imgs = r.json()["images"]
        return imgs[0]

    def get_random_img(self):
        overwrite_args = self.set_random_model()
        args = {
            "prompt": "",
            "negative_prompt": "nsfw, (worst quality, low quality:1.4), signature, watermark, username",
            "height": 768,
            "width": 512,
            'seed': -1, 
            'subseed': -1, 
            'sampler_name': 'DPM++ SDE Karras', 
            'steps': 20, 
            'cfg_scale': 8, 
            'denoising_strength': 0.6, 
            'enable_hr': True, 
            'hr_scale': 2, 
            'hr_upscaler': 'Latent (nearest-exact)', 
            'hr_second_pass_steps': 20, 
        }

        for k in overwrite_args:
            args[k] = overwrite_args[k]

        args["prompt"] = p_gen.get_random_prompt()

        return self.get_img(args), args
