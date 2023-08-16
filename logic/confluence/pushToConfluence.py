from models.rps import RPS
from logic.research import get_research_fields
from logic.jobClass import get_job_classes
from logic.softwares import get_softwares 
from logic.gui import get_guis
from logic.confluence.confluenceAPI import get_conf, create_conf_page
import pandas as pd

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

def create_rp_conf_pages():
    conf = get_conf()
    rps = RPS.select().order_by(RPS.name)
    rpNamesList = [rp.name for rp in rps]
    tablesDict = get_rp_data_tables(rpNamesList)
    parent_id = 245202949
    for rpName in rpNamesList:
        title = f'{rpName} Data'
        body = ''
        for table in tablesDict[rpName]:
            body += table.to_html(index=False,classes='confluenceTable')
        create_conf_page(conf,title=title,body=body,parent_id=parent_id)