import json
import random 

def load_information(path):
    with open(path, 'r', encoding= 'utf-8') as f:
        return json.loads(f.read())


if __name__ == "__main__":
    table = load_information("categories/films.json")
    random.shuffle(table)
    for i in table:
        print(i["question"])
        