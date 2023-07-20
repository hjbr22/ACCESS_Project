import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

def load_api():
   load_dotenv()

load_api()
# The URL endpoint
url = "https://access-ci.atlassian.net/reset/api/space?spaceKey=ACCESSdocumentation"
v2url = 'https://access-ci.atlassian.net/wiki/api/v2/pages/278069249?expand=body.storage'
params = {'limit':"250",'expand': 'body.storage'}

auth = HTTPBasicAuth(os.getenv("atlassian_username"),os.getenv("confluence_token"))
headers = {
   'Accept': "application/json"
}

response = requests.request("GET",v2url,headers=headers,auth=auth)

# Check for HTTP codes other than 200
if response.status_code != 200:
   print('Status:', response.status_code, 'Problem with the request. Exiting.')
   exit()

print(response.text)
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))