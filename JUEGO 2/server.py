import tkinter as tk
import random
from socket import *
import threading

class RandomNumberGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego de Números Aleatorios")
        self.master.geometry("400x250") 
        
        self.intentos = 2
        self.aciertos = 0
        self.fallos = 0
        
        self.gestos = {0: 'idle', 1: 'palma', 2: 'pronacion', 3: 'supinacion'}
        
        self.random_label = tk.Label(master, text="Gesto aleatorio:", font=("Helvetica", 16))  
        self.random_label.pack()
        
        self.random_gesto_label = tk.Label(master, text="", font=("Helvetica", 20, "bold")) 
        self.random_gesto_label.pack()
        
        self.result_label = tk.Label(master, text="", font=("Helvetica", 16))  
        self.result_label.pack()
        
        self.gesto_recibido_title_label = tk.Label(master, text="Gesto recibido:", font=("Helvetica", 16, "bold"))  
        self.gesto_recibido_title_label.pack()
        
        self.gesto_recibido_label = tk.Label(master, text="", font=("Helvetica", 16))  
        self.gesto_recibido_label.pack()
        
        self.score_label = tk.Label(master, text="Aciertos: 0 | Fallos: 0", font=("Helvetica", 14))  
        self.score_label.pack()
        
        self.random_thread = threading.Thread(target=self.generar_gesto_random)
        self.random_thread.daemon = True
        self.random_thread.start()
        
        self.socket_thread = threading.Thread(target=self.receive_from_socket)
        self.socket_thread.daemon = True
        self.socket_thread.start()

    def generar_gesto_random(self):
        while True:
            numero_gesto_aleatorio = random.randint(0, 3)
            nombre_random = self.gestos[numero_gesto_aleatorio]
            self.random_gesto_label.config(text=nombre_random)
            self.master.update()
            threading.Event().wait(2)

    def receive_from_socket(self):        
        with socket(AF_INET, SOCK_STREAM) as sock:
            server_address = (gethostbyname(gethostname()), 10000)
            print('*** Server iniciado con IP %s en el puerto %s ***' % server_address)

            sock.bind(server_address)

            sock.listen(1)
            connection, client_address = sock.accept()

            with connection:
                print('Conexión establecida con', connection)
                while True:
                    data = connection.recv(1).decode()
                    gesto_recibido = int(data)
                    numero_gesto_aleatorio = next((key for key, value in self.gestos.items() if value == self.random_gesto_label.cget("text")), None)
                    self.gesto_recibido_label.config(text=f"{self.gestos[gesto_recibido]}")  # Mostrar el gesto recibido
                    if gesto_recibido == numero_gesto_aleatorio:
                        self.aciertos += 1
                        self.result_label.config(text="¡Correcto!")
                    else:
                        self.intentos -= 1
                        if self.intentos == 0:
                            self.fallos += 1
                            self.result_label.config(text="Fallo")
                            self.intentos = 2
                    self.update_score()

    def update_score(self):
        self.score_label.config(text=f"Aciertos: {self.aciertos} | Fallos: {self.fallos}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomNumberGame(root)
    root.mainloop()
