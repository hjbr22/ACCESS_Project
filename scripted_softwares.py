import os, glob
import json
import shutil
from subprocess import PIPE, run
import sys
import schedule
from datetime import datetime, time, timedelta
import time as tm
from selenium import webdriver
import credientials



#Access MobaXTerm, use an ssh to access the system, and run the command to collect the data
#Create a text file once we have access to the data and replace the corresponding text file that is in the 'softwares' directory
def software_collections():
    
    #Creating variables for the paths of the applications needed for every RP
    mobaXterm_path = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\MobaXterm"
    winSCP_path = "C:\Users\hjbro\Desktop\Computer Programs"
    chromedriver_path = "C:\Users\hjbro\Desktop\Computer Programs\chromedriver"
    driver_activate = webdriver.Chrome(executable_path=chromedriver_path)

    #Going through the RP's that use OpenOnDemand via Chrome and transferrring the files to my computer

    #Anvil
    driver_activate.get("https://portal-aces.hprc.tamu.edu/pun/sys/dashboard")
    
    username_searchbox = driver_activate.find_element_by_id("ACCES Username")
    username_searchbox.send_keys(credientials.username)

    password_searchbox = driver_activate.find_element_by_id("ACCES Password")
    password_searchbox.send_keys(credientials.password)

    driver_activate.implicitly_wait(10)

    


    #ssh_command_ookami = "ssh hbrogna@login.ookami.stonybrook.edu"
    #ssh_command_kryic = "ssh -i prKey.rsa hbrogna@kxc.ccs.uky.edupi"
    os.chdir('softwares')


 # Schedule the event of collecting the software data every day at 17:00 (5 pm)
schedule.every().days.at("17:00").do(software_collections)

#Making sure the program runs continuously
while True:
    schedule.run_pending()
    tm.sleep(1)