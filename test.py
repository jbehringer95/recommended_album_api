import requests
import urllib.parse
import json

import numpy as np

BASE = 'http://recommended-album-api-dev.us-east-1.elasticbeanstalk.com/prediction/'
BASE1 = 'http://127.0.0.1:5000/prediction/'

value_list = ['Art Rock']
response = requests.get(BASE + urllib.parse.quote(str(value_list)))
print(response.json())

