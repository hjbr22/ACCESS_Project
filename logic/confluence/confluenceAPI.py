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

def create_conf_page(conf,title,body,parent_id=None,space="AccessInternalContentDevelopment"):
   try:
        conf.create_page(space=space,title=title,
                            body=body,parent_id=parent_id,
                            type='page',representation='storage',
                            editor='v2', full_width=False )
   except Exception as e:
        print(e)

def get_page_children_ids(pageID):
    conf = get_conf()
    page = conf.get_page_by_id(page_id=pageID)
    pageChildren = conf.get_page_child_by_type(page_id=pageID, type='page')
    childPageIds=[]
    for page in pageChildren:
        childPageIds.append(page['id'])
    return(childPageIds)

       # # pageJsonList=[]
    # # for page_id in childPageIds:
    # #     page = conf.get_page_by_id(page_id)
    # #     print(page)
    # #     pageJsonList.append(json.dumps(page, sort_keys=True, indent=4, separators=(",", ": ")))

    # return(childPageIds)

def get_page_data(pageID="255754279"):
   conf = get_conf()
   page = conf.get_page_by_id(pageID, expand='body.view')
   page_content = page['body']['view']['value'] 

   table = pd.read_html(page_content)

   print(type(table))
   print('\n Number of tables:', len(table))
   #get the first table with index 0
   First_table = table[0]

   #get the second table with index 1
   Second_table = table[1]

   print('\n Table 1\n')
   print(First_table)
   print(Second_table.to_html)
   print('\n Table 2\n')
   print(Second_table)
