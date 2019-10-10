from Utils import *

#Crea la factura que funciona como el encabezado de la lista de articulos en la compra efectuada
def CrearFactura(idCliente, idEmpleado,idSucursal,fecha,mydb, mycursor):
    sentenciaPSQL = insertar["Factura"] + "(%s,%s,\""+fecha+"\",0,\""+fecha+"\")"
    cursor.execute(sentenciaPSQL,(str(idSucursal),str(idCliente)))
    conexion.commit()

    sentenciaPSQL = "SELECT IdFactura FROM Fractura"
    cursor.execute(sentenciaPSQL)
    idFactura = len(cursor.fetchall())

    sentenciaMSQL = insertarMySQL["Factura"] + "(%s,%s,%s,\""+fecha+"\",0,0,\""+fecha+"\")"
    mycursor.execute(sentenciaMSQL,(str(idFactura),str(idEmpleado),str(idCliente)))
    mydb.commit()

    return idFactura

#Añade el monto total de la compra efectuada, los puntos ganados por el cliente y suma una venta al empleado que la realizo
def ActualizarFactura(idFactura, monto, puntosGanados, idCliente, idEmpleado, mydb, mycursor):
    cursor.callproc("ActualizarFactura", (int(idFactura), float(monto),int(puntosGanados),int(idCliente),int(idEmpleado)))
    conexion.commit()

    mycursor.callproc("ActualizarFactura", (int(idFactura), float(monto),int(puntosGanados),int(idCliente),int(idEmpleado)))
    mydb.commit()

#Añade un articulo a la lista de articulos de la compra que se efectua
def Venta(idArticulo, idFactura, precio, mydb, mycursor):
    # sentenciaPSQL = insertar["Venta"] + "(%s , %s, %s)"
    # cursor.execute(sentenciaPSQL,(str(idFactura),str(idArticulo),str(precio)))
    # conexion.commit()
    cursor.callproc("Venta",(int(idFactura), int(idArticulo), float(precio)))
    conexion.commit()

    mycursor.callproc("Venta", (int(idFactura), int(idArticulo), float(precio)))
    mydb.commit()

#def EfectuarUnaCompra(idCliente,idEmpleado,idSucursal,articulos):
#    mydb, mycursor = getSucursal(idSucursal)

#Genera valores semi-aleatorios para el numero de compras que se quiere registrar
def GenerarCompras(numCompras):
    for i in range(3):
        idSucursal= i+1
        mydb, mycursor = getSucursal(idSucursal)
        for n in range(numCompras):
            sentenciaPSQL = "SELECT IdCliente FROM Cliente"
            cursor.execute(sentenciaPSQL)
            cantidadClientes = len(cursor.fetchall())
            idCliente = random.randint(1,int(cantidadClientes))

            sentenciaMSQL = "SELECT IdEmpleado FROM Empleado WHERE Puesto = \"Vendedor\""
            mycursor.execute(sentenciaMSQL)
            cantidadEmpleados = len(mycursor.fetchall())
            idEmpleado = random.randint(1, int(cantidadEmpleados))

            fecha = GenerarFecha()

            idFactura = CrearFactura(idCliente,idEmpleado,idSucursal,fecha,mydb,mycursor)

            monto = 0.0

            numArticulos = random.randint(1, 4)
            for z in range(numArticulos):
                idProd = random.randint(1, 20)

                sentenciaMSQL = "SELECT Precio FROM Producto WHERE Producto.IdProducto = %s"
                mycursor.execute(sentenciaMSQL, (str(idProd),))
                resultados = mycursor.fetchone()
                precio = resultados[0]

                sentenciaMSQL = "SELECT IdArticulo FROM Articulo WHERE Articulo.IdProducto = %s AND Articulo.Estado = \"Disponible\""
                mycursor.execute(sentenciaMSQL,(str(idProd),))
                resultados = mycursor.fetchall()
                if len(resultados) == 0:
                    print("No disponible")
                else:
                    print("check")
                    idArt = resultados[0][0]
                    Venta(idArt, idFactura, precio)
                    monto += precio
                    
            puntosGanados = CalcularPuntos(monto)

            ActualizarFactura(idFactura, monto, puntosGanados, idCliente, idEmpleado, mydb, mycursor)