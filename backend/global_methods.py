import yaml


def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def read_txt(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    return file_contents
