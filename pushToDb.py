from models import db
from models.rps import RPS
from models.gui import GUI
from models.rpGUI import RpGUI
from models.rpMemory import RpMemory
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from confluence.confluenceAPI import get_conf, get_page_children_ids, get_tabulated_page_data

def get_rp_storage_data(storageTable):
    # TODO: validate storageTable
    scratch_tb = storageTable.iloc[0,0]
    longterm_tb = storageTable.iloc[0,1]
    storageData = {'scratch_tb': scratch_tb,
                'longterm_tb': longterm_tb,}
    return storageData

def get_rp_memory_data(memoryTable, rp):
    # TODO: validate memoryTable
    memoryTableIsValid = True
    if memoryTableIsValid:
        node_type = memoryTable.columns[0]
        per_node_memory_gb = memoryTable.columns[1]
        memoryData = []
        for i in range(0, len(memoryTable.index)):
            row = memoryTable.iloc[[i]]
            memoryData.append({'rp':rp,
                            'node_type': row[node_type].to_string(index=False),
                            'per_node_memory_gb':row[per_node_memory_gb].to_string(index=False)})
        return(memoryData)
    return False

def get_rp_functionality_data(funcTable):
    # TODO: validate functionalityTable
    functionalityTableIsValid = True
    if functionalityTableIsValid:
        graphical = funcTable.iloc[0,1]
        parallel = funcTable.iloc[1,1]
        always_running = funcTable.iloc[2,1]
        virtual_machine = funcTable.iloc[3,1]
        funcData = {'graphical':graphical,
                    'parallel':parallel,
                    'always_running':always_running,
                    'virtual_machine':virtual_machine}
        return funcData
    return False

def get_rp_gui_data(guiTable):
    pass

def update_rp_table_form_conf(tables,pageName):

    messages = []

    rpName = pageName[:pageName.rfind(" ")]
    rp = RPS.get_or_none(RPS.name == rpName)

    storageTable = tables[0]
    storageData = get_rp_storage_data(storageTable)

    functionalityTable = tables[2]
    funcData = get_rp_functionality_data(functionalityTable)

    if not rp:
        print(f"RP '{rpName}' not found")
        with db.atomic() as transaction:
            try:
                rpTableData = {}
                rpTableData['name'] = rpName
                rpTableData.update(storageData)
                rpTableData.update(funcData)
                print('Creating RP')
                rp = RPS.create(**rpTableData)
                print('RP created')
            except Exception as e:
                msg = "Error while trying to create RP"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()
    else:
        with db.atomic() as transaction:
            try:
                rpTableData = {}
                rpTableData.update(storageData)
                rpTableData.update(funcData)
                RPS.update(**rpTableData).where(RPS.name==rpName).execute()
                rp = RPS.get_by_id(rp)
                print('RP updated')
            except Exception as e:
                msg = f"Error while trying to update RP {rpName}"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()
    
    memoryTable = tables[1]
    memoryData = get_rp_memory_data(memoryTable,rp)
    if memoryData:
        with db.atomic() as transaction:
            try:
                delRpMem = RpMemory.delete().where(RpMemory.rp == rp)
                delRpMem.execute()
                createRpMem = RpMemory.insert_many(memoryData).on_conflict_replace()
                createRpMem.execute()
                print(f"Memory info successfully updated for {rpName}")
            except Exception as e:
                msg = f"Error while trying to update {rpName} memory"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()
    
    guiTable = tables[3]
    # TODO: Validate guiTable
    guiTableIsValid = True
    if guiTableIsValid:
        guiTable.fillna(1, inplace=True)
        guiTuple = guiTable.itertuples(index=False)
        # print(guiTuple)
        with db.atomic() as transaction:
            try:
                RpGUI.delete().where(RpGUI.rp == rp).execute()
                for item in guiTuple:
                    gui, guiCreated = GUI.get_or_create(gui_name = item[0])
                    #TODO: suitability not added
                    rpGuiData =  {'rp':rp,'gui':gui}
                    rpGui = RpGUI.create(**rpGuiData)
            except Exception as e:
                msg = f"Error while trying to update {rpName} GUI"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()

    fieldsTable = tables[4]
    #TODO: validate fieldsTable
    fieldsTableIsValid = True
    if fieldsTableIsValid:
        fieldsTuple = fieldsTable.itertuples(index=False)
        with db.atomic() as transaction:
            try:
                RpResearchField.delete().where(RpResearchField.rp == rp).execute()
                for item in fieldsTuple:
                    field, fieldCreated = ResearchFields.get_or_create(field_name=item[0])
                    researchFieldData = {'rp':rp,'research_field':field,'suitability':item[1]}
                    RpResearchField.create(**researchFieldData)
            except Exception as e:
                msg = f"Error while trying to update {rpName} research fields"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()

    jobClassTable = tables[5]
    #TODO: validate fieldsTable
    jobClassIsValid = True
    if jobClassIsValid:
        jobClassTuple = jobClassTable.itertuples(index=False)
        with db.atomic() as transaction:
            try:
                RpJobClass.delete().where(RpJobClass.rp == rp).execute()
                for item in jobClassTuple:
                    jobClass, jobClassCreated = JobClass.get_or_create(class_name=item[0])
                    jobClassData = {'rp':rp,'job_class':jobClass,'suitability':item[1]}
                    RpJobClass.create(**jobClassData)
            except Exception as e:
                msg = f"Error while trying to update {rpName} job class"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()

def update_db_from_conf():
    pageIds = get_page_children_ids('245202949')
    conf = get_conf()
    for id in pageIds:
        tables, pageName = get_tabulated_page_data(conf,pageID=id)
        if ('Softwares' in pageName) or ('Outline' in pageName):
            pass
        else:
            update_rp_table_form_conf(tables,pageName)

update_db_from_conf()
