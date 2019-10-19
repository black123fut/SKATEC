from Utils import *


# Funciones-----------------------------------------------------------------
def crearCodigoProductoRandom():
    codigo = ""
    for j in range(9):
        codigo += str(random.randint(0, 9))
    return codigo


def GenerarCodigoArt(idProducto):
    return codigoArticulo[idProducto] + crearCodigoProductoRandom()


def llenarArticulos(fecha, idProd, cantidad, idPed):
    idArticulo = getLargoTablaPG("Articulo") + 1
    for p in range(cantidad):
        codigo = GenerarCodigoArt(idProd)
        sqlInsertar = insertar["Articulo"] + "(" + str(idArticulo) + " , %s,'embodegado', %s," + str(idProd) + \
                      ", " + str(random.randint(1, 3)) + ")"
        cursor.execute(sqlInsertar, (codigo, fecha))
        conexion.commit()

        sqlInsertar = insertar["ListaRecibido"] + "(" + str(idArticulo) + ", " + str(idPed) + ")"
        cursor.execute(sqlInsertar)
        conexion.commit()
        idArticulo += 1


def insertarEnDB(rango, idPed, fecha, offset, cantidad):
    for n in range(rango):
        idProd = n + offset

        sqlInsertar = insertar["ListaSolicitud"] + "(" + str(idProd) + "," + str(idPed) + "," + str(cantidad) + ")"
        cursor.execute(sqlInsertar)
        conexion.commit()

        llenarArticulos(fecha, idProd, cantidad, idPed)


def abastecerBodega(cantidad):
    sqlInsertar = "SELECT IdSolicitudPedido FROM SolicitudPedido"
    cursor.execute(sqlInsertar)
    idPed = len(cursor.fetchall()) + 1
    tmpProveedor = 0
    count = 1
    for i in range(20):
        idProveedor, cantidadProductos = getProveedor(i + 1)
        fecha = time.strftime('%Y-%m-%d')
        sqlInsertar = insertar["SolicitudPedido"] + "(" + str(idPed) + "," + str(idProveedor) + ",%s)"
        cursor.execute(sqlInsertar, (fecha,))
        conexion.commit()

        sqlInsertar = insertar["PedidoRecibido"] + "(" + str(idPed) + "," + str(idPed) + "," + str(idProveedor) + ", " \
                                                                                                                  "%s)"
        cursor.execute(sqlInsertar, (fecha,))
        conexion.commit()
        if tmpProveedor != idProveedor:
            tmpProveedor = idProveedor
            count = i + 1
        insertarEnDB(cantidadProductos, idPed, fecha, count, cantidad)
        idPed += 1


def pedirArticulo(idProducto, cantidad):
    sqlInsertar = "SELECT IdSolicitudPedido FROM SolicitudPedido"
    cursor.execute(sqlInsertar)
    idPed = len(cursor.fetchall()) + 1
    fecha = time.strftime('%Y-%m-%d')
    idProveedor, cantidadProducto = getProveedor(idProducto)

    sqlInsertar = insertar["SolicitudPedido"] + "(" + str(idPed) + "," + str(idProveedor) + ",%s)"
    cursor.execute(sqlInsertar, (fecha,))
    conexion.commit()

    sqlInsertar = insertar["PedidoRecibido"] + "(" + str(idPed) + "," + str(idPed) + "," + str(idProveedor) + ", " \
                                                                                                              "%s)"
    cursor.execute(sqlInsertar, (fecha,))
    conexion.commit()

    sqlInsertar = insertar["ListaSolicitud"] + "(" + str(idProducto) + "," + str(idPed) + "," + str(cantidad) + ")"
    cursor.execute(sqlInsertar)
    conexion.commit()

    llenarArticulos(fecha, idProducto, cantidad, idPed)


def llenarArticulosAgotados():
    queryPG = 'SELECT * FROM CantidadArticulos()'
    cursor.execute(queryPG)
    productos = cursor.fetchall()

    listaproductos = []
    for i in range(len(productos)):
        if productos[i][1] < 45:
            faltantes = 100 - productos[i][1]
            pedirArticulo(productos[i][0], faltantes)
        listaproductos += [productos[i][0]]

    agotados = complementoLista(listaproductos)
    for i in range(len(agotados)):
        pedirArticulo(agotados[i], 100)


abastecerBodega(200)