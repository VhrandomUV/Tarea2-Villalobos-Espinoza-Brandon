"""
intengrantes 

Brandon Villalobos ||   brandon.villalobos@alumos.uv.cl
Benjamin González  ||   benjamin.gonzalez@alumos.uv.cl
David Bombal       ||   david.bombal@alumos.uv.cl
"""

import sys
import requests
import getopt
import time
import re
import subprocess


# Definir el nombre del archivo CSV
csv_file = 'mac_addresses.csv'

# Normalizar la dirección MAC al formato aa:bb:cc:dd:ee:ff


# Obtener el fabricante de la API y guardar en el archivo CSV (usando solo el prefijo MAC)
def get_mac(address):

    # Extraer los caracteres de interes
    
    url = f"https://api.maclookup.app/v2/macs/{address}/company/name"
    
    
    response = requests.get(url)
    manufacturer = response.text.strip()
    

    if response.status_code == 200 and manufacturer != "*NO COMPANY*":
       
        
        return manufacturer
        
        
    else:
        manufacturer = "Not found"
        
        return manufacturer

# Mostrar los fabricantes y los prefijos MAC del archivo CSV
def arp():
    resultado = subprocess.run(['arp', '-a'], capture_output=True, text=True)
    
    # Expresión regular para encontrar las direcciones MAC
    
    patron_mac = r'([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})'
    
    # Busca todas las coincidencias de direcciones MAC
    direcciones_mac = re.findall(patron_mac, resultado.stdout)
    
    # Las direcciones MAC se capturan como tuplas, así que las convertimos en strings
    direcciones_mac = [''.join(mac) for mac in direcciones_mac]
    for mac in direcciones_mac:
        
        print(f"MAC: {mac}  || Fabricante: {get_mac(mac)}")
    return direcciones_mac

# Función de ayuda
def help():
    print('''Use: ./OUILookup --mac <mac> | --arp | [--help]
          --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.
          --arp: muestra los fabricantes de los hosts disponibles en la tabla arp.
          --help: muestra esta ayuda.
    ''')

def main():
  
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["mac=", "arp", "help"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--mac":
            s_time = time.time()
            
            print("Dirección MAC: ", arg)
            print("Fabricante: ", get_mac(arg))
            e_time = time.time()
            r_time = (e_time - s_time) * 1000
            print(f'Tiempo de respuesta: {r_time:.2f}ms')

        elif opt == "--arp":
            arp()
        elif opt == "--help":
            help()



# Manejo de argumentos de línea de comandos
if __name__ == "__main__":
    main()
    
