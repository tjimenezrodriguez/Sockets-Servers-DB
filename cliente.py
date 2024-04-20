from socket import socket

sckt = socket()
srvr_ip = 'localhost'
puerto = 12558
sckt.connect((srvr_ip, puerto))

print("Servicios disponibles:")
print("- may <cadena>")
print("- min <cadena>")
print("- inv <cadena>")
print("- bdd alta <clave> <dato1> <dato2>...")  # podemos añadir tantos argumentos como queramos asociados a una clave con alta/mod
print("- bdd baja <clave1> <clave2>...") # podemos dar de baja/consultar tantas claves como queramos de forma simultánea
print("- bdd mod <clave> <dato1> <dato2>...")
print("- bdd cons <clave1> <clave2>...")
print("- bdd copia")
print("- bdd borrar")
print("- salir")

peticion = input("¿Qué servicio solicitas?: ")
while peticion != 'salir':
    if peticion == 'bdd borrar':   # hemos añadido una confirmación extra, al ser la acción de borrar tan grave
        # podía haberse añadido en la creación de borrar, en bdatos.py, pero tiene más sentido hacerlo aquí en la interacción con el usuario
        confirmacion = input("Si desea borrar todos los registros escriba BORRAR. Esta acción es irreversible.\n")
        if confirmacion == 'BORRAR':
            msj_env = peticion.encode()
            sckt.send(msj_env)
        else:
            print("Operación cancelada.")
            peticion = input("¿Qué servicio solicitas?: ")
            continue
    else:
        msj_env = peticion.encode()
        sckt.send(msj_env)

    msj_rec = sckt.recv(1024)
    respuesta = msj_rec.decode()
    print(peticion + " -> " + respuesta)
    peticion = input("¿Qué servicio solicitas?: ")

sckt.close()
