from models.rps import RPS
from models.gui import GUI
from models.rpGUI import RpGUI
from models.rpJobClass import RpJobClass
from models.rpResearchField import RpResearchField
from models.rpSoftware import RpSoftware
import json
import pandas as pd
from confluenceAPI import get_conf

def create_page(conf,title,body,parent_id=None,space="AccessInternalContentDevelopment"):
   try:
        conf.create_page(space=space,title=title,
                            body=body,parent_id=parent_id,
                            type='page',representation='storage',
                            editor='v2', full_width=False )
   except Exception as e:
        print(e)

def get_research_fields(rpName):
    rp = RPS.select().where(RPS.name==rpName)
    researchFields = RpResearchField.select().where(RpResearchField.rp == rp).order_by(RpResearchField.rp.name)
    return(researchFields)

def get_job_classes(rpName):
    rp = RPS.select().where(RPS.name==rpName)
    jobClasses = RpJobClass.select().where(RpJobClass.rp == rp).order_by(RpJobClass.rp.name)
    return jobClasses

def get_softwares(rpName):
    rp = RPS.select().where(RPS.name==rpName)
    softwares = RpSoftware.select().where(RpSoftware.rp == rp).order_by(RpSoftware.rp.name)
    return(softwares)

def get_guis(rpName):
    rp = RPS.select().where(RPS.name==rpName)
    guis = RpGUI.select().where(RpGUI.rp == rp).order_by(RpGUI.rp.name)
    return(guis)


def get_rp_data_tables(rpNamesList):
    tablesDict = {}
    for rpName in rpNamesList:
        tablesDict[rpName] = []
        rp = RPS.select().where(RPS.name == rpName)[0]
        rpHardware = {'Temp Storage (TB)': [rp.scratch_tb],
                      'Long-Term Storage (TB)':[rp.longterm_tb],
                      'Memory (RAM) (GB)':['']}
        df = pd.DataFrame(data=rpHardware)
        tablesDict[rpName].append(df)
        rpSupports = {
                        'Functionality':['Supports jobs that have a graphical component',
                                                'CPU and GPU run in Parallel',
                                                'Job is always active',
                                                'Has a virtual machine or supports virtualization'],
                        'Suitability':[rp.graphical,
                                       rp.parallel,
                                       rp.always_running,
                                       rp.virtual_machine]
                    }
        df = pd.DataFrame(data=rpSupports)
        tablesDict[rpName].append(df)
        
        guis = get_guis(rpName)
        rpGui = {'GUI':[gui.gui.gui_name for gui in guis],
                 'Suitability': ''}
        df = pd.DataFrame(data=rpGui)
        tablesDict[rpName].append(df)

        researchFields = get_research_fields(rpName)
        rpResearch = {'Field':[field.research_field.field_name for field in researchFields],
                      'Suitability':[field.suitability for field in researchFields]
                      }
        df = pd.DataFrame(data=rpResearch)
        tablesDict[rpName].append(df)

        jobClasses = get_job_classes(rpName)
        rpJob = {'Job Class': [jobClass.job_class.class_name for jobClass in jobClasses],
                 'Suitability':[jobClass.suitability for jobClass in jobClasses]}
        df = pd.DataFrame(data=rpJob)
        tablesDict[rpName].append(df)

        softwares = get_softwares(rpName)
        rpSoftware={'Software Packages': [software.software.software_name for software in softwares],
                    'Suitability':[software.suitability for software in softwares],
                    'CPU/GPU':''}
        df = pd.DataFrame(data=rpSoftware)
        tablesDict[rpName].append(df)

    return(tablesDict)

def get_page_children(pageID=245202949):
    conf = get_conf()
    page = conf.get_page_by_id(page_id=pageID)
    pageChildren = conf.get_page_child_by_type(page_id=pageID, type='page')
    childPageIds=[]
    for page in pageChildren:
        childPageIds.append(page['id'])
    print(childPageIds)

    # pageJsonList=[]
    # for page_id in childPageIds:
    #     page = conf.get_page_by_id(page_id)
    #     print(page)
    #     pageJsonList.append(json.dumps(page, sort_keys=True, indent=4, separators=(",", ": ")))

    return(childPageIds)

conf = get_conf()
rps = RPS.select().order_by(RPS.name)
rpNamesList = [rp.name for rp in rps]
print(rpNamesList)
tablesDict = get_rp_data_tables(rpNamesList)
parent_id = 245202949
for rpName in rpNamesList:
    title = f'{rpName} Data'
    body = ''
    for table in tablesDict[rpName]:
        body += table.to_html(index=False,classes='confluenceTable')
    create_page(conf,title=title,body=body,parent_id=parent_id)
