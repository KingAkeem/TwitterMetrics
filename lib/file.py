import csv
import os
from flask import make_response

def create_csv(name, rows, fields):
	filename = f'{name}.csv'
	with open(filename, 'w+') as csvfile:
		csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
		csvwriter.writeheader()
		for row in rows:
			try:
				csvwriter.writerow(row)
			except (KeyError, ValueError) as e:
				print(f'Found invalid row. {e}')
		return filename 

def make_csv_response(username, rows, fields):
	filename = create_csv(username, rows, fields)
	with open(filename, 'rb') as csv_file:
		response = make_response(csv_file.read())

	if os.path.exists(filename):
		os.remove(filename)

	response.status = 200
	response.headers["Content-Disposition"] = f"attachment; filename={filename}"
	response.headers["Content-type"] = "text/csv"
	return response