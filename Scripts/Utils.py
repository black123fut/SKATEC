import random
import datetime
import time
import urllib.request, json
from Dictionaries import *
from Connections import *


def getLargoTablaPG(nombre):
    sqlInsertar = "SELECT Id" + nombre + " FROM " + nombre
    cursor.execute(sqlInsertar)
    largo = len(cursor.fetchall())
    return largo


def getIdProductoPG(nombre, categoria):
    sqlInsertar = "SELECT IdProducto FROM Producto WHERE Nombre=%s AND CategoriaActivo=%s"
    cursor.execute(sqlInsertar, (nombre, categoria))
    return cursor.fetchall()


def getIdProductoPGbyId(idProd):
    sqlInsertar = "SELECT * FROM Producto WHERE IdProducto=" + str(idProd)
    cursor.execute(sqlInsertar)
    return cursor.fetchall()


def getSucursalPG(idSucursal):
    sqlInsertar = "SELECT * FROM Sucursal WHERE IdSucursal=" + str(idSucursal)
    cursor.execute(sqlInsertar)
    return cursor.fetchall()


def getLargoTablaMySQL(nombre, mycursor):
    sqlInsertar = "SELECT Id" + nombre + " FROM " + nombre
    mycursor.execute(sqlInsertar)
    largo = len(mycursor.fetchall())
    return largo


def unpackFecha(articulos):
    res = []
    for x in articulos:
        tmp = []
        for y in range(len(x)):
            if y == len(x) - 1:
                tmp += ['%s' % x[y], ]
            else:
                tmp += [x[y]]
        res += [tuple(tmp)]

    return res


def GenerarFecha():
    anio = random.randint(2014, 2019)
    mes = random.randint(1, 12)
    dia = random.randint(1, 30)
    # fecha = anio + "-" + mes + "-" + dia
    fecha = datetime.datetime(anio, mes, dia)
    return fecha.strftime('%Y-%m-%d')


def GenerarFechaGarantia():
    fechaIn = time.strftime('%Y-%m-%d')
    fechaFin = str(int(fechaIn[:4])+1) + fechaIn[4:]
    return fechaIn, fechaFin


def GenerarFechaNac():
    anio = random.randint(1950, 2005)
    mes = random.randint(1, 12)
    dia = random.randint(1, 30)
    fecha = datetime.datetime(anio, mes, dia)
    return fecha.strftime('%Y-%m-%d')


def GetFecha(anio, mes, dia):
    return datetime.datetime(anio, mes, dia).strftime('%Y-%m-%d')


def GenerarPromocion(idSucursal, idProducto):
    mycursor, mydb = getSucursal(idSucursal)
    prodRandom = random.randint(1, 20) if idProducto == 0 else idProducto
    descuento = random.randint(10, 70)
    sucursal = getSucursalPG(idSucursal)[0]
    producto = getIdProductoPGbyId(prodRandom)[0]
    fecha = time.strftime('%Y-%m-%d')
    vencimiento = datetime.datetime(2019, random.randint(10, 12), random.randint(1, 30)).strftime('%Y-%m-%d')

    myInsert = insertarMySQL["Promocion"] + "(" + producto[1] + ", " + sucursal[1] + ", %s, %s, " + str(descuento) \
               + ", " + str(producto[0]) + ")"
    mycursor.execute(myInsert, (fecha, vencimiento))
    mydb.commit()


def GenerarDireccion():
    direccion = str(random.randint(50, 5000)) + "mts "
    num = random.randint(1, 4)
    if num == 1:
        direccion += "norte y "
    elif num == 2:
        direccion += "sur y "
    elif num == 3:
        direccion += "este y "
    else:
        direccion += "oeste y "

    direccion += str(random.randint(50, 500)) + "mts "

    num = random.randint(1, 4)
    if num == 1:
        direccion += "norte de "
    elif num == 2:
        direccion += "sur de "
    elif num == 3:
        direccion += "este de "
    else:
        direccion += "oeste de "

    num = random.randint(1, 4)
    if num == 1:
        direccion += "la escuela"
    elif num == 2:
        direccion += "la iglesia"
    elif num == 3:
        direccion += "la comisaria"
    elif num == 4:
        direccion += "el mercado central"
    elif num == 5:
        direccion += "el parque central"
    else:
        direccion += "el museo"

    return direccion


def obtenerNombre(cedula):
    with urllib.request.urlopen("https://apis.gometa.org/cedulas/" + str(cedula) + "&key=KtivgvSWRiAWCZK") as url:
        data = json.loads(url.read().decode())
        if data['resultcount'] == 0:
            return 1,1
        nombre = data["results"][0]["firstname1"]
        apellidos = data["results"][0]["lastname"]
        return nombre, apellidos


def CalcularPuntos(monto):
    if monto > 50000:
        puntos = int(monto*0.1)
        return puntos
    else:
        puntos = int(monto*0.05)
        return puntos


def GenerarCedula():
    cedula = str(random.randint(1, 7))
    for i in range(8):
        cedula = cedula + str(random.randint(0, 9))
    cedula = int(cedula)
    return cedula

	
def GenerarNombre():
    ind = random.randint(0, 79)
    return nombres[ind]

	
def GenerarApellido():
    ind = random.randint(0,99)
    return apellidos[ind]

	
def GenerarTel():
    telefono = str(random.randint(2, 9))
    for i in range(7):
        telefono = telefono + str(random.randint(0, 9))
    return telefono


def GenerarEmail(nombre):
    num = random.randint(1,5)
    if num == 1:
        return nombre + "@gmail.com"
    elif num == 2:
        return nombre + "@hotmail.com"
    elif num == 3:
        return nombre + "@outlook.com"
    elif num == 4:
        return nombre + "@yahoo.com"
    else:
        return nombre + "@livemail.com"

		
def getUsuarioPG(cedula):
    sentenciaPSQL = "SELECT * FROM Usuario WHERE Cedula = %s"
    cursor.execute(sentenciaPSQL, (str(cedula),))
    usuario = cursor.fetchone()
    return usuario
