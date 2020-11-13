import argparse
import socket
from protocol import helloiam, msglen, givememsg, checksum, bye

# Se definen los parámetros requeridos y opcionales para la ejecución del cliente
parser = argparse.ArgumentParser()
parser.add_argument("user_name", help="Nombre de usuario para establecer conexión con el server.")
parser.add_argument("-cip", "--client_ip", help="IPv4 del cliente.", default='10.2.126.99')
parser.add_argument("-sip", "--server-ip", help="IPv4 del servidor.", default='10.2.126.2')
parser.add_argument("-tp", "--tcp-port", help="Puerto TCP del servidor.", default=19876, type=int)
parser.add_argument("-up", "--udp-port", help="Puerto UDP del cliente.", default=55350, type=int)
parser.add_argument("-t", "--timeout", help="Tiempo de espera para establecer la conexión en segundos.", default=20.0, type=float)
args = parser.parse_args()

# Variables globales
user_name = args.user_name
server = args.server_ip
client = args.client_ip
tcp_port = args.tcp_port
udp_port = args.udp_port
timeout = args.timeout

# Timeout para conexión
try:
  socket.setdefaulttimeout(timeout)
except ValueError as error:
  print(f'ERROR: timeout definido en un rango no aceptado [{error}]')
  exit()
except OverflowError as error:
  print(f'ERROR: timeout establecido no permitido [{error}]')
  exit()

# Creación de los sockets TCP y UDP
tpc_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Conexión de socket TCP y se habilita el socket UDP del cliente 
try:
  tpc_client.connect((server, tcp_port))
  udp_client.bind((client, udp_port))
except socket.error as error:
  print(f'ERROR: no se pudo establecer una conexión con el servidor [{error} in {timeout} seg]')
  udp_client.close()
  exit()
except OverflowError as error:
  print(f'ERROR: puerto definido fuera de rango [{error}]')
  udp_client.close()
  exit()

# Flujo de comunicación con el servidor
try:
  helloiam(tpc_client, user_name)
  msgLength = int(msglen(tpc_client))
  msg = givememsg(tpc_client, udp_client, udp_port, msgLength)
  checksum(tpc_client, msg)
  bye(tpc_client)
except ValueError as error:
  print(error)
except socket.timeout as error:
  print(f'ERROR: no se pudo establecer la conexión en el tiempo definido por defecto [{error} in {timeout}]')
finally:
  udp_client.close()