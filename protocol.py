import base64
from hashlib import md5

BUFFER_SIZE = 4096
CHR_ENCODE_FORMART = 'utf-8'
UDP_ATTEMPTS = 10

def helloiam(TCPsocket, user):
  TCPsocket.send((f"helloiam {user}").encode(CHR_ENCODE_FORMART))
  auth = TCPsocket.recv(BUFFER_SIZE)
  if auth.decode(CHR_ENCODE_FORMART).rstrip('\n') == 'ok':
    print(f'\n--> {user} validado satisfactoriamente!\n    Respuesta del servidor: {auth.decode(CHR_ENCODE_FORMART)}')
  else:
    raise ValueError(f'ERROR: error para el usuario {user} [{auth.decode(CHR_ENCODE_FORMART)}]')

def msglen(TCPsocket):
  TCPsocket.send(("msglen").encode(CHR_ENCODE_FORMART))
  message_length = TCPsocket.recv(BUFFER_SIZE)
  response = list(message_length.decode(CHR_ENCODE_FORMART).rstrip('\n').split(" "))
  if response[0] == 'ok':
    print(f'--> Longitud del mensaje: {response[1]} bytes\n    Respuesta del servidor: {response[0]}')
    return response[1]
  else:
    raise ValueError(f'ERROR: error al obtener la longitud del mensaje [{message_length.decode(CHR_ENCODE_FORMART)}]')

def givememsg(TCPsocket, UDPsocket, UDPport, messageLength):
  attempt = 0
  verified = False
  get_message = 'givememsg ' + str(UDPport)
  TCPsocket.send((get_message).encode(CHR_ENCODE_FORMART))
  while UDP_ATTEMPTS > attempt:
    message = UDPsocket.recvfrom(BUFFER_SIZE)
    if len(base64.b64decode(message[0]).decode(CHR_ENCODE_FORMART)) != messageLength:
      print(f'--> Nuevo intento de recepción de paquetes UDP [Intento: {attempt}]')
      attempt += 1
    else:
      verified = True
      break

  if verified:
    print(f'\n--> Mensaje obtenido desde el servidor: {base64.b64decode(message[0]).decode(CHR_ENCODE_FORMART)}')
    return message[0]
  else:
    raise ValueError(f'ERROR: la longitud del mensaje no es igual a la esperada [{message[0].decode(CHR_ENCODE_FORMART)}]')

def checksum(TCPsocket, message):
  checksum = 'chkmsg ' + md5(base64.b64decode(message)).hexdigest()
  TCPsocket.send((checksum).encode(CHR_ENCODE_FORMART))
  checked = TCPsocket.recv(BUFFER_SIZE)
  if checked.decode(CHR_ENCODE_FORMART).rstrip('\n') == 'ok':
    print(f'\n--> Mensaje validado satisfactoriamente!\n    Respuesta del servidor: {checked.decode(CHR_ENCODE_FORMART)}')
  else:
    raise ValueError(f'ERROR: error al validar el mensaje obtenido desde el servidor [{checked.decode(CHR_ENCODE_FORMART)}]')

def bye(TCPsocket):
  end_connection = 'bye'
  TCPsocket.send((end_connection).encode(CHR_ENCODE_FORMART))
  response = TCPsocket.recv(BUFFER_SIZE)
  if response.decode(CHR_ENCODE_FORMART).rstrip('\n') == 'ok':
    print(f'--> Cierre de conexión con el servidor satisfactoria!\n    Respuesta del servidor: {response.decode(CHR_ENCODE_FORMART)}')
  else:
    raise ValueError(f'ERROR: error al cerrar la conexión con el servidor [{response.decode(CHR_ENCODE_FORMART)}]')
