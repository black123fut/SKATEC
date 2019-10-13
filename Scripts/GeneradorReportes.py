import csv
import os
from Utils import *


def cambiarEstadoArticulos(articulos):
    for i in range(len(articulos)):
        cursor.callproc('ActualizarArticulo', (articulos[i][0], articulos[i][1]))


def ventas(mycursor, fecha, rango):
    mycursor.callproc('ObtenerVentas', (fecha,))
    ventas = mycursor.fetchall()

    inicio = rango + 1
    for i in range(len(ventas)):
        insertPG = insertar["Venta"] + "(" + str(inicio) + ", " + \
                   str(ventas[i][1]) + ", " + str(ventas[i][2]) + ")"
        cursor.execute(insertPG)
        conexion.commit()
        inicio += 1


def agregarPuntosClientes(clientes, fecha, mycursor):
    for i in range(len(clientes)):
        id = clientes[i][0]
        mycursor.callproc('ObtenerPuntosGanados', (id, fecha))
        puntosGanados = mycursor.fetchall()

        cursor.callproc('ActualizarCliente', (id, puntosGanados))


def agregarFacturasEnBodega(facturas, idSucursal):
    cursor.execute('SELECT IdFactura FROM Factura')
    ids = cursor.fetchall()

    for i in range(len(facturas)):
        insertPG = insertar["Factura"] + "(" + str(facturas[i][2]) + ", " + str(idSucursal) + ", " + str(facturas[i][4])\
                   + ", " + str(facturas[i][3]) + ", %s, " + str(facturas[i][7]) + ", %s, %s)"
        cursor.execute(insertPG, (facturas[i][5], facturas[i][8], facturas[i][9]))
        conexion.commit()

    return len(ids)



def crearCSV(fecha, lista, nombre, columnnames):
    path = "Reportes/" + fecha + "/"
    os.mkdir(path)
    with open(path + nombre + '.csv', 'wb') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(columnnames)
        writer.writerows(lista)
    csvFile.close()


def obtenerCambios(mycursor, mydb, idSucursal):
    fecha = time.strftime('%Y-%m-%d')

    mycursor.callproc('ComprasRealizadas', (fecha,))
    colnames_articulos = [desc[0] for desc in mycursor.description]
    articulos = mycursor.fetchall()

    mycursor.callproc('PuntosClientes', (fecha,))
    colnames_clientes = [desc[0] for desc in mycursor.description]
    clientes = mycursor.fetchall()

    mycursor.callproc('CantidadArticulos')
    colnames_stock = [desc[0] for desc in mycursor.description]
    stock = mycursor.fetchall()

    mycursor.callproc('ObtenerFacturas', (fecha,))
    colnames_facturas = [desc[0] for desc in mycursor.description]
    facturas = mycursor.fetchall()

    crearCSV(fecha, articulos, "ArticulosVendidos", colnames_articulos)
    crearCSV(fecha, clientes, "PuntosDeClientes", colnames_clientes)
    crearCSV(fecha, stock, "Inventario", colnames_stock)
    crearCSV(fecha, facturas, "Facturas", colnames_facturas)

    agregarFacturasEnBodega(facturas, idSucursal)