#----------------------------FUNCIONES DE AYUDA Y COMPLEMENTO--------------------------------------------------

from .models import herramientas #Opciones
from decimal import Decimal


def obtenerIdProducto(nombre_herramientas):
    id_producto = herramientas.objects.get(nombre_herramientas=nombre_herramientas)
    resultado = id_producto.id

    return resultado

#def productoTieneIva(idProducto):



#def sacarIva(elemento):


#def ivaActual(modo):


def obtenerProducto(idHerramientas):
    herramientas = Herramientas.objects.get(id=idHerramientas)      
    return herramientas

