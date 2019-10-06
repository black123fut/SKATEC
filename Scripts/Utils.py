import random
import datetime
from Connections import *


def GenerarFecha():
    anio = random.randint(2014, 2019)
    mes = random.randint(1, 12)
    dia = random.randint(1, 30)
    # fecha = anio + "-" + mes + "-" + dia
    fecha = datetime.datetime(anio, mes, dia)
    return fecha.strftime('%Y-%m-%d')


def getLargoTablaPG(nombre):
    sqlInsertar = "SELECT Id" + nombre + " FROM " + nombre
    cursor.execute(sqlInsertar)
    largo = len(cursor.fetchall())
    return largo


def getLargoTablaMySQL(nombre):
    sqlInsertar = "SELECT Id" + nombre + " FROM " + nombre
    mycursor.execute(sqlInsertar)
    largo = len(mycursor.fetchall())
    return largo


def unpackFecha(articulos):
    res = []
    for x in articulos:
        tmp = []
        for y in range(len(x)):
            if y == len(x) - 1:
                tmp += ['%s' % x[y],]
            else:
                tmp += [x[y]]
        res += [tuple(tmp)]

    return res


def GenerarDireccion():
    direccion = str(random.randint(50, 5000)) + "mts "
    num = random.randint(1, 4)
    if num == 1:
        direccion += "norte y "
    elif num == 2:
        direccion += "sur y "
    elif num == 3:
        direccion += "este y "
    else:
        direccion += "oeste y "

    direccion += str(random.randint(50, 500)) + "mts "

    num = random.randint(1, 4)
    if num == 1:
        direccion += "norte de "
    elif num == 2:
        direccion += "sur de "
    elif num == 3:
        direccion += "este de "
    else:
        direccion += "oeste de "

    num = random.randint(1, 4)
    if num == 1:
        direccion += "la escuela"
    elif num == 2:
        direccion += "la iglesia"
    elif num == 3:
        direccion += "la comisaria"
    elif num == 4:
        direccion += "el mercado central"
    elif num == 5:
        direccion += "el parque central"
    else:
        direccion += "el museo"

    return direccion