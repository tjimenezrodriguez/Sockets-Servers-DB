"""
Programación Paralela

Práctica 2: Sockets y arquitectura cliente-servidor

Integrantes: Álex Carrillo Delgado, Alonso Delgado Morales, Teófilo Jiménez Rodríguez.

"""

from socket import socket
import threading
from bdatos import alta, baja, modificacion, consulta, copia, borrar

# primero creamos las acciones que puede hacer nuestro servidor:

def en_mayusc(frase: str) -> str:
    return frase.upper()

def en_minusc(frase: str) -> str:
    return frase.lower()

def invertir(frase: str) -> str:
    return frase[::-1]

# creamos dos diccionarios para la interacción con el cliente mediante fns y ops.
# obs: lo hacemos en 2 distintos porque funcionan de forma distinta.
# al tenerlo en diccionarios es muy modular, y se pueden añadir funciones fácilmente sin modificar apenas el resto del código.

fns = {'may': en_mayusc,
       'min': en_minusc,
       'inv': invertir}
ops = {'alta': alta,
       'baja': baja,
       'mod': modificacion,
       'cons': consulta,
       'copia': copia,
       'borrar': borrar}

def manejar_fns(fn: str, args: [str]) -> str:
    if fn in fns:
        resp = fns[fn](' '.join(args)) # lo hemos extendido para varias cadenas
    else:
        resp = "Esa operación no es válida." # manejo de errores
    return resp

# como tenemos tres tipos de operaciones, por su número de args, creamos tres funciones auxiliares que regulen los casos.
def manejar_altamod(op: str, args: [str]) -> str:
    if len(args) >= 2:
        clave, *datos = args
        resp = ops[op](clave,datos)
    else:
        resp = "Ese formato no es válido, faltan argumentos." # manejo de error de formato
    return resp

def manejar_bajacons(op: str, args: [str]) -> str:
    if len(args) >= 1:
        r = []
        for clave in args:
            resp = ops[op](clave)
            r.append(resp)
        resp = '\n'.join(r)
    else:
        resp = "Ese formato no es válido, mínimo se necesita una clave." # manejo de error de formato
    return resp

def manejar_copborr(op: str, args: [str]) -> str:
    if len(args) == 0:
        resp = ops[op]()
    else:
        resp = "Ese formato no es válido, copia y borrar no tienen argumentos adicionales." # manejo de error de formato
    return resp

def manejar_bdd(op: str, args: [str]) -> str:
    if op == 'alta' or op == 'mod':  # escribimos los casos concretos por legibilidad, pero podría hacerse más compacto haciendo dos subgrupos de ops para mayor modularidad.
        resp = manejar_altamod(op,args)
    elif op == 'baja' or op == 'cons':
        resp = manejar_bajacons(op,args)
    elif op == 'copia' or op == 'borrar':
        resp = manejar_copborr(op,args)
    else:
        resp = "Esa operación no es válida." # manejo de error de operaciones
    return resp
def manejar_cliente(cl_socket: socket) -> None:
    msj_rec = cl_socket.recv(1024)
    while msj_rec:
        msj =  msj_rec.decode()
        comando, *args = msj.split(' ') # obtengo la primera palabra en comando y lo demás a formato lista en args
        if comando == 'bdd':
            op, *args2 = args
            resp = manejar_bdd(op, args2)
        else:
            # fns
            resp = manejar_fns(comando, args)

        msj_env = resp.encode()
        cl_socket.send(msj_env)
        msj_rec = cl_socket.recv(1024)
    cl_socket.close()

# configuración del servidor

srvr_socket = socket()
ip_addr = 'localhost'
puerto = 12558

srvr_socket.bind((ip_addr, puerto))
srvr_socket.listen()

# ciclo principal
while True:
    cl_socket, _ = srvr_socket.accept()
    cliente_thread = threading.Thread(target=manejar_cliente, args=(cl_socket,))
    cliente_thread.start()