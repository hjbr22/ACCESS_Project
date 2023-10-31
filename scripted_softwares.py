import os
import json
import shutil
from subprocess import PIPE, run
import sys
import schedule
from datetime import datetime, time, timedelta
import time as tm
from selenium import webdriver
import credentials
import paramiko
from pexpect import pxssh  # Import pxssh for MobaXterm

# Define the host and SSH credentials for the WinSCP connection
winSCP_host = 'your_winscp_host'
winSCP_port = 22
ACCESS_username = credentials.username
ACCESS_password = credentials.password

# OOKAMI
OOKAMI_username = credentials.ookami_username
OOKAMI_password = credentials.ookami_password

# Darwin
darwin_username = credentials.darwin_username
darwin_password = credentials.darwin_password

# Anvil
anvil_website = "https://idp.access-ci.org/idp/profile/SAML2/Redirect/SSO?execution=e1s1"

# Define the local and remote paths for the text file
local_text_file = 'local_path_to_text_file.txt'
remote_text_file = 'remote_path_to_text_file.txt'

# Access MobaXTerm and use SSH to access the system
def mobaXterm_access():
    try:
        # Replace these with the appropriate MobaXterm session information
        mobaXterm_host = 'your_mobaxterm_host'
        mobaXterm_username = 'your_mobaxterm_username'
        mobaXterm_password = 'your_mobaxterm_password'

        # Create an SSH session using pxssh
        s = pxssh.pxssh()
        s.login(mobaXterm_host, mobaXterm_username, mobaXterm_password)

        # Run commands to collect data on MobaXterm
        # For example, you can run a command to copy files to a specific location
        s.sendline('cp source_file destination_directory')

        # Wait for the command to complete
        s.prompt()

        # Optionally, perform any further operations on MobaXterm

        # Logout from the MobaXterm session
        s.logout()

    except Exception as e:
        print(f"An error occurred while accessing MobaXterm: {e}")

# Access MobaXTerm, use an SSH to access the system, and run the command to collect the data
def software_collections():
    try:
        # Access MobaXterm and collect data
        mobaXterm_access()

        # Create an SSH client for WinSCP connection
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname=winSCP_host, port=winSCP_port, username=OOKAMI_username, password=OOKAMI_password)

        # Transfer the remote text file to local
        with ssh_client.open_sftp() as sftp:
            sftp.get(remote_text_file, local_text_file)

        # Close the SSH connection
        ssh_client.close()

        # Optionally, perform any text file processing or replacement here

    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the event of collecting the software data every day at 18:00 (6 pm)
schedule.every().day.at("18:00").do(software_collections)

# Making sure the program runs continuously
while True:
    schedule.run_pending()
    tm.sleep(1)

