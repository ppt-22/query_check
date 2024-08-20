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
from pprint import pprint 

def main(args):
	
	strict_check = []
	lenient_check = []
	regex_check = []
	if args.lenient:
		# flag = 1
		lenient_check = args.lenient
	if args.regex:
		# flag_r = 1
		regex_check = args.regex

	if args.strict:
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
	sample_data_3 = []
	sample_data = []
	p_1 = []
	p_2 = []
	p_3 = []
	s_d = {}


	if args.strict:
		for i in df:
			matches_s = [x for x in strict_check if re.search(rf"\b{x.lower()}\b", df[i].lower())]
			if len(matches_s)==len(strict_check) and i!="1.1.2784":
				sample_data_1.append([i,df[i],matches_s])
				temp = {}
				temp["query"] = df[i]
				temp["matches"] = matches_s
				s_d[i] = temp
				p_1.append(i)

	if args.lenient:
		if args.strict:
			for i in s_d:
				matches_l = [x for x in lenient_check if re.search(rf"\b{x.lower()}\b", s_d[i]["query"].lower())]
				if i!="1.1.2784" and len(matches_l)!=0:
					sample_data_2.append([i,s_d[i]["query"],strict_check + matches_l])
					p_2.append(i)
		else:
			for i in df:
				matches_l = [x for x in lenient_check if re.search(rf"\b{x.lower()}\b", df[i].lower())]
				if i!="1.1.2784" and len(matches_l)!=0:
					sample_data_2.append([i,df[i],strict_check + matches_l])
					p_2.append(i)

	if args.regex:
		if args.strict:
			print(args.strict)
			for i in s_d:
				matches_r = [x for x in regex_check if re.search(rf"{x}", df[i].lower())]
				if i!="1.1.2784" and len(matches_r)!=0:
					sample_data_3.append([i,s_d[i]["query"],strict_check + matches_r])
					p_3.append(i)
		else:
			for i in df:
				matches_r = [x for x in regex_check if re.search(rf"{x}", df[i].lower())]
				if i!="1.1.2784" and len(matches_r)!=0:
					sample_data_3.append([i,df[i],matches_r])
					p_3.append(i)


	def get_inter(list1,list2,list3):
		concat = [list1,list2,list3]
		t = []
		if len(list1)!=0:
			t = list1[:]
			concat.remove(list1)
		elif len(list2)!=0:
			t = list2[:]
			concat.remove(list2)
		elif len(list3)!=0:
			t = list3[:]
			concat.remove(list3)
		for i in concat:
			if len(i)!=0:
				t = list(set(i) & set(t))
		return t

	p_inter = get_inter(p_1,p_2,p_3)


	sample_data = sample_data_1 + sample_data_2 + sample_data_3
	master_sample = [titles]
	ms_dict = {}
	for id in p_inter:
		for s in sample_data:
			if id in s:
				ms_dict[id] = s

	master_sample.extend(list(ms_dict.values()))
	if args.all:
		t.add_rows(master_sample)
	else:
		t.add_rows(sample_data)

	print(t.draw())
	print("searched keywords: ")
	if len(strict_check)!=0:
		print("\tstrict check: ",strict_check)
	if len(lenient_check)!=0:
		print("\tlenient check: ",lenient_check)
	if len(regex_check)!=0:
		print("\tregex check: ",regex_check)
	print(f"{len(sample_data)-1} results")
	print("\ntips:")
	print("-> use -h or --help for help")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query finder.\nThe calling command is 'find'. Example: 'find -s msiexec'"
	)
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Verbose output"
    )
    parser.add_argument('-s', '--strict', nargs="*", required=False, help="Strict search. The keywords after the flag will be checked strictly. This flag is mandatory")
    parser.add_argument('-l', '--lenient', nargs="*", required=False, help="Lenient search. The keywords after the flag will be not be checked strictly")
    parser.add_argument('-re', '--regex',  nargs="*", required=False, help="Search using regular expression")
    parser.add_argument('-a', '--all',  action="store_true", required=False, help="Exclude results with only strict check keywords")
    args = parser.parse_args()
    main(args)
