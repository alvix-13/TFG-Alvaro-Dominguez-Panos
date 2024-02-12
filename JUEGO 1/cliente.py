from socket import *
import threading as thread
import clasificador_directo


sock = socket(AF_INET, SOCK_STREAM)

local_host = input("Introduce la IP del host: ")
server_address = (local_host, 10000)
print('Conectado al server con IP %s y puerto %s' % server_address)

sock.connect(server_address)

def mandar_msg():
    while True:
        message = clasificador_directo.execute()
        message = str(message)
        sock.sendall(message.encode())

t1 = thread.Thread(target=mandar_msg)

try:
    t1.start()
except KeyboardInterrupt:
    sock.close()
