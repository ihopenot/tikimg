import os
import yaml

all_data = {}

for path, _, files in os.walk("tags"):
    for file in files:
        if file.endswith(".yaml"):
            print(file)
            r = yaml.safe_load(open(os.path.join(path, file), encoding="utf8").read())
            key = '.'.join(r["category"] + [r["name"]])
            value = [{k: r["content"][k]["name"]} for k in r["content"]]
            all_data[key] = value

open("text.yaml", "w", encoding="utf-8").write(yaml.safe_dump(all_data, allow_unicode=True))