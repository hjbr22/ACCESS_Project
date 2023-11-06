import os
import json
import shutil
from subprocess import PIPE, run
import subprocess
import sys
import schedule
from datetime import datetime, time, timedelta
import time as tm
from selenium import webdriver
import credentials
import paramiko
from pexpect import pxssh  # Import pxssh for MobaXterm

# Define the SSH credentials for the WinSCP connection
winSCP_port = 22
ACCESS_username = credentials.username
ACCESS_password = credentials.password

# OOKAMI
OOKAMI_username = credentials.ookami_username
OOKAMI_password = credentials.ookami_password
OOKAMI_hostname = credentials.ookami_host
OOKAMI_text = 'ookami_modules.txt'

# Darwin
darwin_username = credentials.darwin_username
darwin_password = credentials.darwin_password
darwin_hostname = credentials.darwin_host
darwin_text = 'darwin_modules.txt'

# Anvil
anvil_website = "https://ondemand.anvil.rcac.purdue.edu/pun/sys/dashboard"

#Expanse
expanse_website = "https://portal.expanse.sdsc.edu/pun/sys/dashboard"

#Delta
delta_website = ""

# Stampede-2
stampede2_username = credentials.stampede2_username
stampede2_password = credentials.stampede2_password
stampede2_hostname = credentials.stampede2_host
stampede2_text = 'stampede-2_modules.txt'

#Bridges-2
bridges2_username = credentials.bridges2_username
bridges2_password = credentials.bridges2_password
bridges2_text = 'bridges-2_modules.txt'

#KyRIC
kyric_username = credentials.kyric_username
kyric_hostname = credentials.kyric_host
kyric_text = 'kyric_modules.txt'


# Access MobaXTerm and use SSH to access the system
def mobaXterm_access():
    try:
        # Replace these with the appropriate MobaXterm session information
        mobaXterm_host = credentials.kyric_hostname
        mobaXterm_username = credentials.kyric_username

        # Use subprocess to open MobaXTerm with SSH
        command = f'mobaxterm.exe -ssh {mobaXterm_username}@{mobaXterm_host}'
        subprocess.run(command, shell=True)

        # Optionally, perform any further operations on MobaXTerm

    except Exception as e:
        print(f"An error occurred while accessing MobaXTerm: {e}")


#Accessing WIN SCP to be able to get the information for Stampede-2, Darwin, and OOKAMI
def winscp_access():
    try:
        # Set up a WinSCP connection
        winscp_path = r"C:\Users\hjbro\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\WinSCP\WinSCP.exe"

        # Access Stampede-2 connection and transfer the text file over using WinSCP
        stampede2_command = f'{winscp_path} sftp://{ACCESS_username}:{ACCESS_password}@{stampede2_hostname}:{winSCP_port}'
        stampede2_command += f' /command "put {stampede2_text} {stampede2_text}"'
        subprocess.run(stampede2_command, shell=True)

        # Access Darwin connection and transfer the text file over using WinSCP
        darwin_command = f'{winscp_path} sftp://{darwin_username}:{darwin_password}@{darwin_hostname}:{winSCP_port}'
        darwin_command += f' /command "put {darwin_text} {darwin_text}"'
        subprocess.run(darwin_command, shell=True)

        # Access OOKAMI connection and transfer the text file over using WinSCP
        ookami_command = f'{winscp_path} sftp://{OOKAMI_username}:{OOKAMI_password}@{OOKAMI_hostname}:{winSCP_port}'
        ookami_command += f' /command "put {OOKAMI_text} {OOKAMI_text}"'
        subprocess.run(ookami_command, shell=True)

        # Optionally, perform any text file processing or replacement here

    except Exception as e:
        print(f"An error occurred: {e}")

