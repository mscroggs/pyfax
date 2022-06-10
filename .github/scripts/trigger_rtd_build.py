import requests
import sys

URL = 'https://readthedocs.org/api/v3/projects/pyfax/versions/latest/builds/'
TOKEN = sys.argv[-1]
HEADERS = {'Authorization': f'token {TOKEN}'}
response = requests.post(URL, headers=HEADERS)
print(response.json())
