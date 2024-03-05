import tkinter as tk
import importlib
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds
from time import sleep
import threading


def ejecutar_clasificador():
    global ejecutando
    ejecutando = True
    
    modulo_clasificador = importlib.import_module("clasificador_directo")
    board_shim.prepare_session()
    board_shim.start_stream()

    while ejecutando:
        prediccion = modulo_clasificador.execute(board_id, board_shim)
        
        gestos = {0: 'idle', 1: 'palma', 2: 'pronacion', 3: 'supinacion'}
        texto_informativo.config(text=f"Predicción: {gestos[prediccion]}")
        
        ventana.update()

def ejecutar_entrenamiento(tipo):
    def entreno():
        modulo_adquirir = importlib.import_module("adquisicion")
        board_shim.prepare_session()
        board_shim.start_stream()

        for i in range(4):
            guia("reposo" if i == 0 else
               "palma" if i == 1 else
                "pronacion" if i == 2 else
                "supinacion")

            modulo_adquirir.ejecutar_experimento(board_id, board_shim, "APP/data/data_train.csv", i, 0.25, False)

        board_shim.stop_stream()
        board_shim.release_all_sessions()

        texto_informativo.config(text=f"Fin de la adquisición")
        sleep(3)

        texto_informativo.config(text=f"Inicio entrenamiento")

        modulo_entrenar = importlib.import_module("entrenamiento")       
        if tipo == "rapido":
            precision_entrenamiento, precision_generalizacion = modulo_entrenar.ejecutar_rapido("APP/data/data_train.csv")
        else:
            precision_entrenamiento, precision_generalizacion = modulo_entrenar.ejecutar("APP/data/data_train.csv")

        texto_informativo.config(text=f"Fin entrenamiento")
        sleep(2)
        texto_informativo.config(text=f"Resultado precisión entrenamiento {round(precision_entrenamiento, 3)}, \n y precisión real estimada {round(precision_generalizacion, 3)}")

    entrenamiento_thread = threading.Thread(target=entreno)
    entrenamiento_thread.start()

def entrenar_rapido():
    ejecutar_entrenamiento("rapido")

def entrenar():
    ejecutar_entrenamiento("completo")

def guia(gesto):
    texto_informativo.config(text=f"Prepara: {gesto} en 20 segundos")
    sleep(17)
    texto_informativo.config(text=f"{gesto} en 3 segundos")
    sleep(1)
    texto_informativo.config(text=f"{gesto} en 2 segundos")
    sleep(1)
    texto_informativo.config(text=f"{gesto} en 1 segundos")
    sleep(1)
    texto_informativo.config(text=f"GO")
    sleep(1)

# Función para detener la ejecución
def detener_ejecucion():
    global ejecutando
    if ejecutando:
        board_shim.stop_stream()
        board_shim.release_all_sessions()
        ejecutando = False
    else:
        pass

BoardShim.enable_dev_board_logger()
params = MindRoveInputParams()
board_id = BoardIds.MINDROVE_WIFI_BOARD
board_shim = BoardShim(board_id, params)

ejecutando = False

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Clasificador de gestos de la mano")
ventana.configure(bg="gray")

ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)
ventana.grid_columnconfigure(2, weight=1)
ventana.grid_columnconfigure(3, weight=1)
ventana.grid_rowconfigure(0, weight=1)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_rowconfigure(2, weight=1)
ventana.grid_rowconfigure(3, weight=1)

titulo = tk.Label(ventana, text="Clasificador de gestos de la mano", font=("Helvetica", 16, "bold"), bg="gray", fg="white")
titulo.grid(row=0, column=1, pady=20, padx=15)

boton_ejecutar = tk.Button(ventana, text="Ejecutar clasificador", command=ejecutar_clasificador, font=("Helvetica", 12, "bold"), bg="black", fg="white")
boton_entrenar_rapido = tk.Button(ventana, text="Entrenamiento rápido", command=entrenar_rapido, font=("Helvetica", 12, "bold"), bg="black", fg="white")
boton_entrenar = tk.Button(ventana, text="Entrenamiento completo", command=entrenar, font=("Helvetica", 12, "bold"), bg="black", fg="white")
boton_detener = tk.Button(ventana, text="Detener ejecución", command=detener_ejecucion, font=("Helvetica", 12, "bold"), bg="black", fg="white")

# Posicionar los botones con grid
boton_ejecutar.grid(row=1, column=0, pady=15, padx=15)
boton_detener.grid(row=3, column=0, pady=15, padx=15)
boton_entrenar.grid(row=1, column=2, pady=15, padx=15)
boton_entrenar_rapido.grid(row=3, column=2, pady=15, padx=15)

texto_informativo = tk.Label(text=f"", font=("Helvetica", 12, "bold"), bg="gray", fg="white")
texto_informativo.grid(row=2, column=1, pady=15, padx=15)

# Iniciar la aplicación
ventana.mainloop()