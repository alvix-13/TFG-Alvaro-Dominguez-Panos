from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds
import time
import numpy as np
from mindrove.data_filter import DataFilter, NoiseTypes
from datetime import datetime
import csv
import sys

def escalar_datos(datos, factor):
    filas, columnas = datos.shape
    for i in range(filas):
        for j in range(columnas):
            datos[i, j] *= factor

def mav(datos):
    return np.mean(np.abs(datos), axis=1)

def ejecutar_experimento(csv_file, label, window_size, usar_current=False):
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
    time_channel = BoardShim.get_timestamp_channel(board_id)

    np.set_printoptions(threshold=np.inf, linewidth=np.inf)

    num_points = int(window_size * sampling_rate)

    columnas = ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7", "CH8", "AccX", "AccY", "AccZ", "GyX", "GyY", "GyZ", "TimeStamp", "label"]

    with open(csv_file, 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(columnas)

    tiempo_limite = 4  # segundos
    tiempo_inicio = time.time()

    processed_timestamps = set()

    while time.time() - tiempo_inicio < tiempo_limite:
        try:
            if board_shim.get_board_data_count() >= num_points:
                if usar_current:
                    data = board_shim.get_current_board_data(num_points)
                else:
                    data = board_shim.get_board_data(num_points)

                for count, channel in enumerate(emg_channels):
                    DataFilter.remove_environmental_noise(data[channel], sampling_rate, NoiseTypes.FIFTY.value)

                emg_data = data[emg_channels]
                accel_data = data[accel_channels]
                gyro_data = data[gyro_channels]
                time_data = data[time_channel]

                dt_object = datetime.fromtimestamp(time_data[0])
                timestamp_modificado = dt_object.strftime("%M:%S.%f")

                if timestamp_modificado not in processed_timestamps:
                    escalar_datos(emg_data, 0.045)
                    escalar_datos(accel_data, 0.01526)
                    escalar_datos(gyro_data, 0.000061035)

                    mav_emg = mav(emg_data)
                    mav_accel = mav(accel_data)
                    mav_gyro = mav(gyro_data)

                    print(mav_emg)

                    csv_data = [mav_emg] + [mav_accel] + [mav_gyro] + [[timestamp_modificado]] + [[label]]

                    with open(csv_file, 'a', newline='') as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerow([item for sublist in csv_data for item in sublist])

                    processed_timestamps.add(timestamp_modificado)

        except KeyboardInterrupt:
            print("Se detectó un KeyboardInterrupt. Ejecutando acciones antes de salir...")

            board_shim.stop_stream()
            board_shim.release_all_sessions()

            sys.exit(0)

    board_shim.stop_stream()
    board_shim.release_all_sessions()
