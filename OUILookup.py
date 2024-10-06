import sys
import requests
import getopt
import time
import csv
import os
import re

# Definir el nombre del archivo CSV
csv_file = 'mac_addresses.csv'

# Normalizar la dirección MAC al formato aa:bb:cc:dd:ee:ff
def normalize_mac(address):
    # Eliminar cualquier separador (puntos, guiones, espacios) y convertir a minúsculas
    address = re.sub(r'[^a-fA-F0-9]', '', address).lower()
    
    # Insertar dos puntos cada dos caracteres
    return ':'.join(address[i:i+2] for i in range(0, len(address), 2))

# Crear el archivo CSV si no existe
def create_csv():
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['prefix', 'manufacturer'])  # Encabezados

# Guardar el prefijo MAC y el fabricante en el archivo CSV, evitando duplicados
def save_mac_to_csv(prefix, manufacturer):
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        prefixes = [row['prefix'] for row in reader]
    
    if prefix in prefixes:
        print(f"Prefijo {prefix} ya está en el archivo.")
    else:
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([prefix, manufacturer])
            print(f"Prefijo {prefix} y fabricante {manufacturer} guardados en el archivo.")

# Obtener el fabricante de la API y guardar en el archivo CSV (usando solo el prefijo MAC)
def get_mac(address):

    address = normalize_mac(address)

    # Extraer los caracteres de interes
    prefix = ":".join(address.split(":")[:3])
    url = f"https://api.macvendors.com/{address}"
    
    s_time = time.time()
    response = requests.get(url)
    e_time = time.time()
    r_time = (e_time - s_time) * 1000

    if response.status_code == 200:
        manufacturer = response.text.strip()
        print("Prefijo MAC: ", prefix)
        print("Fabricante: ", manufacturer)
        print(f'Tiempo de respuesta: {r_time:.2f}ms')
        
        save_mac_to_csv(prefix, manufacturer)
    else:
        print("Prefijo MAC: ", prefix)
        print("Fabricante: Not found")
        print(f'Tiempo de respuesta: {r_time:.2f}ms')

# Mostrar los fabricantes y los prefijos MAC del archivo CSV
def arp():
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        entries = list(reader)

    if entries:
        print("Fabricantes y sus respectivos prefijos MAC:")
        for row in entries:
            print(f"{row['prefix']} - {row['manufacturer']}")
    else:
        print("No se encontraron entradas en el archivo.")

# Función de ayuda
def help():
    print('''Use: ./OUILookup --mac <mac> | --arp | [--help]
          --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.
          --arp: muestra los fabricantes de los hosts disponibles en el archivo CSV.
          --help: muestra esta ayuda.
    ''')

# Manejo de argumentos de línea de comandos
if __name__ == "__main__":
    create_csv()  # Crear el archivo CSV si no existe
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["mac=", "arp", "help"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--mac":
            get_mac(arg)
        elif opt == "--arp":
            arp()
        elif opt == "--help":
            help()
