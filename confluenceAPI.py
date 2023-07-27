import os
from dotenv import load_dotenv
from atlassian import Confluence
import pandas as pd

def get_conf(url='https://access-ci.atlassian.net'):

   load_dotenv()

   altas_user = os.getenv("atlassian_username")
   conf_token = os.getenv("confluence_token")

   # The URL endpoint
   conf = Confluence(url=url, username=altas_user, password=conf_token)
   return conf

def get_page_data(pageID=None):
   conf = get_conf()
   pageID = '255754279'
   page = conf.get_page_by_id(pageID, expand='body.view')
   page_content = page['body']['view']['value'] 

   # print(page_content)
   table = pd.read_html(page_content)

   print(type(table))
   # print(table)
   print('\n Number of tables:', len(table))
   #get the first table with index 0
   First_table = table[0]

   #get the second table with index 1
   Second_table = table[1]

   print('\n Table 1\n')
   print(First_table)
   print(Second_table.to_html)
   # print('\n Table 2\n')
   # print(Second_table)

# get_page_data()
