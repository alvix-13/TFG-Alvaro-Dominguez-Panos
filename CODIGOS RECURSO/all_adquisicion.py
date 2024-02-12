import adquisicion
from time import sleep

def todos_experimentos(csv_file, label, win_size, current=False):
    guia("reposo" if label == 0 else
         "puño" if label == 1 else
         "palma" if label == 2 else
         "flexion" if label == 3 else
         "extension" if label == 4 else
         "pronacion" if label == 5 else
         "supinacion")

    csv_path = f' {csv_file}' if current else f' {csv_file}'
    adquisicion.ejecutar_experimento(csv_path, label, win_size, current)

def fin():
    print("======================================")
    print("\n\n\n\n\n")
    print(f"FIN DE LA ADQUISICIÓN")
    print("\n\n\n\n\n")
    print("======================================")
    sleep(60)

def guia(gesto):
    print("======================================")
    print("\n\n\n\n\n")
    print(f"PREPARA {gesto} 20")
    print("\n\n\n\n\n")
    print("======================================")
    sleep(17)
    print("3")
    sleep(1)
    print("2")
    sleep(1)
    print("1")
    sleep(1)
    print("GOOOOOO")
    sleep(1)

experiments = [
    ('idle11.csv', 0),
    ('puño11.csv', 1),
    ('palma11.csv', 2),
    ('flex11.csv', 3),
    ('ext11.csv', 4),
    ('pro11.csv', 5),
    ('sup11.csv', 6)
]

win_sizes = [0.25, 0.15, 0.01]
current = [False, False, False, True, True, True]

for win_size in win_sizes:
    for is_current in current:
        for csv_file, label in experiments:
            todos_experimentos(csv_file, label, win_size, is_current)
        fin()
