from models.rpGUI import RpGUI

def calculate_score(data):
    score = {}
    print("in calculate_score", data.get('hpc-use'))
    
    # If user has not used an hpc before
    if data.get("hpc-use") == '0':
        rpsWithGui = RpGUI.select()
        rpNames = [rp.rp.name for rp in rpsWithGui]
        # increase score for all rps with a GUI
        for rp in rpNames:
            if rp in score:
                score[rp] += 1
            else:
                score[rp] = 1
    elif data.getlist("used-hpc"):
        for rp in data.getlist("used-hpc"):
            if rp in score:
                score[rp] += 1
            else:
                score[rp] = 1
        print(data.getlist("used-hpc"))
    
    # print(data.getlist("used-hpc"))
    print(score)
        
    return " "

