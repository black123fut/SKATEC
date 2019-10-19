from Utils import *
from GeneradorReportes import *

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
    for i in range(20):
        cont = str(i + 1) if idProd == 0 else str(idProd)

        sqlInsertar = "SELECT * FROM Articulo WHERE Estado = 'EnCamino' AND IdProducto = " + cont
        cursor.execute(sqlInsertar)
        articulos = unpackFecha(cursor.fetchall())

        myInsert = insertarMySQL["ListaSolicitud"] + "(" + cont + ", " + str(ultimaSolicitud) + ", " + \
                   str(len(articulos)) + ")"
        mycursor.execute(myInsert)
        mydb.commit()
        for j in range(len(articulos)):
            myInsert = insertarMySQL["Articulo"] + "(" + str(articulos[j][0]) + ", " + str(articulos[j][1]) + ", " + \
                       str(articulos[j][2]) + ", %s, %s, %s, %s, " + str(direccion[0][1]) + ")"
            mycursor.execute(myInsert, (articulos[j][3], 'Disponible', articulos[j][5], direccion[0][0]))
            mydb.commit()

            myInsert = insertarMySQL["ListaRecibido"] + "(" + str(articulos[j][0]) + ", " + str(ultimaSolicitud) + ")"
            mycursor.execute(myInsert)
            mydb.commit()
        if idProd != 0:
            break

    # Cambia el estado de los articulos en bodega a disponibles
    cursor.callproc("ColocadosEnSucursal", ())
    conexion.commit()


def llenarSucursales(fecha):
    """
    Llena todas las sucursal con un poco de todos los productos
    :param fecha:
    :return:
    """
    for n in range(3):
        numSucursal = n + 1
        mydb, mycursor = getSucursal(numSucursal)

        solicitarMercaderia(fecha, mydb, mycursor)
        totalLista = enviarAlTransporte(numSucursal, fecha, 0, 0)
        recibirEnSucursal(fecha, totalLista, numSucursal, mydb, mycursor, 0)


def pedirProductosBodega(nombreProd, categoria, idSucursal, cantidad, idProd):
    """
    Pide una cantidad de producto especifico a una sucursal especfica.
    :param nombreProd: Nombre del producto que se va a pedir.
    :param categoria: Categoria del producto que se va a pedir.
    :param idSucursal: Id de la sucursal donde se va a hacer el pedido.
    :param cantidad: Cantidad de articulos que se solicitan.
    """
    mydb, mycursor = getSucursal(idSucursal)
    fecha = time.strftime('%Y-%m-%d')

    idProducto = getIdProductoPG(nombreProd, categoria)[0][0] if idProd == 0 else idProd
    solicitarMercaderia(fecha, mydb, mycursor)
    totalLista = enviarAlTransporte(idSucursal, fecha, idProducto, cantidad)
    recibirEnSucursal(fecha, totalLista, idSucursal, mydb, mycursor, idProducto)


def pedirArticulosFaltantes(idSucursal):
    """
    Llena la una sucursal especifica con los articulos que faltan para que tenga minimo 5 de ese producto
    """
    mydb, mycursor = getSucursal(idSucursal)

    mycursor.callproc('CantidadArticulosDisponibles')
    stock = obtenerResultado(mycursor.stored_results())
    idlista = []
    listaReporte = []
    for i in range(len(stock)):
        faltantes = 5 - stock[i][3]
        if faltantes > 0:
            listaReporte += [getIdProductoPG(stock[i][0], stock[i][1])[0][0]]
            pedirProductosBodega(stock[i][0], stock[i][1], idSucursal, faltantes + 5, 0)
        idlista += [stock[i][2]]

    agotados = complementoLista(idlista)
    listaReporte += agotados
    for i in range(len(agotados)):
        pedirProductosBodega("", "", idSucursal, 10, agotados[i])

    articulosFaltantes(listaReporte, idSucursal)


for i in range(1, 4):
    pedirArticulosFaltantes(i)
# fechaapedido = datetime.datetime(2019, 10, 2).strftime('%Y-%m-%d')
# llenarSucursales(fechaapedido)