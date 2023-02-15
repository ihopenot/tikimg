import yaml
import random

config = yaml.safe_load(open("config.yaml", "r", encoding='utf8').read())
print(config)

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
    
tag_database = TagDatabase("tags.yaml", config)

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

p_gen = PromptGenerator(tag_database)

if __name__ == "__main__":
    for i in range(20):
        print(p_gen.get_random_prompt())