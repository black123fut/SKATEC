import random
from Dictionaries import *
from Connections import *
from Utils import *

# Funciones-----------------------------------------------------------------
def crearCodigoProductoRandom():
    codigo = ""
    for j in range(9):
        codigo += str(random.randint(0, 9))
    return codigo


def GenerarCodigoArt(idProducto):
    return codigoArticulo[idProducto] + crearCodigoProductoRandom()


def insertarEnDB(rango, idPed, fecha, idArt, offset):
    for n in range(rango):
        idProd = n + offset
        cantidad = random.randint(5, 15)

        sqlInsertar = insertar["ListaSolicitud"] + "(" + str(idProd) + "," + str(idPed) + "," + str(cantidad) + ")"
        cursor.execute(sqlInsertar)
        conexion.commit()

        for p in range(cantidad):
            codigo = GenerarCodigoArt(idProd)
            sqlInsertar = insertar["Articulo"] + "(" + str(idArt) + ", %s,'embodegado', %s," + \
                          str(idProd) + ", " + str(random.randint(1,3)) + ")"
            cursor.execute(sqlInsertar, (codigo, fecha))
            conexion.commit()

            sqlInsertar = insertar["ListaRecibido"] + "(" + str(idArt) + "," + str(idPed) + ")"
            cursor.execute(sqlInsertar)
            conexion.commit()
            idArt += 1
    return idArt


sqlInsertar = "SELECT IdSolicitudPedido FROM SolicitudPedido"
cursor.execute(sqlInsertar)
idPed = len(cursor.fetchall()) + 1

sqlInsertar = "SELECT IdArticulo FROM Articulo"
cursor.execute(sqlInsertar)
idArt = len(cursor.fetchall()) + 1

for i in range(5):
    idProv = i + 1
    fecha = GenerarFecha()
    sqlInsertar = insertar["SolicitudPedido"] + "(" + str(idPed) + "," + str(idProv) + ",%s)"
    cursor.execute(sqlInsertar, (fecha,))
    conexion.commit()

    sqlInsertar = insertar["PedidoRecibido"] + "(" + str(idPed) + "," + str(idPed) + "," + str(idProv) + ", %s)"
    cursor.execute(sqlInsertar, (fecha,))
    conexion.commit()

    if i == 0:
        idArt = insertarEnDB(2, idPed, fecha, idArt, 1)

    elif i == 1:
        idArt = insertarEnDB(1, idPed, fecha, idArt, 3)

    elif i == 2:
        idArt = insertarEnDB(5, idPed, fecha, idArt, 4)

    elif i == 3:
        idArt = insertarEnDB(9, idPed, fecha, idArt, 9)

    elif i == 4:
        idArt = insertarEnDB(3, idPed, fecha, idArt, 18)

    idPed += 1

outfile1 = open('idPedido.txt', 'w')
outfile1.write(str(idPed))
outfile1.close()

outfile2 = open('idArticulo.txt', 'w')
outfile2.write(str(idArt))
outfile2.close()