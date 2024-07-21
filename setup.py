import re
import yaml
import os
from datetime import datetime
from yaml_utils_local import write_yaml_data,get_yaml_data
import subprocess

dirname = os.path.dirname(__file__)
main_file = os.path.join(dirname, 'main.py')
req_file = os.path.join(dirname, 'requirements.txt')

q_1 = input("This your first time? [y/n] ")

if q_1=='y':
    print("\nWelcome! Creating a config.yaml and rule_data.json file for you!\n")
    with open('config.yaml','w') as fp:
        pass
    with open('rule_data.json','w') as fp:
        pass

tap_path = input("Enter path to your TAP_Detection repository:    ")

current_time = datetime.now()
timestamp = f"{current_time.year} {current_time.month} {current_time.day} {current_time.hour} {current_time.minute} {current_time.second}"

yaml_file = os.path.join(dirname, 'config.yaml')

data_to_append = {
    'TAP_path' : tap_path,
    'timestamp' : timestamp
}
write_yaml_data(yaml_file, data_to_append)

#now getting all the data required from TAP
import get_data
get_data

print("Installing dependencies...")
command = f"""'{main_file}'" >> ~/.bashrc"""
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()

print("Setting alias for you...")
command_r = f"pip install {req_file}"
process = subprocess.Popen(command_r, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()

print("\nYou're all set!\n")

print("\nHow to use:")
print("-> The calling command is 'val'. Example: 'val -s msiexec'")
print("-> use -s or --strict for Strict search. The keywords after the flag will be checked strictly. This flag is mandatory")
print("-> use -l or --lenient flag for lenient search")
print("-> use -l or --lenient for Lenient search. The keywords after the flag will be not be checked strictly")
print("-> use -a or --all to exclude results with only strict check keywords")
print("-> use -h or --help for help")