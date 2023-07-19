from models.rpGUI import RpGUI
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from models.rps import RPS
from models.software import Software
from models.rpSoftware import RpSoftware
import operator
from functools import reduce
import logging

#Initialize query logger
query_logger = logging.getLogger(__name__)

#Override default logging level
query_logger.setLevel('INFO')

#Handler/Formatter for query logs. Send to query.logs
query_handler = logging.FileHandler("formInfo.log", mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
query_handler.setFormatter(formatter)
query_logger.addHandler(query_handler)


def calculate_points(currentPoints, suitability=1):
    """
    Calculates how many points should be given based on suitability
    This functions is called by the other 'calculate_score_' functions
    """
    if suitability>0:
        points = currentPoints + (suitability*1)
    else:
        points = currentPoints + 0.5

    return points

def calculate_score_rf(researchFieldList,scoreBoard):
    """
    Calculates and gives points to rps based on the items in the researchFieldList
    researchFieldList: list of research fields the user selected
    scoreBoard: dict with RPs as keys and their scores as values
                if RP has not been assigned a value yet then it will not be in the dict
    return: returns the updated scoreboard
    """
    # Set the parameters used to filter the table
    filter = []
    for researchField in researchFieldList:
        filter.append((ResearchFields.field_name == f"{researchField}"))
    
    # Combine the RpResearchField and ResearchFields tables, and 
    # Only select the ones that match the filter
    rpWithFieldTable = (RpResearchField.select()
                                       .join(ResearchFields, on=(RpResearchField.research_field==ResearchFields.id))
                                       .where(reduce(operator.or_,filter))).select()
    query_logger.info("SQLite Query - Research Fields:\n%s", rpWithFieldTable)
    for row in rpWithFieldTable:
        rp = row.rp.name
        suitability = row.suitability
        if rp in scoreBoard:
            scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'],suitability)
            scoreBoard[rp]['reasons'].append(row.research_field.field_name)
        else:
            scoreBoard[rp] = {'score': 1, 'reasons': [row.research_field.field_name]}
    return scoreBoard

def calculate_score_jc(jobClassList,scoreBoard):
    """
    Calculates and gives points to rps based on the items in the jobClassList
    jobClassList: list of job classes the user selected
    scoreBoard: dict with RPs as keys and their scores as values
                if RP has not been assigned a value yet then it will not be in the dict
    return: returns the updated scoreboard
    """
    # Set the parameters used to filter the table
    filter = []
    for jobClass in jobClassList:
        filter.append((JobClass.class_name == f"{jobClass}"))
    
    # Combine the RpJobClass and JobClass tables, and 
    # Only select the ones that match the filter
    rpWithJobClass = (RpJobClass.select()
                                .join(JobClass, on=(RpJobClass.job_class==JobClass.id))
                                .where(reduce(operator.or_,filter))).select()
    query_logger.info("SQLite Query - Job Classes:\n%s", rpWithJobClass)
    for row in rpWithJobClass:
        rp = row.rp.name
        suitability = row.suitability
        if rp in scoreBoard:
            scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'],suitability)
            scoreBoard[rp]['reasons'].append(row.job_class.class_name)
        else:
            scoreBoard[rp] = {'score': 1, 'reasons': [row.job_class.class_name]}
    
    return(scoreBoard)

def calculate_score_software(softwareList,scoreBoard):
    """
    Calculates and gives points to rps based on the items in the softwareList
    softwareList: list of softwares the user selected
    scoreBoard: dict with RPs as keys and their scores as values
                if RP has not been assigned a value yet then it will not be in the dict
    return: returns the updated scoreboard
    """
    # Set the parameters used to filter the table
    filter = []
    for software in softwareList:
        filter.append((Software.software_name == f"{software}"))
    
    # Combine the RpSoftware and Software tables, and 
    # Only select the ones that match the filter
    rpWithSoftware = (RpSoftware.select()
                                .join(Software, on=(RpSoftware.software==Software.id))
                                .where(reduce(operator.or_,filter))).select()
    query_logger.info("SQLite Query - Softwares:\n%s", rpWithSoftware)
    for row in rpWithSoftware:
        rp = row.rp.name
        suitability = row.suitability
        if rp in scoreBoard:
            scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'],suitability)
            scoreBoard[rp]['reasons'].append(row.software.software_name)
        else:
            scoreBoard[rp] = {'score': 1, 'reasons': [row.software.software_name]}

    return(scoreBoard)

def classify_rp_storage(storageType):
    """
    Classifies RPs into three categories: less-than-1, 1-10, more-than-10,
        based on their storage (in TB)
    (These categories directly correspond to the values gotten from the form)
    storageType: must be "long-term" or "scratch" for what type of storage needs to be classified
    returns a dict with each category as the key as a list of RP names that fit
        that categories as the values
    """
    
    classifiedRps = {}
    
    if storageType == "long-term":
        ltOneTb = RPS.select().where(RPS.longterm_tb < 1.0)
        oneToTenTb = RPS.select().where((RPS.longterm_tb >= 1.0) & (RPS.longterm_tb< 10.0))
        mtTenTb = RPS.select().where(RPS.longterm_tb >= 10.0)

    elif storageType == "scratch":
        ltOneTb = RPS.select().where(RPS.scratch_tb < 1.0)
        oneToTenTb = RPS.select().where((RPS.scratch_tb >= 1.0) & (RPS.scratch_tb< 10.0))
        mtTenTb = RPS.select().where(RPS.scratch_tb >= 10.0)

    classifiedRps["less-than-1"] = [rp.name for rp in ltOneTb]
    classifiedRps["1-10"] = [rp.name for rp in oneToTenTb]
    classifiedRps["more-than-10"] = [rp.name for rp in mtTenTb]

    return classifiedRps



def get_recommendations(formData):
    scoreBoard = {}
    yes = '1'
    # If user has not used an hpc before
    if formData.get("hpc-use") == '0':
        rpsWithGui = RpGUI.select()
        rpNames = list({rp.rp.name for rp in rpsWithGui})
        # increase score for all rps with a GUI
        for rp in rpNames:
            if rp in scoreBoard:
                scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'])
                scoreBoard[rp]['reasons'].append("GUI")
            else:
                scoreBoard[rp] = {'score': 1, 'reasons': ["GUI"]}

    # If user has used ACCESS hpc
    elif formData.get("used-hpc"):
        # increase score for all ACCESS RPs user has experience with
        for rp in formData.get("used-hpc"):
            if rp in scoreBoard:
                scoreBoard[rp]['score'] += 1
                scoreBoard[rp]['reasons'].append("User Experience")
            else:
                scoreBoard[rp] = {'score': 1, 'reasons': ["User Experience"]}
    
    # Research Field
    researchFields = formData.get("research-field")
    researchFieldList = researchFields.split(",")

    if researchFieldList:
        scoreBoard = calculate_score_rf(researchFieldList,scoreBoard)
    
    # Job Class
    jobClasses = formData.get("job-class")
    jobClassList = jobClasses.split(",")
    if jobClasses:
        scoreBoard = calculate_score_jc(jobClassList, scoreBoard)

    # Storage
    storageNeeded = formData.get("storage")
    if storageNeeded:
        ## TODO: Need to get data for i-nodes and calculates scores accordingly here:
        numFiles = formData.get("num-files")
        
        longTermStorageNeeded = formData.get("long-term-storage")
        scratchStorageNeeded = formData.get("temp-storage")

        if (longTermStorageNeeded != "unsure" and longTermStorageNeeded) :
            storageType = "long-term"
            classifiedRpsLt = classify_rp_storage(storageType)
            for rp in classifiedRpsLt[longTermStorageNeeded]:
                if rp in scoreBoard:
                    scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'])
                    scoreBoard[rp]['reasons'].append("Long Term Storage")
                else:
                    scoreBoard[rp] = {'score': 1, 'reasons': ["Long Term Storage"]}

        if (scratchStorageNeeded and scratchStorageNeeded != "unsure"):
            storageType = "scratch"
            classifiedRpsScratch = classify_rp_storage(storageType)
            for rp in classifiedRpsScratch[scratchStorageNeeded]:
                if rp in scoreBoard:
                    scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'])
                    scoreBoard[rp]['reasons'].append("Scratch Storage")
                else:
                    scoreBoard[rp] = {'score': 1, 'reasons': ["Scratch Storage"]}
    # Memory (RAM)
    memoryNeeded = formData.get("memory")
    # TODO: add scoring system after the memory data has been added to the db
    if memoryNeeded:
        pass

    # Software
    softwares = formData.get("software")
    if softwares:
        softwareList = softwares.split(",")
        if softwareList:
            scoreBoard = calculate_score_software(softwareList, scoreBoard)

    # Graphics
    graphicsNeeded = formData.get("graphics")
    # TODO: add scoring after the graphics data has been added to the db
    if graphicsNeeded == yes:
        graphicalRps = RPS.select().where(RPS.graphical > 0)
        for rp in graphicalRps:
            suitability = rp.graphical
            if rp.name in scoreBoard:
                scoreBoard[rp.name]['score['] = calculate_points(scoreBoard[rp.name]['score'], suitability)
                scoreBoard[rp.name]['reasons'].append("Graphics")
            else:
                scoreBoard[rp.name] = {'score': 1 * suitability, 'reasons': ["Graphics"]}

    # CPU and GPU in parallel
    CpuGpuParallelNeeded = formData.get("cpu-gpu-parallel")
    if (CpuGpuParallelNeeded and int(CpuGpuParallelNeeded) != 0):
        parallelRPs = RPS.select().where(RPS.parallel > 0)
        parallelRpNames = [rp.name for rp in parallelRPs]
        
        for rp in parallelRpNames:
            if rp in scoreBoard:
                scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'])
                scoreBoard[rp]['reasons'].append("CPU/GPU Parallel Processing")
            else:
                scoreBoard[rp] = {'score': 1, 'reasons': ["CPU/GPU Parallel Processing"]} 


    # Job needs to be running always
    alwaysRunningNeeded = formData.get("job-run")
    if alwaysRunningNeeded == yes:
        arRps = RPS.select().where(RPS.always_running > 0)
        for rp in arRps:
            suitability = rp.always_running * 4
            if rp.name in scoreBoard:
                scoreBoard[rp.name]['score'] = calculate_points(scoreBoard[rp.name]['score'],suitability)
                scoreBoard[rp.name]['reasons'].append("Always Running")
            else:
                scoreBoard[rp.name] = {'score': 1*suitability, 'reasons': ["Always Running"]}

    # Virtual machine
    VmNeeded = formData.get("vm")
    if VmNeeded == yes:
        vmRps = RPS.select().where(RPS.virtual_machine > 0)
        for rp in vmRps:
            suitability = rp.virtual_machine * 4
            if rp.name in scoreBoard:
                scoreBoard[rp.name]['score'] = calculate_points(scoreBoard[rp.name]['score'],suitability)
                scoreBoard[rp.name]['reasons'].append("Virtual Machine")
            else:
                scoreBoard[rp.name] = {'score': 1*suitability, 'reasons': ["Virtual Machine"]}
    query_logger.info('Recommendation Scoreboard:\n%s', scoreBoard)
    return scoreBoard

