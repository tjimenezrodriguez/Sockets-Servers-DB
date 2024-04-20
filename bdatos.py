"""
Programación Paralela

Práctica 2: Sockets y arquitectura cliente-servidor

Integrantes: Álex Carrillo Delgado, Alonso Delgado Morales, Teófilo Jiménez Rodríguez.

"""

import threading  # a nuestra clase le hemos añadido directamente los bloqueos, para poder hacer un tratamiento seguro y compartimentado de la información
# esto corresponde al paso extra: bloqueo selectivo

class BaseDatos:
    def __init__(self) -> None:
        self.datos = {}
        self.locks = {}  # esto permite que cada clave tenga su propio objeto de bloqueo asociado
        self.lock_global = threading.Lock()  # bloqueo global para crear objetos de bloqueo sin problemas

    # creamos una función para tratar con los bloqueos: dada la clave, obtiene su objeto de bloqueo y si no tiene, lo crea
    # podríamos tener un problema si antes de tener dichos objetos de bloqueo se tratase de acceder simultáneamente a la misma clave
    # gracias al bloqueo global lo evitamos

    def _get_lock(self, clave: str) -> threading.Lock:
        with self.lock_global:
            if clave not in self.locks:
                self.locks[clave] = threading.Lock()
        return self.locks[clave]

    # dentro del diccionario cada clave tendrá su lista "valores" asociada.
    # podríamos haber trabajado con diccionarios, pero como tendríamos que haber determinado el nombre de las subcategorías (ej: DNI, fecha,...)
    # restando flexibilidad al código, al no poder tener distintos tipos de datos en la base ni distintas cantidades de atributos asociadas a una clave
    # (pues vendrían ya predeterminados), hemos preferido trabajar con listas y no tener esa limitación.
    def alta(self, clave: str, valores: [str]) -> str:
        with self._get_lock(clave):
            if clave not in self.datos:
                self.datos[clave] = valores
                return "El registro se ha añadido con éxito."
            else:
                return "La clave ya existía en la base de datos. Para modificar, use mod."

    def baja(self, clave: str) -> str:
        with self._get_lock(clave):
            if clave in self.datos:
                del self.datos[clave]
                return f"El registro asociado a '{clave}' se ha eliminado con éxito."
            else:
                return "La clave '{clave}' no existe en la base de datos."

    def modificacion(self, clave: str, valores: [str]) -> str:
        with self._get_lock(clave):
            if clave in self.datos:
                self.datos[clave] = valores
                return "El registro se ha modificado con éxito."
            else:
                return "La clave aportada no existe en la base de datos."

    def consulta(self, clave: str) -> str:
        with self._get_lock(clave):
            if clave in self.datos:
                resultado = ', '.join(self.datos[clave])
                return f"Los datos asociados a '{clave}' son: {resultado}"
            else:
                return f"La clave '{clave}' no existe en la base de datos."

    # para las dos siguientes funciones, sí usamos un bloqueo global, al ser acciones que afectan a todos los datos a la vez

    def copia(self) -> str:  # devuelve todos los datos que hay
        with self.lock_global:
            if self.datos:
                resultado = "\n".join(
                    f"Clave: {clave}, Valores: {', '.join(valores)}" for clave, valores in self.datos.items())
                return f"Los datos en la base de datos son:\n{resultado}"
            else:
                return "La base de datos está vacía."

    def borrar(self) -> str:      # borra todos los datos
        with self.lock_global:
            self.datos.clear()
        return "Todos los registros se han eliminado con éxito."


# Funciones auxiliares para las operaciones en la base de datos (simplifica notación para cuando se usen en servidor.py)

bdd = BaseDatos()


def alta(clave: str, valor: [str]) -> str:
    return bdd.alta(clave, valor)


def baja(clave: str) -> str:
    return bdd.baja(clave)


def modificacion(clave: str, valor: [str]) -> str:
    return bdd.modificacion(clave, valor)


def consulta(clave: str) -> str:
    return bdd.consulta(clave)


def copia() -> str:
    return bdd.copia()


def borrar() -> str:
    return bdd.borrar()