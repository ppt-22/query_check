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

def source_bashrc():
    if os.environ.get("SHELL") == "/bin/bash":
        subprocess.run(["bash", "source ~/.bashrc"], shell=True, check=True)
        print()
    elif os.environ.get("SHELL") == "/bin/zsh":
        subprocess.run(["zsh","source ~/.bashrc"], shell=True, check=True)
    else:
        print("Error: Unsupported shell")

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

r = subprocess.run(["which","python"])
if r.returncode==0:
    python_v = "python"
else:
    r = subprocess.run(["which","python3"])
    if r.returncode==0:
        python_v = "python3"
    else:
        print("ERROR")
        exit(0)

shell_path = os.environ.get("SHELL")
print(shell_path)
if shell_path:
    if "bash" in shell_path:
        shell = "bashrc"
    elif "zsh" in shell_path:
        shell = "zshrc"
    else:
        shell = "bashrc"

if q_1=='y':
    print("Installing dependencies...")
    command_r = f"pip install {req_file}"
    process = subprocess.Popen(command_r, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process.kill()

    q_2 = 'p'

    while True:
        q_2 = input("The next step would be setting an alias by writing it to .bashrc file and sourcing it. Do you wish to proceed? [y/n] ")
        if q_2.lower()=='y':
            print("Setting alias for you...")
            command = f"""echo "alias findquery='{python_v} {main_file}'" >> ~/.{shell}"""
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            process.kill()
            source_bashrc()
            break
        elif q_2.lower()=='n':
            print(f"{main_file} is the path to the main file. Run this file to use this tool.")
            break
        else:
            print("wrong choice. You must pick from 'y' or 'n'")


print("\nconfig.yaml: I'M ALIVE! I'M ALIVEEEE!\n")

if q_1=='y':
    print("\nHow to use:")
    if q_2.lower()=='y':
        print("-> The calling command is 'findquery'. Example: 'findquery -s msiexec'")
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
