import re
import yaml
import os
from datetime import datetime
from yaml_utils_local import write_yaml_data,get_yaml_data
import subprocess

dirname = os.path.dirname(__file__)
main_file = os.path.join(dirname, 'main.py')
req_file = os.path.join(dirname, 'requirements.txt')

q_1 = 'p'

while True:
    q_1 = input("This your first time? [y/n] ")
    if q_1.lower()=='y':
        print("\nWelcome! Creating a config.yaml and rule_data.json file for you!\n")
        with open('config.yaml','w') as fp:
            pass
        with open('rule_data.json','w') as fp:
            pass
        break
    elif q_1.lower()=='n':
        print("Alright, then I'm assuming you already have config.yaml and rule_data.json setup already")
        break
    else:
        print("wrong choice. You must pick from 'y' or 'n'")

tap_path = input("Enter path to your TAP_Detection repository:    ")

current_time = datetime.now()
timestamp = f"{current_time.year} {current_time.month} {current_time.day} {current_time.hour} {current_time.minute} {current_time.second}"

yaml_file = os.path.join(dirname, 'config.yaml')

config_data = {
    'TAP_path' : tap_path,
    'timestamp' : timestamp
}
write_yaml_data(yaml_file, config_data)

#now getting all the data required from TAP
import get_data
get_data

if q_1=='y':
    print("Installing dependencies...")
    command_r = f"pip install {req_file}"
    process = subprocess.Popen(command_r, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

    q_2 = 'p'

    while True:
        q_2 = input("The next step would be setting an alias by writing it to .bashrc file and sourcing it. Do you wish to proceed? [y/n] ")
        if q_2.lower()=='y':
            print("Setting alias for you...")
            command = f"""echo "alias find='python {main_file}'" >> ~/.bashrc"""
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            command = "source ~/.bashrc"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            break
        elif q_2.lower()=='n':
            print(f"{main_file} is the path to the main file. Run this file to use this tool.")
            break
        else:
            print("wrong choice. You must pick from 'y' or 'n'")


print("\nYou're all set!\n")

if q_1=='y':
    print("\nHow to use:")
    if q_2.lower()=='y':
        print("-> The calling command is 'find'. Example: 'find -s msiexec'")
    if q_2.lower()=='n':
        print(f"-> The calling command is {main_file}. Example: '{main_file} -s msiexec'")
    print("-> use -s or --strict for Strict search. The keywords after the flag will be checked strictly. This flag is mandatory")
    print("-> use -l or --lenient for Lenient search. The keywords after the flag will be not be checked strictly")
    print("-> use -re or --regex to search using regular expression.")
    print("-> use -a or --all to exclude results with only strict check keywords")
    print("-> use -h or --help for help")
else:
    print("\nTips:")
    print("-> use -h or --help for help")
