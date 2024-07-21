import re
import yaml
import os
from datetime import datetime
from yaml_utils_local import write_yaml_data,get_yaml_data

dirname = os.path.dirname(__file__)

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