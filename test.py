import requests
import urllib.parse
import json

import numpy as np

BASE = 'http://127.0.0.1:5000/'

value_list = ['thrash Metal', 'Acoustic rock', 'ENErgetic', 'Male VocaLs', 'alternative rock', 'Art Rock', 'melancholic']
response = requests.get(BASE + 'prediction/' + urllib.parse.quote(str(value_list)))
print(response.json())