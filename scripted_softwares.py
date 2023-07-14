import os, glob
import json
import shutil
from subprocess import PIPE, run
import sys
import schedule
from datetime import datetime, time, timedelta
import time as tm


#Access MobaXTerm, use an ssh to access the system, and run the command to collect the data
#Create a text file once we have access to the data and replace the corresponding text file that is in the 'softwares' directory
def software_collections():
    

    

    os.chdir('softwares')


 # Schedule the event of collecting the software data every day at 17:00 (5 pm)
schedule.every().days.at("17:00").do(software_collections)

#Making sure the program runs continuously
while True:
    schedule.run_pending()
    tm.sleep(1)