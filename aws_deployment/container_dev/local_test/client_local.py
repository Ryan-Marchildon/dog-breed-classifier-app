import sys
import base64
import os
import json
import requests
import csv
from prettytable import PrettyTable

"""
Usage from terminal:
$ python client_local.py <PATH-TO-IMAGE>

	e.g.:
	$ python client_local.py ./test_imgs/poodle_1.jpg

"""

API_URL = "http://localhost:8080/invocations"


print('*** Running Dog Breed Classifier Client (Local)')
print('Image Path: ', sys.argv[1])
print('API URL: ', API_URL)

# SPECIFY THE IMAGE FILE (JPG OR JPEG ONLY)
IMG_NAME = sys.argv[1]
IMG_PATH = os.path.join(os.getcwd(), IMG_NAME)


# ENCODE IMAGE FILE
ENCODING = 'utf-8'
with open(IMG_PATH, 'rb') as img_file:
	base64_image_bytes = base64.b64encode(img_file.read())
	
base64_image_string = base64_image_bytes.decode(ENCODING)	


# GENERATE RESPONSE REQUEST
headers = {"content-type": 'application/json'}
content = json.dumps({"image": base64_image_string})

response = requests.post(API_URL, data=content, headers=headers)


# PROCESS THE RESPONSE
inferences_string = response.content.decode(ENCODING)
reader = csv.reader(inferences_string.split('\n'), delimiter=',')

print('\nTop 5 Inferred Breeds:')
results_table = PrettyTable(['Rank', 'Inferred Breed', 'Probability'])
results_table.align['Rank'] = 'r'
results_table.align['Inferred Breed'] = 'l'
results_table.align['Probability'] = 'l'
for i, csv_row in enumerate(reader):
	results_table.add_row([i+1, csv_row[0], csv_row[1]])
	if i+1 == 5:
		break
print(results_table)

