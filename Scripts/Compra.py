from Utils import *


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

def ActualizarFactura(idFactura, monto, puntosGanados, idCliente, idEmpleado, mydb, mycursor):
    mycursor.callproc("ActualizarFactura", (int(idFactura), float(monto),int(puntosGanados),int(idCliente),int(idEmpleado)))
    mydb.commit()
    # Falta crear el store procedure ActualizarFactura en PostgreSQL


def Venta(idArticulo, idFactura, precio, mydb, mycursor):
    # sentenciaPSQL = insertar["Venta"] + "(%s , %s, %s)"
    # cursor.execute(sentenciaPSQL,(str(idFactura),str(idArticulo),str(precio)))
    # conexion.commit()
    mycursor.callproc("Venta", (int(idFactura), int(idArticulo), float(precio)))
    mydb.commit()
    # Falta crear el store procedure Venta en PostgreSQL


def GenerarCompras(numCompras):
    for i in range(3):
        idSucursal= i+1
        mydb, mycursor = getSucursal(idSucursal)
        for n in range(numCompras):
            sentenciaPSQL = "SELECT IdCliente FROM Cliente"
            cursor.execute(sentenciaPSQL)
            cantidadClientes = len(cursor.fetchall())
            idCliente = random.randint(1,int(cantidadClientes))

            sentenciaPSQL = "SELECT IdEmpleado FROM Empleado"
            cursor.execute(sentenciaPSQL)
            cantidadEmpleados = len(cursor.fetchall())
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