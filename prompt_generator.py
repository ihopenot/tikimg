import yaml
import random
from utils import *

class TagDatabase:
    def __init__(self, file, config) -> None:
        data = open(file, encoding='utf-8').read()
        r = yaml.safe_load(data)
        self.database = [ [[], config[i]["prob"]] for i in range(len(config))]
        for k in r:
            for i in range(len(config)):
                if k not in config[i]["types"]:
                    continue

                for v in r[k]:
                    for tag in v:
                        if "!|" in tag:
                            num, tag = tag.split('!|')
                            num = int(num)
                            self.database[i][0] += [tag] * num
                        else:
                            self.database[i][0] += [tag]
    
class PromptGenerator:
    def __init__(self, tag_database: TagDatabase = None) -> None:
        self.database = tag_database.database
    
    def get_random_prompt(self):
        tags = ["masterpiece", "best quality", "ultra-detailed", "illustration"]

        # girls numer
        if random.random() < 0.07:
            tags.append("2girls")
        else:
            tags.append("1girl")
        
        if self.database == None:
            return ", ".join(tags)

        for choice in self.database:
            if random.random() < choice[1]:
                tags.append(random.choice(choice[0]))
        
        return ", ".join(tags)

def get_random_prompt():
    return p_gen.get_random_prompt()

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