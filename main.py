from texttable import Texttable
import json
import sys
from pytz import timezone
from datetime import datetime
import subprocess
import re
import math
import argparse
import os
import yaml

def main(args):
	
	flag = 0
	lenient_check = []
	if args.lenient:
		flag = 1
		lenient_check = args.lenient

	strict_check = args.strict

	dirname = os.path.dirname(__file__)
	
	#yaml file with all the data
	yaml_file = os.path.join(dirname, 'config.yaml')
	
	#json file with rule data 
	json_file = os.path.join(dirname, 'rule_data.json')

	#get_data python script
	get_data_file = os.path.join(dirname, 'get_data.py')

	current_time = datetime.now()
	b = datetime(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second)

	with open(yaml_file,'r') as file:
		existing_data = yaml.load(file, Loader=yaml.FullLoader)
	last_check = existing_data['timestamp'].split(" ")
	a = datetime(int(last_check[0]), int(last_check[1]), int(last_check[2]), int(last_check[3]), int(last_check[4]), int(last_check[5]))

	diff = b-a
	hours = diff.total_seconds()/3600
	print("last update: ",math.ceil(hours*100)/100,"hours ago")

	TAP_path = existing_data['TAP_path']
	if hours>24:
		subprocess.run(["git", "checkout", "dev"], cwd=TAP_path)
		subprocess.run(["git", "pull"], cwd=TAP_path)
		print("Updating rule_data.json")
		subprocess.call(['python3',get_data_file])

	with open(json_file) as f:
		df = json.load(f)

	t = Texttable(max_width=140)
	titles = ["id", "query","match"]

	values = list(df.values())

	sample_data_1 = [titles]
	sample_data_2 = []
	sample_data = []

	p_1 = {}

	for i in df:
	#	matches = [x for x in keywords if x.lower() in df[i].lower()]
		matches_s = [x for x in strict_check if re.search(rf"\b{x.lower()}\b", df[i].lower())]
		if len(matches_s)==len(strict_check) and i!="1.1.2784":
			sample_data_1.append([i,df[i],matches_s])
			temp = {}
			temp["query"] = df[i]
			temp["matches"] = matches_s
			p_1[i] = temp

	if flag == 1 and len(lenient_check)!=0:
		for i in p_1:
			matches_l = [x for x in lenient_check if re.search(rf"\b{x.lower()}\b", p_1[i]["query"].lower())]
			if i!="1.1.2784" and len(matches_l)!=0:
				sample_data_2.append([i,p_1[i]["query"],strict_check + matches_l])

	sample_data = sample_data_1 + sample_data_2

	if args.all:
		sample_data_2.insert(0,titles)
		t.add_rows(sample_data_2)
	else:
		t.add_rows(sample_data)

	print(t.draw())
	print("searched keywords: ",strict_check + lenient_check)
	print(f"{len(sample_data)-1} results")
	print("\ntips:")
	print("-> use -l or --lenient flag for lenient search")
	print("-> use -s or --strict for Strict search. The keywords after the flag will be checked strictly")
	print("-> use -l or --lenient for Lenient search. The keywords after the flag will be not be checked strictly")
	print("-> use -a or --all to exclude results with only strict check keywords")
	print("-> use -h or --help for help")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ACE rules Formatter")
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Verbose output"
    )
    parser.add_argument('-s', '--strict', nargs="*", required=True, help="Strict search. The keywords after the flag will be checked strictly")
    parser.add_argument('-l', '--lenient', nargs="*", required=False, help="Lenient search. The keywords after the flag will be not be checked strictly")
    parser.add_argument('-a', '--all',  action="store_true", required=False, help="Exclude results with only strict check keywords")
    args = parser.parse_args()
    main(args)
