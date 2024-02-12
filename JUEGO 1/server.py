from socket import *
import threading as thread
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


sock = socket(AF_INET, SOCK_STREAM)

server_address = (gethostbyname(gethostname()), 10000)
print('*** Server iniciado con IP %s en el puerto %s ***' % server_address)

sock.bind(server_address)

sock.listen(1)


fig, ax = plt.subplots()
fig.canvas.manager.set_window_title("DEMO")
gestos = {0: 'idle', 1: 'palma', 2: 'pronacion', 3: 'supinacion'}
predic = [0, 0, 0, 0]
bar_colors = ['red', 'blue', 'green', 'yellow']
bar_chart = ax.bar(list(gestos.keys()), predic, color=bar_colors)
ax.set_xticks(list(gestos.keys()))
ax.set_xticklabels(list(gestos.values()))
ax.set_ylim(0, 1)
ax.set_ylabel("Gesto activo")
ax.set_title("Predicción en Tiempo Real")


def recibir_msg():
    while True:
        data = connection.recv(1).decode()
        data = int(data)
        predicciones = [0] * len(gestos)
        predicciones[data] = 1
        for height, bar in zip(predicciones, bar_chart):
            bar.set_height(height)
        update(predicciones)   

def init():
    for barra in bar_chart:
        barra.set_height(0)
    return bar_chart

def update(predicciones):
    return bar_chart
    

print('*** Esperando conexión ***')
connection, client_address = sock.accept()

print('Conectado desde:', client_address)
t1 = thread.Thread(target=recibir_msg)

anim = FuncAnimation(fig, update, init_func=init, blit=False, cache_frame_data=False)

try:
    t1.start()
    plt.show()
    
except KeyboardInterrupt:
    sock.close()


