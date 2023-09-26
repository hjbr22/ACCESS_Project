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
from confluence.APIValidation import validate_storage_table, validate_suitability, validate_memory_table

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
    if RPS.select().count() == 0:
        rp = None
    else:
        rp = RPS.get_or_none(RPS.name == rpName)
        print(f"\nGetting data for {rpName}")

    storageTable = tables[0]
    storageTableIsValid, msg = validate_storage_table(storageTable)
    if storageTableIsValid:
        storageData = get_rp_storage_data(storageTable)
    else:
        messages.append(msg+(". Storage data was not updated."))
        print(msg+(". Storage data was not updated."))

    functionalityTable = tables[2]
    funcTableIsValid, msg = validate_suitability(functionalityTable)
    if funcTableIsValid:
        funcData = get_rp_functionality_data(functionalityTable)
    else:
        messages.append(msg+(". Functionality data was not updated."))
        print(msg+(". Functionality data was not updated."))

    if not rp:
        print(f"RP '{rpName}' not found")
        if not (funcTableIsValid and storageTableIsValid):
            print(f'Unable to create new RP {rpName}.')
            messages.append(f'Unable to create new RP {rpName}.')
            return
        with db.atomic() as transaction:
            try:
                rpTableData = {}
                rpTableData['name'] = rpName
                rpTableData.update(storageData)
                rpTableData.update(funcData)
                rp = RPS.create(**rpTableData)
                print(f"Rp {rpName} created")
            except Exception as e:
                msg = f"Error while trying to create RP {rpName}"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()
    else:
        with db.atomic() as transaction:
            try:
                rpTableData = {}
                if storageTableIsValid:
                    rpTableData.update(storageData)
                if funcTableIsValid:
                    rpTableData.update(funcData)
                RPS.update(**rpTableData).where(RPS.name==rpName).execute()
                print(f'RP {rpName} updated')
            except Exception as e:
                msg = f"Error while trying to update RP {rpName}"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()
    
    memoryTable = tables[1]
    memoryDataIsValid, msg = validate_memory_table(memoryTable)

    if memoryDataIsValid:
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
    else:
        messages.append(msg+("Memory data was not updated."))
        print(msg+("Memory data was not updated."))
    
    guiTable = tables[3]
    # TODO: Validate guiTable
    guiTableIsValid = validate_suitability(guiTable)
    if guiTableIsValid:
        guiTable.fillna(1, inplace=True) #replace na with 1
        guiTuple = guiTable.itertuples(index=False)
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
    fieldsTableIsValid,msg = validate_suitability(fieldsTable)
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
    else:
        messages.append(msg+(". Fields data was not updated."))
        print(msg+(". Fields data was not updated."))

    jobClassTable = tables[5]
    #TODO: validate fieldsTable
    jobClassIsValid,msg = validate_suitability(jobClassTable)
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
    else:
        messages.append(msg+(". Job class data was not updated."))
        print(msg+(". Job class data was not updated."))

    print("Errors: ", messages)

def update_db_from_conf():
    conf = get_conf()
    pageIds = get_page_children_ids(conf,'245202949')
    for id in pageIds:
        tables, pageName = get_tabulated_page_data(conf,pageID=id)
        if ('Softwares' in pageName) or ('Outline' in pageName):
            pass
        else:
            update_rp_table_form_conf(tables,pageName)

if __name__ == '__main__':
    update_db_from_conf()
    