# Access MobaXTerm, use an SSH to access the system, and run the command to collect the data
def software_collections():
    try:
        # Access MobaXterm and collect data
        mobaXterm_access()

        # Create an SSH client for WinSCP connection
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname=kyric_hostname, port=winSCP_port, username=kyric_username)

        # Transfer the remote text file to local
        with ssh_client.open_sftp() as sftp:
            sftp.get(kyric_text, kyric_text)

        # Close the SSH connection
        ssh_client.close()

        #Access WIN SCP to be able to get the information for Stampede-2, Darwin, and OOKAMI


        # Optionally, perform any text file processing or replacement here

    except Exception as e:
        print(f"An error occurred: {e}")

# Access the Anvil website and transfer a file
def ondemand_access_and_transfer():
    try:
        # Set up a WebDriver for Chrome
        chromedriver_path = "C:\Users\hjbro\Desktop\Computer Programs\chromedriver"
        driver = webdriver.Chrome(executable_path=chromedriver_path)

        # Access the Anvil website
        driver.get(anvil_website)

        # You may need to interact with the website, e.g., login and navigate to the file you want to download using Selenium.

        
        username_field = driver.find_element_by_id('username_input_id')
        username_field.send_keys(ACCESS_username)

        password_field = driver.find_element_by_id('password_input_id')
        password_field.send_keys(ACCESS_password)

        login_button = driver.find_element_by_id('login_button_id')
        login_button.click()

        # Navigate to the file you want to files tab and then the "Home Directory" section underneath that tab

        files_tab = driver.find_element_by_id('Files')
        files_tab.click()
        home_directory_tab = driver.find_element_by_id('Home Directory')
        home_directory_tab.click()
        desktop_tab = driver.find_element_by_id('Desktop')
        desktop_tab.click()
        select_box_anvil_modules = driver.find_element_by_id('select_box_id')
        select_box_anvil_modules.click()

        #Click the download button in order to download the text file

        download_button = driver.find_element_by_id('Download')
        download_button.click()


        #Expanse
        driver.get(expanse_website)
        
        username_field = driver.find_element_by_id('username_input_id')
        username_field.send_keys(ACCESS_username)

        password_field = driver.find_element_by_id('password_input_id')
        password_field.send_keys(ACCESS_password)

        login_button = driver.find_element_by_id('login_button_id')
        login_button.click()

        # Navigate to the file you want to files tab and then the "Home Directory" section underneath that tab

        files_tab = driver.find_element_by_id('Files')
        files_tab.click()
        home_directory_tab = driver.find_element_by_id('Home Directory')
        home_directory_tab.click()
        desktop_tab = driver.find_element_by_id('Desktop')
        desktop_tab.click()
        select_box_anvil_modules = driver.find_element_by_id('select_box_id')
        select_box_anvil_modules.click()

        #Click the download button in order to download the text file

        download_button = driver.find_element_by_id('Download')
        download_button.click()


        #Delta

        driver.get(delta_website)

        username_field = driver.find_element_by_id('username_input_id')
        username_field.send_keys(ACCESS_username)

        password_field = driver.find_element_by_id('password_input_id')
        password_field.send_keys(ACCESS_password)

        login_button = driver.find_element_by_id('login_button_id')
        login_button.click()

        # Navigate to the file you want to files tab and then the "Home Directory" section underneath that tab

        files_tab = driver.find_element_by_id('Files')
        files_tab.click()
        home_directory_tab = driver.find_element_by_id('Home Directory')
        home_directory_tab.click()
        desktop_tab = driver.find_element_by_id('Desktop')
        desktop_tab.click()
        select_box_anvil_modules = driver.find_element_by_id('select_box_id')
        select_box_anvil_modules.click()

        #Click the download button in order to download the text file

        download_button = driver.find_element_by_id('Download')
        download_button.click()


    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the event of collecting the software data every day at 18:00 (6 pm)
schedule.every().day.at("18:00").do(software_collections)

# Making sure the program runs continuously
while True:
    schedule.run_pending()
    tm.sleep(1)

