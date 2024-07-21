from datetime import datetime
import yaml
import json
import os
from yaml_utils_local import write_yaml_data, get_yaml_data
import subprocess

dirname = os.path.dirname(__file__)
yaml_file = os.path.join(dirname, 'config.yaml')
json_file = os.path.join(dirname, 'rule_data.json')
main_file = os.path.join(dirname, 'main.py')
existing_data = get_yaml_data(yaml_file)


current_time = datetime.now()
# f = open("/home/pavan_pothams/projects/self_scripts/check_query/timestamp.txt", "w")
existing_data['timestamp'] = f"{current_time.year} {current_time.month} {current_time.day} {current_time.hour} {current_time.minute} {current_time.second}"
write_yaml_data(yaml_file,existing_data)

# Get the list of all files and directories
path = f"{existing_data['TAP_path']}/rules/extended"
dir_list = os.listdir(path)
print(f"Fetching data from '{path}'...")

json_data = {}

for i in dir_list:
    if '.yaml' in i:
        with open(f'{path}/{i}', 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            json_data[data.get('id')] = data.get('search')

out_file = open(json_file, "w")

json.dump(json_data, out_file, indent = 4)

out_file.close()
f.close()

print("Setting alias for you...")
command = f"""echo "alias val='{main_file}'" >> ~/.bashrc"""
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()

print("\nYou're all set!\n")

print("\nHow to use:")
print("-> The calling command is 'val'. Example: 'val -s msiexec'")
print("-> use -s or --strict for Strict search. The keywords after the flag will be checked strictly. This flag is mandatory")
print("-> use -l or --lenient flag for lenient search")
print("-> use -l or --lenient for Lenient search. The keywords after the flag will be not be checked strictly")
print("-> use -a or --all to exclude results with only strict check keywords")
print("-> use -h or --help for help")