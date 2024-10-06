import sys
import requests
import getopt
import time


def get_mac(address):
    url = f"https://api.macvendors.com/{address}"
    
    s_time = time.time()

    response = requests.get(url)

    e_time = time.time()

    r_time = (e_time-s_time) * 1000

    if response.status_code == 200:
        print("MAC adress: ", address)
        print("Fabricante: ", response.text)
        print(f'Tiempo de respuesta: {r_time:.2f}ms')
        sys.exit()
        
    if address is None:
        print("Por favor, proporciona una dirección MAC con el argumento --mac")
        sys.exit(2)

    else:
        print("MAC adress: ", address)
        print("Fabricante: ", "Not found")
        print(f'Tiempo de respuesta: {r_time:.2f}ms')
        sys.exit()
    
    
    

def help():
    print('''Use: ./OUILookup --mac <mac> | --arp | [--help]\n
          --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.\n
          --arp: muestra los fabricantes de los host disponibles en la tabla arp.\n
          --help: muestra este mensaje y termina.''')
    sys.exit()


def arp():
    print('hola')
    sys.exit()


def main(argv):
    try:
        opts, argv =getopt.getopt(argv, "", ['mac=', "help", "arp"])
    except getopt.GetoptError:
        print('Error: use --help para ver modo de uso')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--mac':
            address= arg
            get_mac(address)
        elif opt == '--help':
            help()
        elif opt == '--arp':
            
            arp()
            

if __name__ == "__main__":
    main(sys.argv[1:])