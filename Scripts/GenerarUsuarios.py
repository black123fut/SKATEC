from Utils import *

def GenerarUsuario():
    cedula = GenerarCedula()
    nombre = GenerarNombre()
    apellido = GenerarApellido()
    nombreCompleto = nombre + apellido
    fechaHoraReg, fecha = GenerarFechaHora()
    telefono = GenerarTel()
    email = GenerarEmail(nombreCompleto)
    direccion = GenerarDireccion()
    canton = random.randint(1, 82)

    sentenciaPSQL = insertar["Usuario"] + "(%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sentenciaPSQL, (str(cedula),str(nombre),str(apellido),str(fecha),str(telefono),str(email),str(direccion), str(canton)))
        conexion.commit()
        return cedula, fecha
    except EnvironmentError:
        return 1, 1


def GenerarClientes(cantidad):
    for i in range(cantidad):
        cedula, fecha = GenerarUsuario()

        if int(cedula) == 1:
            print("Usuario ya registrado")
        else:
            cursor.callproc("RegistrarCliente", (str(cedula),str(fecha),"NULL"))
            conexion.commit()
            resultado = cursor.fetchone()

            idCliente = resultado[0]

            usuario = getUsuarioPG(cedula)

            for n in range(3):
                mydb, mycursor = getSucursal(n + 1)
                sentenciaMSQL = insertar["Usuario"] + "(%s,%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(sentenciaMSQL, usuario)
                mydb.commit()

                sentenciaMSQL = insertar["Cliente"] + "(%s,%s,0,%s,NULL)"
                mycursor.execute(sentenciaMSQL,(str(idCliente),str(cedula),str(fecha)))
                mydb.commit()



def GenerarVendedores(cantidad,idSucursal):
    for i in range(cantidad):
        cedula, fecha = GenerarUsuario()
        if int(cedula) ==1:
            print("Usuario ya registrado")
        else:
            codigo = GenerarCodigoEmpleado(idSucursal)

            cursor.callproc("RegistrarEmpleado", (str(cedula), str(codigo), str(fecha),"Vendedor",str(280000.0)))
            conexion.commit()
            resultado = cursor.fetchone()

            idEmpleado = resultado[0]

            sentenciaPSQL = insertar["Vendedor"] + "(%s,%s,0)"
            cursor.execute(sentenciaPSQL,(str(idEmpleado),str(idSucursal)))

            usuario = getUsuarioPG(cedula)

            mydb, mycursor = getSucursal(idSucursal)
            sentenciaMSQL = insertar["Usuario"] + "(%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sentenciaMSQL, usuario)
            mydb.commit()

            sentenciaMSQL = insertarMySQL["Empleado"] + "(%s,%s,\"Activo\",%s,\"Vendedor\",%s,0,%s)"
            mycursor.execute(sentenciaMSQL, (str(idEmpleado),str(codigo),str(idSucursal),str(280000.0),str(cedula)))
            mydb.commit()


def GenerarCodigoEmpleado(idSuc):
    codigo = "SE-"+idSuc+"-"
    for n in range(3):
        for i in range(4):
            codigo = codigo + str(random.randint(0, 9))
        codigo = codigo + "-"
    codigo = codigo + str(random.randint(0, 9))
    return codigo


#def CrearCliente():


#def CrearEmpleado():