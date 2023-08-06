import os
from dotenv import load_dotenv
from atlassian import Confluence
import pandas as pd

def load_api():
   load_dotenv()

load_api()

# altas_user = os.getenv("atlassian_username")
# conf_token = os.getenv("confluence_token")
# page_id = '255754279'

# # The URL endpoint
# url = 'https://access-ci.atlassian.net'
# conf = Confluence(url=url, username=altas_user, password=conf_token)
# page = conf.get_page_by_id(page_id, expand='body.view')
# page_content = page['body']['view']['value'] 

# table = pd.read_html(page_content)

# print('\n Number of tables:', len(table))
# tot_tables = len(table)

# #Printing the contents of all the tables from the API call
# for i in tot_tables:
#    print(table[i])
#    print('\n')
