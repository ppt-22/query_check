import yaml

def get_yaml_data(file_path):
    with open(file_path,'r') as file:
        existing_data = yaml.load(file, Loader=yaml.FullLoader)
        if existing_data:
            return existing_data
        else:
            return

def write_yaml_data(file_path, data):
    with open(file_path,'w') as file:
        new_data = data
        yaml.dump(new_data,file,sort_keys=False)