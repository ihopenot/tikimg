import yaml
import random
from typing import Dict, List
from utils import *

class Prompt_Entry:
    def __init__(self, tags, prob, types, categories) -> None:
        assert categories != None
        self.prob = prob
        self.tags = []
        for type in types:
            self.tags += tags[type]
        self.categories = categories
    
    def get(self):
        if random.random() < self.prob:
            return [random.choice(self.tags)]
        else:
            return []

class TagDatabase:
    def __init__(self, file, config) -> None:
        data = open(file, encoding='utf-8').read()
        r = yaml.safe_load(data)
        self.tags = {k: [] for k in r}
        for tagtype in r:
            for tag in r[tagtype]:
                for tagname in tag:
                    tagname = tagname.replace("\\\\", "\\")
                    if "!|" in tagname:
                        num, tagname = tagname.split('!|')
                        num = int(num)
                        self.tags[tagtype] += [tagname] * num
                    else:
                        self.tags[tagtype] += [tagname]

        self.prompt_entrys = [ self.create_prompt_entry(conf["prob"], conf["types"], conf["categories"]) for conf in config]
    
    def create_prompt_entry(self, prob, types, categories):
        return Prompt_Entry(self.tags, prob, types, categories)
    
class PromptGenerator:
    def __init__(self, tag_database: TagDatabase = None) -> None:
        self.database = tag_database
    
    def get_random_prompt(self, custom=None):
        tags : Dict[str, List] = {
            "quality": ["masterpiece", "best quality", "ultra-detailed", "illustration"],
            "total": [],
            "style": [],
            "character": [],
            "series": [],
            "artists": [],
            "general": [],
        }

        # girls number
        if random.random() < 0.07:
            tags["total"].append("2girls")
        else:
            tags["total"].append("1girls")
        
        if self.database == None:
            return tags

        for entry in self.database.prompt_entrys:
            tags[entry.categories] += entry.get()
        
        if custom is None:
            return tags
        
        for conf in custom:
            entry = self.database.create_prompt_entry(conf["prob"], conf["types"], conf["categories"])
            tags[entry.categories] += entry.get()
        
        return tags

def get_random_prompt(format, custom):
    ret = []
    tags = p_gen.get_random_prompt(custom)
    order = format.split('/')
    for i in order:
        ret += tags[i]
    return ", ".join(ret)

def rebuild_prompt_generator():
    global p_gen
    config = get_config()["tags_config"]
    tag_database = TagDatabase("tags.yaml", config)
    p_gen = PromptGenerator(tag_database)

add_reload_config_hook(rebuild_prompt_generator)

p_gen = None
rebuild_prompt_generator()

if __name__ == "__main__":
    for i in range(20):
        print(get_random_prompt())