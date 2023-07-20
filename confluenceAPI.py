import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs

def load_api():
   load_dotenv()

load_api()
# The URL endpoint
pageid = '255754279'
url = f'https://access-ci.atlassian.net/wiki/rest/api/content/{pageid}'
params = {'expand': 'body.view'}

auth = HTTPBasicAuth(os.getenv("atlassian_username"),os.getenv("confluence_token"))
headers = {
   'Accept': "application/json"
}
response = requests.request("GET",url,headers=headers,auth=auth,params=params)

# Check for HTTP codes other than 200
if response.status_code != 200:
   print('Status:', response.status_code, 'Problem with the request. Exiting.')
   exit()

data = json.loads(response.text)
pageContent = bs(data['body']['view']['value'])
print(pageContent.prettify())
with open('confluencePage.html', 'w') as cp:
   print(type(pageContent.prettify()))
   cp.write(pageContent.prettify())