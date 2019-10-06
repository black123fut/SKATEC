from Dictionaries import *
from Utils import *


def enviarAlTransporte(idSucursal, fecha):
    total = 0
    totalLista = []
    sqlInsertar = insertar["Envio"] + "(%s" + ", " + str(idSucursal) + ")"
    cursor.execute(sqlInsertar, (fecha,))
    conexion.commit()

    numenvio = getLargoTablaMySQL("Envio")
    for i in range(20):
        rand = random.randint(1, 5)
        cursor.callproc("AgregarListaEnvio", (idSucursal, numenvio, rand, i + 1))
        conexion.commit()
        total += rand
        totalLista += [rand]

    return totalLista


def solicitarMercaderia(fecha, mydb, mycursor):
    myInsert = insertarMySQL["SolicitudPedido"] + "(%s)"
    mycursor.execute(myInsert, (fecha,))
    mydb.commit()


def recibirEnSucursal(fecha, listaCantidades, sucursal, mydb, mycursor):
    ultimaSolicitud = getLargoTablaMySQL("SolicitudPedido")
    myInsert = insertarMySQL["PedidoRecibido"] + "(" + str(ultimaSolicitud) + ", %s)"
    mycursor.execute(myInsert, (fecha,))
    mydb.commit()

    cursor.execute("SELECT * FROM ObtenerDireccionSucursal(" + str(sucursal) + ")")
    direccion = cursor.fetchall()

    for i in range(20):
        idProd = str(i + 1)
        myInsert = insertarMySQL["ListaSolicitud"] + "(" + idProd + ", " + str(ultimaSolicitud) + ", " + \
                   listaCantidades[i] + ")"
        mycursor.execute(myInsert)
        mydb.commit()

        sqlInsertar = "SELECT * FROM Articulo WHERE Estado = 'EnCamino' AND IdProducto = " + idProd
        cursor.execute(sqlInsertar)
        articulos = unpackFecha(cursor.fetchall())

        for j in range(listaCantidades[i]):
            myInsert = insertarMySQL["Articulo"] + "(" + str(articulos[j][0]) + ", " + str(articulos[j][1]) + ", " + \
                       str(articulos[j][2]) + "%s, %s, %s, %s, " + str(direccion[1]) + ")"
            mycursor.execute(myInsert, (articulos[j][3], 'Disponible', articulos[j][5], direccion[0]))
            mydb.commit()

            myInsert = insertarMySQL["ListaRecibido"] + "(" + str(articulos[j][0]) + ", " + str(ultimaSolicitud) + ")"
            mycursor.execute(myInsert)

    #Cambia el estado de los articulos en bodega a disponibles
    cursor.callproc("ColocadosEnSucursal", ())


def llenarSucursales():
    for n in range(3):
        numSucursal = n + 1
        mydb, mycursor = getSucursal(numSucursal)
        fecha = GenerarFecha()
        solicitarMercaderia(fecha, mydb, mycursor)
        totalLista = enviarAlTransporte(numSucursal, fecha)
        recibirEnSucursal(fecha, totalLista, numSucursal, mydb, mycursor)