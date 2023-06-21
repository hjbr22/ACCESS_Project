from models.rpGUI import RpGUI
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from models.rps import RPS
import operator
from functools import reduce

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

    for row in rpWithFieldTable:
        rp = row.rp.name
        suitability = row.suitability
        if rp in scoreBoard:
            scoreBoard[rp] = calculate_points(scoreBoard[rp],suitability)
        else:
            scoreBoard[rp] = 1
    return scoreBoard

def calculate_score_jc(jobClassList,scoreBoard):
    """
    Calculates and gives points to rps based on the items in the jobClassList
    jobClassList: list of research fields the user selected
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

    for row in rpWithJobClass:
        rp = row.rp.name
        suitability = row.suitability
        if rp in scoreBoard:
            scoreBoard[rp] = calculate_points(scoreBoard[rp],suitability)
        else:
            scoreBoard[rp] = 1
    
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
    
    # If user has not used an hpc before
    if formData.get("hpc-use") == '0':
        rpsWithGui = RpGUI.select()
        rpNames = [rp.rp.name for rp in rpsWithGui]
        # increase score for all rps with a GUI
        for rp in rpNames:
            if rp in scoreBoard:
                scoreBoard[rp] = calculate_points(scoreBoard[rp])
            else:
                scoreBoard[rp] = 1  

    # If user has used ACCESS hpc
    elif formData.getlist("used-hpc"):
        # increase score for all ACCESS RPs user has experience with
        for rp in formData.getlist("used-hpc"):
            if rp in scoreBoard:
                scoreBoard[rp] += 1
            else:
                scoreBoard[rp] = 1
    
    # Research Field
    researchFieldList = formData.getlist("research-field")
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

        if longTermStorageNeeded != "unsure":
            storageType = "long-term"
            classifiedRpsLt = classify_rp_storage(storageType)
            for rp in classifiedRpsLt[longTermStorageNeeded]:
                if rp in scoreBoard:
                    scoreBoard[rp] = calculate_points(scoreBoard[rp])
                else:
                    scoreBoard[rp] = 1

        if scratchStorageNeeded != "unsure":
            storageType = "scratch"
            classifiedRpsScratch = classify_rp_storage(storageType)
            for rp in classifiedRpsScratch[scratchStorageNeeded]:
                if rp in scoreBoard:
                    scoreBoard[rp] = calculate_points(scoreBoard[rp])
                else:
                    scoreBoard[rp] = 1
    
    # Memory (RAM)
    memoryNeeded = formData.get("memory")
    # TODO: add scoring system after the memory data has been added to the db
    if memoryNeeded:
        pass

    # Software



    # Graphics
    graphicsNeeded = formData.get("graphics")
    # TODO: add scoring after the graphics data has been added to the db
    if graphicsNeeded:
        pass

    # CPU and GPU in parallel
    CpuGpuParallelNeeded = formData.get("cpu-gpu-parallel")
    if CpuGpuParallelNeeded:
        parallelRPs = RPS.select().where(RPS.parallel==True)
        parallelRpNames = [rp.name for rp in parallelRPs]

        for rp in parallelRpNames:
            if rp in scoreBoard:
                scoreBoard[rp] = calculate_points(scoreBoard[rp])
            else:
                scoreBoard[rp] = 1  


    # Job needs to be running always
    # TODO: add scoring after relevant data has been added to the db
    alwaysRunningNeeded = formData.get("always-running")
    if alwaysRunningNeeded:
        pass

    # Virtual machine
    # TODO: add scoring after relevant data has been added to the db
    VmNeeded = formData.get("vm-needed")
    if VmNeeded:
        pass

    
    return scoreBoard

