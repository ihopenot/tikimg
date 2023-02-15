import yaml
import random

config = [
    ([
    '构图.制图特效',
    '构图.图片类型',
    '构图.画风',
    ], 0.05),

    ([
    '构图.色彩',
    ], 0.07),

    ([
    '构图.视角',
    ], 0.1),

    ([
    '构图.背景',
    ], 0.07),

    ([
    '人文景观.位置.室内', 
    '人文景观.位置.室外', 
    '人文景观.位置.建筑物',
    '人文景观.城市', 
    ], 0.4),

    ([
    '自然景观.位置.室外',
    '自然景观.天空/气象',
    '自然景观.花卉',
    ], 0.4),

    ([
    '人物.摆位',
    ], 0.12),

    ([
    '人物.类型',
    ], 0.05),

    ([
    '人物.胸部size',
    ], 0.7),

    ([
    '人物.衣装',
    ], 0.5),

    ([
    '人物.全身装饰',
    ], 0.24),

    ([
    '人物.上身装饰',
    ], 0.24),

    ([
    '人物.下身装饰',
    ], 0.15),

    ([
    '人物.鞋袜',
    ], 0.3),

    ([
    '人物.胸部',
    ], 0.2),

    ([
    '人物.头发',
    ], 0.2),

    ([
    '人物.头部饰品',
    ], 0.3),

    ([
    '人物.耳朵',
    ], 0.1),

    ([
    '人物.脖子',
    ], 0.11),

    ([
    '人物.动作',
    ], 0.15),

    ([
    '人物.面部',
    ], 0.15),

    ([
    '物品',
    ], 0.2),

    ([
    '人文景观.食物.主食',
    '人文景观.食物.乳制品',
    '人文景观.食物.水果',
    '人文景观.食物.糖果零食',
    '人文景观.食物.肉类与海鲜',
    '人文景观.食物.蔬菜与香料',
    '人文景观.食物.调味料',
    '人文景观.食物.谷制品',
    '人文景观.食物.饮料', 
    ], 0.1),
]

class TagDatabase:
    def __init__(self, file, config) -> None:
        data = open(file, encoding='utf-8').read()
        r = yaml.safe_load(data)
        self.database = [ [[], config[i][1]] for i in range(len(config))]
        for k in r:
            for i in range(len(config)):
                if k not in config[i][0]:
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