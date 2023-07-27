from models.rps import RPS
from models.gui import GUI
from models.rpGUI import RpGUI
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.software import Software
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

def get_rp_tables(rpNamesList):
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

def get_body():
    body="""
        <html>
            <body>
                <table class="confluenceTable" data-layout="default" data-local-id="5cbbf97b-608c-4f90-a077-31744917bd69">
                    <tr>
                        <th class="confluenceTh">
                            <p><strong>Temp Storage (TB)</strong></p>
                        </th>
                        <th class="confluenceTh">
                            <p><strong>Long-Term Storage (TB)</strong></p>
                        </th>
                        <th class="confluenceTh">
                            <p><strong>Memory (RAM) (GB)</strong></p>
                        </th>
                    </tr>
                    <tr>
                        <td class="confluenceTd">
                            <p>1</p>
                        </td>
                        <td class="confluenceTd">
                            <p>2.5</p>
                        </td>
                        <td class="confluenceTd">
                            <p>120</p>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
    """
    return body


def get_page_children():
    conf = get_conf()
    pageID = 245202949
    page = conf.get_page_by_id(page_id=pageID)
    pageChildren = conf.get_page_child_by_type(page_id=pageID, type='page')
    childPageIds=[]
    for page in pageChildren:
    #    print(page)
    #    print(page['id'])
        childPageIds.append(page['id'])
    print(childPageIds)

    pageJsonList=[]
    for page_id in childPageIds:
        page = conf.get_page_by_id(page_id)
        print(page)
        pageJsonList.append(json.dumps(page, sort_keys=True, indent=4, separators=(",", ": ")))

    print(pageJsonList)
    # for pageJson in pageJsonList:
    #    print(pageJson)
    # print(list(pageChildren))
        # print(json.dumps(pageChild, sort_keys=True, indent=4, separators=(",", ": ")))

# conf = get_conf()
# title = "test Title"
# with open('confluencePage.html','r') as f:
#     try:
#         body = f.read()
#     except:
#         print("couldn't read file")
#         body = ''
# body=get_body()
# parent_id = 245202949

# create_page(conf,title=title,body=body,parent_id=parent_id)

conf = get_conf()
rps = RPS.select().order_by(RPS.name)
rpNamesList = [rp.name for rp in rps]
print(rpNamesList)
tablesDict = get_rp_tables(rpNamesList)
parent_id = 245202949
for rpName in rpNamesList:
    print(rpName,"\n\n",tablesDict[rpName], '\n\n')

#     title = f'{rpName} Data'
#     body = ''
#     for table in tablesDict['Stampede-2']:
#         body += table.to_html(index=False,classes='confluenceTable')
#     create_page(conf,title=title,body=body,parent_id=parent_id)

# print(html)