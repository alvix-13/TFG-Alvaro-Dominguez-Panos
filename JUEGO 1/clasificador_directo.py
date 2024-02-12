import pickle
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds
import numpy as np
from mindrove.data_filter import DataFilter, NoiseTypes
import pandas as pd
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

modelo_final = pickle.load(open('MEJOR MODELO/modelo_XGB.pkl','rb'))

hora_actual = datetime.now().strftime("%H-%M-%S")
csv_file = f'DATOS DIRECTO/datos_{hora_actual}.csv'

columnas = ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8", "AccX", "AccY", "AccZ", "GyX", "GyY", "GyZ", "TimeStamp", "label"]

with open(csv_file, 'a', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(columnas)

window_size = 0.25  
num_points = int(window_size * sampling_rate)

contador_predicciones_iguales = 0
prediccion_anterior = None
gestos = {0: 'idle', 1: 'palma', 2: 'pronacion', 3: 'supinacion'}

def escalar_datos(datos, factor):
    filas, columnas = datos.shape
    for i in range(filas):
        for j in range(columnas):
            datos[i, j] *= factor
            
def mav(datos):
   return np.mean(np.abs(datos), axis=1)

def execute():
    while True:
        global prediccion_anterior, contador_predicciones_iguales, gestos
        if board_shim.get_board_data_count() >= num_points:
            data = board_shim.get_current_board_data(num_points)

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

            data = [item for sublist in data_clasificar for item in sublist]

            nombres_entrenamiento = ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8", "AccX", "AccY", "AccZ", "GyX", "GyY", "GyZ"]
            datos_prediccion_array = np.array(data, dtype=float) 
            datos_prediccion_array = datos_prediccion_array.reshape(1, -1)

            if datos_prediccion_array.shape[1] == len(nombres_entrenamiento):
                datos_prediccion_array = pd.DataFrame(datos_prediccion_array, columns=nombres_entrenamiento)
                prediccion = modelo_final.predict(datos_prediccion_array)[0]

                csv_data = data_clasificar + [[timestamp_modificado]] + [[prediccion]]

                with open(csv_file, 'a', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow([item for sublist in csv_data for item in sublist])

            if prediccion == prediccion_anterior:
                contador_predicciones_iguales += 1
            else:
                contador_predicciones_iguales = 0
            
            prediccion_anterior = prediccion

            if contador_predicciones_iguales == 1:
                
                return prediccion

