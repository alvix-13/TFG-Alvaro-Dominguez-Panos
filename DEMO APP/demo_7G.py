import pickle
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds
import numpy as np
from mindrove.data_filter import DataFilter, NoiseTypes
import pandas as pd
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
from datetime import datetime


BoardShim.enable_dev_board_logger()
params = MindRoveInputParams()
board_id = BoardIds.MINDROVE_WIFI_BOARD
board_shim = BoardShim(board_id, params)

board_shim.prepare_session()
board_shim.start_stream()

emg_channels = BoardShim.get_emg_channels(board_id)
accel_channels = BoardShim.get_accel_channels(board_id)
gyro_channels = BoardShim.get_gyro_channels(board_id)
sampling_rate = BoardShim.get_sampling_rate(board_id)
package_num = BoardShim.get_package_num_channel(board_id)
time_channel = BoardShim.get_timestamp_channel(board_id)

modelo_final = pickle.load(open('ENTRENAMIENTOS RELEVANTES/BEST FASE 1/modelo_LR.pkl','rb'))

hora_actual = datetime.now().strftime("%H-%M-%S")
csv_file = f'DATOS DIRECTO/datos_{hora_actual}.csv'

columnas = ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8", "AccX", "AccY", "AccZ", "GyX", "GyY", "GyZ", "TimeStamp"]

with open(csv_file, 'a', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(columnas)

window_size = 0.25  
num_points = int(window_size * sampling_rate)

contador_predicciones_iguales = 0
prediccion_anterior = None

fig, ax = plt.subplots()
fig.canvas.manager.set_window_title("DEMO")
gestos = {0: 'idle', 1: 'puño', 2: 'palma', 3: 'flexion', 4: 'extension',  5: 'pronacion', 6: 'supinacion'}
predic = [0, 0, 0, 0, 0, 0, 0]
bar_colors = ['red', 'blue', 'green', 'yellow', 'pink', 'orange', 'purple']
bar_chart = ax.bar(list(gestos.keys()), predic, color=bar_colors)
ax.set_xticks(list(gestos.keys()))
ax.set_xticklabels(list(gestos.values()))
ax.set_ylim(0, 1)
ax.set_ylabel("Gesto activo")
ax.set_title("Predicción en Tiempo Real")


def init():
    for barra in bar_chart:
        barra.set_height(0)
    return bar_chart

def escalar_datos(datos, factor):
    filas, columnas = datos.shape
    for i in range(filas):
        for j in range(columnas):
            datos[i, j] *= factor
            
def mav(datos):
   return np.mean(np.abs(datos), axis=1)

def update(frame):
    global prediccion_anterior, contador_predicciones_iguales
    if board_shim.get_board_data_count() >= num_points:
        data = board_shim.get_current_board_data(num_points)
        #data = board_shim.get_board_data(num_points)

        for count, channel in enumerate(emg_channels):
            DataFilter.remove_environmental_noise(data[channel], sampling_rate, NoiseTypes.FIFTY.value)

        emg_data = data[emg_channels]
        accel_data = data[accel_channels]
        gyro_data = data[gyro_channels]
        time_data = data[time_channel]

        dt_object = datetime.fromtimestamp(time_data[0])
        timestamp_modificado = dt_object.strftime("%M:%S.%f")

        escalar_datos(emg_data, 0.045)
        escalar_datos(accel_data, 0.01526)
        escalar_datos(gyro_data, 0.000061035)

        mav_emg = mav(emg_data)
        mav_accel = mav(accel_data)
        mav_gyro = mav(gyro_data)

        data_clasificar = [mav_emg] + [mav_accel] + [mav_gyro]

        csv_data = data_clasificar + [[timestamp_modificado]]

        with open(csv_file, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([item for sublist in csv_data for item in sublist])


        data = [item for sublist in data_clasificar for item in sublist]

        nombres_entrenamiento = ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8", "AccX", "AccY", "AccZ", "GyX", "GyY", "GyZ"]
        datos_prediccion_array = np.array(data, dtype=float) 
        datos_prediccion_array = datos_prediccion_array.reshape(1, -1)

        if datos_prediccion_array.shape[1] == len(nombres_entrenamiento):
            datos_prediccion_array = pd.DataFrame(datos_prediccion_array, columns=nombres_entrenamiento)
            prediccion = modelo_final.predict(datos_prediccion_array)[0]

        predicciones = [0] * len(gestos)
        predicciones[prediccion] = 1
        print(prediccion)

        if prediccion == prediccion_anterior:
                contador_predicciones_iguales += 1
        else:
            contador_predicciones_iguales = 0
        
        prediccion_anterior = prediccion

        if contador_predicciones_iguales == 1:
            
            for height, bar, gesture in zip(predicciones, bar_chart, gestos.values()):
                bar.set_height(height)
                bar.set_label(gesture)
            
        return bar_chart


try:
    ani = FuncAnimation(fig, update, init_func=init, blit=False, cache_frame_data=False)
    plt.show()

except KeyboardInterrupt:
        print("Se detectó un KeyboardInterrupt. Saliendo...")
        sys.exit(0)
        
