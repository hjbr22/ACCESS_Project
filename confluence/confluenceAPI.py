import os
from dotenv import load_dotenv
from atlassian import Confluence
import pandas as pd
# from APIValidation import validate_table_1, validate_table_2, validate_table_3, validate_table_4, validate_table_5, validate_table_6

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

def get_page_children_ids(conf,pageID):
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

def get_tabulated_page_data(conf, pageID):
   page = conf.get_page_by_id(pageID, expand='body.view')
   pageContent = page['body']['view']['value'] 
   pageTitle = page['title']
   table = pd.read_html(pageContent)
   
   return table, pageTitle
   

