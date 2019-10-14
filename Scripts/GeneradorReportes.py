import csv
import os
from Utils import *


def cambiarEstadoArticulos(articulos):
    for i in range(len(articulos)):
        cursor.callproc('ActualizarArticulo', (articulos[i][0], articulos[i][1]))


def ventas(mycursor, fecha, rango, numfacturas):
    mycursor.callproc('ObtenerVentas', (fecha,))
    ventas = obtenerResultado(mycursor.stored_results())

    inicio = rango + 1
    print( "largo :   ",len(ventas))
    for i in range(numfacturas):
        insertPG = insertar["Venta"] + "(" + str(inicio) + ", " + \
                   str(ventas[i][1]) + ", " + str(ventas[i][2]) + ")"
        cursor.execute(insertPG)
        conexion.commit()
        inicio += 1


def agregarPuntosClientes(clientes, fecha, mycursor):
    for i in range(len(clientes)):
        id = clientes[i][0]
        mycursor.callproc('ObtenerPuntosGanados', (id, fecha))
        puntosGanados = obtenerResultado(mycursor.stored_results())[0][0]
        print(id ,"           ", puntosGanados)
        cursor.callproc('ActualizarCliente', (id, int(puntosGanados)))


def agregarFacturasEnBodega(facturas, idSucursal):
    cursor.execute('SELECT IdFactura FROM Factura')
    ids = cursor.fetchall()

    for i in range(len(facturas)):
        insertPG = insertar["Factura"] + "(" + str(facturas[i][2]) + ", " + str(idSucursal) + ", " + str(facturas[i][4])\
                   + ", " + str(facturas[i][3]) + ", %s, " + str(facturas[i][7]) + ", %s, %s)"
        cursor.execute(insertPG, (facturas[i][5], facturas[i][8], facturas[i][9]))
        conexion.commit()

    return len(ids), len(facturas)


def crearCSV(fecha, lista, nombre):
    path = "Reportes/" + fecha + "/"
    if not os.path.exists(path):
        os.mkdir(path)

    with open(path + nombre + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        print(lista)
        writer.writerows(lista)

    csvFile.close()


def obtenerResultado(stored):
    lista = []
    for resultados in stored:
        lista += resultados.fetchall()
    return lista

def obtenerCambios(mycursor, mydb, idSucursal):
    fecha = time.strftime('%Y-%m-%d')

    mycursor.callproc('ComprasRealizadas', (fecha,))
    articulos = obtenerResultado(mycursor.stored_results())

    mycursor.callproc('PuntosClientes', (fecha,))
    clientes = obtenerResultado(mycursor.stored_results())

    mycursor.callproc('CantidadArticulos')
    stock = obtenerResultado(mycursor.stored_results())

    mycursor.callproc('ObtenerFacturas', (fecha,))
    facturas = obtenerResultado(mycursor.stored_results())

    crearCSV(fecha, articulos, "ArticulosVendidos")
    crearCSV(fecha, clientes, "PuntosDeClientes")
    crearCSV(fecha, stock, "Inventario")
    crearCSV(fecha, facturas, "Facturas")

    rango, numfacturas = agregarFacturasEnBodega(facturas, idSucursal)
    #agregarPuntosClientes(clientes, fecha, mycursor)
    ventas(mycursor, fecha, rango, numfacturas)
    cambiarEstadoArticulos(articulos)

def iniciar(idSucursal):
    mydb, mycursor = getSucursal(idSucursal)
    obtenerCambios(mycursor, mydb, idSucursal)

iniciar(1)