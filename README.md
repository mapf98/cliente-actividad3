# Actividad 3 - Sistemas Distribuidos
## UCAB - Ing. Informática

Se elaboró un cliente con python para establecer una conexión a través del protocolo indicado.

# Pasos a seguir para ejecutar el cliente

+ Clonar el repositorio en su ruta de preferencia
```
git clone https://github.com/mapf98/cliente-actividad3.git
```

+ Ejecutar el script de python llamado cliente.py con el usuario correspondiente
```
py cliente.py mapena.16
```

+ Y por último ver el resultado de la ejecución

# Parametros de ejecucion opcionales

Para ver el listado de comandos disponibles se puede ejecutar el siguiente comando:
```
py cliente.py -h
```
o
```
py cliente.py --help
```

A continuación, los parámetros opcionales y requeridos para la ejecución del script:
```
Requeridos:
Nombre       Descripción
user_name    Nombre de usuario para establecer conexión con el server

Opcionales:
Reducido  Completo         Valor          (Por defecto)    Descripción
-cip      --client_ip      CLIENT_IP      10.2.126.99      IPv4 del cliente
-sip      --server-ip      SERVER_IP      10.2.126.2       IPv4 del servidor
-tp       --tcp-port       TCP_PORT       19876            Puerto TCP del servidor
-up       --udp-port       UDP_PORT       55350            Puerto UDP del cliente
-t        --timeout        TIMEOUT        20.0             Tiempo de espera para establecer la conexión en segundos
```

Ejemplo de uso:
```
py cliente.py mapena.16 -cip 10.2.126.110 -sip 10.2.126.30 -tp 17777 -up 34450 -t 20.5
```

## Creado por Miguel Peña C.I 26.530.119