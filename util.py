import csv


def read():
	with open('./static/timeseries.csv', 'r') as f:
		reader = csv.reader(f)
		timedata = list(reader)
	return timedata