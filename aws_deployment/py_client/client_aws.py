import sys
import base64
import os
import json
import requests
import csv
import tkinter
import PIL
from PIL import Image, ImageTk

from prettytable import PrettyTable
from tkinter.filedialog import askopenfilename

"""
Usage from terminal:
$ python client_local.py <PATH-TO-IMAGE>

	e.g.:
	$ python client_local.py ./test_imgs/poodle_1.jpg

"""

API_URL = "https://osbh7tvzj3.execute-api.us-east-2.amazonaws.com/beta/classifydogbreed"


# SPECIFY THE IMAGE FILE (JPG OR JPEG ONLY)
if len(sys.argv) is not 1:
	IMG_NAME = sys.argv[1]
	IMG_PATH = os.path.join(os.getcwd(), IMG_NAME)
else:
	IMG_PATH = askopenfilename() 


# DISPLAY STATUS TO CONSOLE
print('*** Running Dog Breed Classifier Client (Local)')
print('Image Path: ', IMG_PATH)
print('API URL: ', API_URL)


# RESIZE IMAGE IF NECESSARY 
# -- There is a file size limit on AWS API requests
WIDTH_THRESHOLD = 2000  # pixels
img = Image.open(IMG_PATH)
if img.size[0] > WIDTH_THRESHOLD:
	wpercent = (WIDTH_THRESHOLD / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((WIDTH_THRESHOLD, hsize), PIL.Image.ANTIALIAS)
	img.save('resized_image.jpg')
	IMG_PATH = os.path.join(os.getcwd(), 'resized_image.jpg')


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
inferences = json.loads(response.content.decode(ENCODING))['results']
reader = csv.reader(inferences.split('\n'), delimiter=',')

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

