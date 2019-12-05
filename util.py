import csv
import json


def read():
	with open('./static/timeseries.csv', 'r') as f:
		reader = csv.reader(f)
		timedata = list(reader)
	return timedata


def read_json():
	with open('./static/js/wc_true.json','r', encoding='utf-8') as f:
		parsed_json = json.load(f)
	return parsed_json

def get_count():

	return count