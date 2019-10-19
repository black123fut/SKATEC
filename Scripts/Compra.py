from Utils import *


def metodoPago():
    num = random.randint(1, 2)
    if num == 1:
        return "Efectivo"
    else:
        return "Tarjeta"


# Crea la factura que funciona como el encabezado de la lista de articulos en la compra efectuada
def CrearFactura(idCliente, idEmpleado, fecha, fechaVence, metoPago, mydb, mycursor):
    sentenciaMSQL = insertarMySQL["Factura"] + "(%s,%s,%s,0,0,%s,%s)"
    mycursor.execute(sentenciaMSQL, (str(idEmpleado), str(idCliente), str(fecha), str(fechaVence), str(metoPago)))
    mydb.commit()

    sentenciaMSQL = "SELECT IdFactura FROM Factura"
    mycursor.execute(sentenciaMSQL)
    idFactura = len(mycursor.fetchall())
    return idFactura


# Añade el monto total de la compra efectuada, los puntos ganados por el cliente y suma una venta al empleado que la realizo
def ActualizarFactura(idFactura, monto, puntosGanados, idCliente, idEmpleado, mydb, mycursor):
    mycursor.callproc("ActualizarFactura", (int(idFactura), float(monto), int(puntosGanados), int(idCliente),
                                            int(idEmpleado)))
    mydb.commit()


# Añade un articulo a la lista de articulos de la compra que se efectua
def Venta(idArticulo, idFactura, precio, mydb, mycursor):
    mycursor.callproc("Venta", (int(idFactura), int(idArticulo), float(precio)))
    mydb.commit()


# Genera una compra con los datos que se desean
def EfectuarUnaCompra(idCliente, idEmpleado, idSucursal, cantidad, idProducto):
    mydb, mycursor = getSucursal(idSucursal)
    fechaIn, fechaFin = GenerarFechaGarantia()
    metodoPag = metodoPago()
    idFactura = CrearFactura(idCliente, idEmpleado, fechaIn, fechaFin, metodoPag, mydb, mycursor)
    monto = 0.0

    for idArt in range(cantidad):
        sentenciaMSQL = "SELECT IdProducto FROM Articulo WHERE IdProducto = %s AND Estado = %s"
        mycursor.execute(sentenciaMSQL, (str(idProducto), 'Disponible'))
        resultados = mycursor.fetchall()

        idProd = int(resultados[0][0])

        sentenciaMSQL = "SELECT Precio FROM Producto WHERE Producto.IdProducto = %s"
        mycursor.execute(sentenciaMSQL, (str(idProd),))
        resultados = mycursor.fetchone()
        precio = resultados[0]

        Venta(idArt, idFactura, precio, mydb, mycursor)
        monto += precio

    puntosGanados = CalcularPuntos(monto)
    ActualizarFactura(idFactura, monto, puntosGanados, idCliente, idEmpleado, mydb, mycursor)


# Genera valores semi-aleatorios para el numero de compras que se quiere registrar
def GenerarCompras(numCompras):
    for i in range(3):
        idSucursal = i + 1
        mydb, mycursor = getSucursal(idSucursal)
        for n in range(numCompras):
            sentenciaMSQL = "SELECT IdCliente FROM Cliente"
            mycursor.execute(sentenciaMSQL)
            cantidadClientes = len(mycursor.fetchall())
            idCliente = random.randint(1, cantidadClientes)

            sentenciaMSQL = "SELECT IdEmpleado FROM Empleado WHERE Puesto = \"Vendedor\""
            mycursor.execute(sentenciaMSQL)
            cantidadEmpleados = mycursor.fetchall()
            posicion = random.randint(0, len(cantidadEmpleados) - 1)
            idEmpleado = int(cantidadEmpleados[posicion][0])
            fechaIn, fechaFin = GenerarFechaGarantia()
            metodoPag = metodoPago()
            idFactura = CrearFactura(idCliente, idEmpleado, fechaIn, fechaFin, metodoPag, mydb, mycursor)
            monto = 0.0
            numArticulos = random.randint(1, 4)

            for z in range(numArticulos):
                idProd = random.randint(1, 20)
                sentenciaMSQL = "SELECT Precio FROM Producto WHERE Producto.IdProducto = %s"
                mycursor.execute(sentenciaMSQL, (str(idProd),))
                resultados = mycursor.fetchone()
                precio = resultados[0]
                sentenciaMSQL = "SELECT IdArticulo FROM Articulo WHERE Articulo.IdProducto = %s AND Articulo.Estado = \"Disponible\""
                mycursor.execute(sentenciaMSQL, (str(idProd),))
                resultados = mycursor.fetchall()
                if len(resultados) == 0:
                    print("No disponible")
                else:
                    print("check")
                    idArt = resultados[0][0]
                    Venta(idArt, idFactura, precio, mydb, mycursor)
                    monto += precio

            puntosGanados = CalcularPuntos(monto)
            ActualizarFactura(idFactura, monto, puntosGanados, idCliente, idEmpleado, mydb, mycursor)


# EfectuarUnaCompra(6, 6, 1, 10, 4)
GenerarCompras(50)
