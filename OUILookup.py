import sys
import requests
import getopt
import time
import csv
import os
import re
import subprocess

# Definir el nombre del archivo CSV
csv_file = 'mac_addresses.csv'

# Normalizar la dirección MAC al formato aa:bb:cc:dd:ee:ff
def normalize_mac(address):
    # Eliminar cualquier separador (puntos, guiones, espacios) y convertir a minúsculas
    address = re.sub(r'[^a-fA-F0-9]', '', address).lower()
    
    # Insertar dos puntos cada dos caracteres
    return ':'.join(address[i:i+2] for i in range(0, len(address), 2))

# Obtener el fabricante de la API y guardar en el archivo CSV (usando solo el prefijo MAC)
def get_mac(address):

    address = normalize_mac(address)

    # Extraer los caracteres de interes
    
    url = f"https://api.macvendors.com/{address}"
    
    s_time = time.time()
    response = requests.get(url)
    e_time = time.time()
    r_time = (e_time - s_time) * 1000

    if response.status_code == 200:
        manufacturer = response.text.strip()
        print("Dirección MAC: ", address)
        print("Fabricante: ", manufacturer)
        print(f'Tiempo de respuesta: {r_time:.2f}ms')
        
        
    else:
        print("Dirección MAC: ", address)
        print("Fabricante: Not found")
        print(f'Tiempo de respuesta: {r_time:.2f}ms')

# Mostrar los fabricantes y los prefijos MAC del archivo CSV
def arp():
    resultado = subprocess.run(['arp', '-a'], capture_output=True, text=True)
    
    # Expresión regular para encontrar las direcciones MAC
    patron_mac = r'([0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2})'
    
    # Busca todas las coincidencias de direcciones MAC
    direcciones_mac = re.findall(patron_mac, resultado.stdout)
    
    # Las direcciones MAC se capturan como tuplas, así que las convertimos en strings
    direcciones_mac = [''.join(mac) for mac in direcciones_mac]
    for mac in direcciones_mac:
        get_mac(mac)
    return direcciones_mac

# Función de ayuda
def help():
    print('''Use: ./OUILookup --mac <mac> | --arp | [--help]
          --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.
          --arp: muestra los fabricantes de los hosts disponibles en la tabla arp.
          --help: muestra esta ayuda.
    ''')

# Manejo de argumentos de línea de comandos
if __name__ == "__main__":
    
    
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
