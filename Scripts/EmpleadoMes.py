from Utils import *


def aumentarSalario(idEmpleado, mycursor):
    mycursor.callproc('AumentarSalario', (idEmpleado, ))


def agregarEmpleadoATablaMes(empleado, fechaactual, mydb, mycursor):
    idEmpleado = str(empleado[0])

    myInsert = insertarMySQL["EmpleadoMes"] + "(" + idEmpleado + ", %s)"
    mycursor.execute(myInsert, (fechaactual, ))
    mydb.commit()

    sqlInsert = insertar["EmpleadoMes"] + "(" + idEmpleado + ", %s)"
    cursor.execute(sqlInsert, (fechaactual, ))
    conexion.commit()

    aumentarSalario(empleado[0], mycursor)


def getEmpleadoMes(mes, anio, mycursor):
    mespasado = mes - 1
    aniopasado = anio
    if mes == 1:
        mespasado = 12
        aniopasado = anio - 1

    fechaactual = GetFecha(anio, mes, 1)
    fechapasada = GetFecha(aniopasado, mespasado, 1)

    mycursor.callproc('ObtenerEmpleadoMes', (fechapasada, fechaactual))
    empleado = []
    for emp in mycursor.stored_results():
        empleado += emp.fetchall()

    return empleado[0], fechaactual


def seleccionarEmpleadoMes(idsucursal, mes, anio):
    mydb, mycursor = getSucursal(idsucursal)

    empleado, fechaactual = getEmpleadoMes(mes, anio, mycursor)
    agregarEmpleadoATablaMes(empleado, fechaactual, mydb, mycursor)


# for i in range(1, 4):
#     seleccionarEmpleadoMes(i, 11, 2019)
