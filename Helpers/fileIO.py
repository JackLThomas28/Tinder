import json

def load_json_file(file_name):
    data = None
    with open(file_name, 'r') as infile:
        data = json.load(infile)
    return data


def save_json_file(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)