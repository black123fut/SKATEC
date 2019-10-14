from Utils import *


def enviarAlTransporte(idSucursal, fecha, idProd, cantidad):
    totalLista = []
    sqlInsertar = insertar["Envio"] + "(%s" + ", " + str(idSucursal) + ")"
    cursor.execute(sqlInsertar, (fecha,))
    conexion.commit()

    numenvio = getLargoTablaPG("Envio")
    for i in range(20):
        rand, prod = (random.randint(1, 5), i + 1) if idProd == 0 else (cantidad, idProd)
        cursor.callproc("AgregarListaEnvio", (numenvio, idSucursal, rand, prod))
        conexion.commit()
        totalLista += [rand]

        if idProd != 0:
            break

    return totalLista


def solicitarMercaderia(fecha, mydb, mycursor):
    myInsert = insertarMySQL["SolicitudPedido"] + "(%s)"
    mycursor.execute(myInsert, (fecha,))
    mydb.commit()


def recibirEnSucursal(fecha, listaCantidades, sucursal, mydb, mycursor, idProd):
    ultimaSolicitud = getLargoTablaMySQL("SolicitudPedido", mycursor)
    myInsert = insertarMySQL["PedidoRecibido"] + "(" + str(ultimaSolicitud) + ", %s)"
    mycursor.execute(myInsert, (fecha,))
    mydb.commit()

    cursor.execute("SELECT * FROM ObtenerDireccionSucursal(" + str(sucursal) + ")")
    direccion = cursor.fetchall()
    print(direccion)
    for i in range(20):
        cont = str(i + 1) if idProd == 0 else str(idProd)
        myInsert = insertarMySQL["ListaSolicitud"] + "(" + cont + ", " + str(ultimaSolicitud) + ", " + \
                   str(listaCantidades[i]) + ")"
        mycursor.execute(myInsert)
        mydb.commit()

        sqlInsertar = "SELECT * FROM Articulo WHERE Estado = 'EnCamino' AND IdProducto = " + cont
        cursor.execute(sqlInsertar)
        articulos = unpackFecha(cursor.fetchall())

        for j in range(listaCantidades[i]):
            myInsert = insertarMySQL["Articulo"] + "(" + str(articulos[j][0]) + ", " + str(articulos[j][1]) + ", " + \
                       str(articulos[j][2]) + ", %s, %s, %s, %s, " + str(direccion[0][1]) + ")"
            mycursor.execute(myInsert, (articulos[j][3], 'Disponible', articulos[j][5], direccion[0][0]))
            mydb.commit()

            myInsert = insertarMySQL["ListaRecibido"] + "(" + str(articulos[j][0]) + ", " + str(ultimaSolicitud) + ")"
            mycursor.execute(myInsert)

        if idProd != 0:
            break

    # Cambia el estado de los articulos en bodega a disponibles
    cursor.callproc("ColocadosEnSucursal", ())


# Llena todas las sucursales con un poco de todos los productos
def llenarSucursales(fecha):
    for n in range(3):
        numSucursal = n + 1
        mydb, mycursor = getSucursal(numSucursal)

        solicitarMercaderia(fecha, mydb, mycursor)
        totalLista = enviarAlTransporte(numSucursal, fecha, 0, 0)
        recibirEnSucursal(fecha, totalLista, numSucursal, mydb, mycursor, 0)



llenarSucursales(datetime.datetime(2019, 10, 1).strftime('%Y-%m-%d'))


# Llena una sucursal espeifica con un producto y cantidad especifica
def pedirProductosBodega(nombreProd, categoria, idSucursal, cantidad):
    mydb, mycursor = getSucursal(idSucursal)
    fecha = time.strftime('%Y-%m-%d')

    idProducto = getIdProductoPG(nombreProd, categoria)[0][0]
    solicitarMercaderia(fecha, mydb, mycursor)
    totalLista = enviarAlTransporte(idSucursal, fecha, idProducto, cantidad)
    recibirEnSucursal(fecha, totalLista, idSucursal, mydb, mycursor, idProducto)
