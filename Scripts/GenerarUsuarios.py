from Utils import *

def GenerarUsuario(cedula):
    print("ne")
    nombre, apellidos = obtenerNombre(cedula)
    print("nee")
    if nombre != 1:
        nombreCompleto = nombre + apellidos
        fecha = GenerarFecha()
        fechaNac = GenerarFechaNac()
        telefono = GenerarTel()
        email = GenerarEmail(nombreCompleto)
        direccion = GenerarDireccion()
        canton = random.randint(1, 82)

        sentenciaPSQL = insertar["Usuario"] + "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sentenciaPSQL, (str(cedula),str(nombre),str(apellidos),str(fecha),str(telefono),str(email),str(direccion),str(fechaNac), str(canton)))
            conexion.commit()
            return fecha
        except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction):
            return 1
    return 2


def GenerarClientes(cantidad,cedulaIn):
    cedula = cedulaIn
    for i in range(cantidad):
        print(cedula)
        fecha = GenerarUsuario(cedula)
        if fecha == 1:
            print("Usuario ya registrado")
        elif fecha == 2:
            print("Cedula invalida")
        else:
            cursor.callproc("RegistrarCliente", (str(cedula),str(fecha),str(fecha)))
            conexion.commit()
            print("Okkkkk")
            resultado = cursor.fetchone()

            idCliente = resultado[0]

            usuario = getUsuarioPG(cedula)

            for n in range(3):
                mydb, mycursor = getSucursal(n + 1)
                sentenciaMSQL = insertar["Usuario"] + "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(sentenciaMSQL, usuario)
                mydb.commit()

                sentenciaMSQL = insertar["Cliente"] + "(%s,%s,0,%s,%s)"
                mycursor.execute(sentenciaMSQL,(str(idCliente),str(cedula),str(fecha),str(fecha)))
                mydb.commit()
        cedula += 1



def GenerarVendedores(cantidad,idSucursal,cedulaIn):
    cedula = cedulaIn
    for i in range(cantidad):
        fecha = GenerarUsuario(cedula)
        if fecha == 1:
            print("Usuario ya registrado")
        elif fecha == 2:
            print("Cedula invalida")
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
            sentenciaMSQL = insertar["Usuario"] + "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sentenciaMSQL, usuario)
            mydb.commit()

            sentenciaMSQL = insertar["Empleado"] + "(%s,%s,\"Activo\",%s,\"Vendedor\",%s,0,%s,%s)"
            mycursor.execute(sentenciaMSQL, (str(idEmpleado),str(codigo),str(idSucursal),str(280000.0),str(cedula),str(fecha)))
            mydb.commit()
        cedula += 1


def GenerarCodigoEmpleado(idSuc):
    codigo = "SE-"+str(idSuc)+"-"
    for n in range(3):
        for i in range(4):
            codigo = codigo + str(random.randint(0, 9))
        codigo = codigo + "-"
    codigo = codigo + str(random.randint(0, 9))
    return codigo


def CrearCliente(cedula, nombre, apellidos, fecha, fechaNac, telefono, email, direccion, canton):
    sentenciaPSQL = insertar["Usuario"] + "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sentenciaPSQL, (
        str(cedula), str(nombre), str(apellidos), str(fecha), str(telefono), str(email), str(direccion), str(fechaNac),
        str(canton)))
        conexion.commit()

        print("Usuario creado con exito")

        cursor.callproc("RegistrarCliente", (str(cedula), str(fecha), str(fecha)))
        conexion.commit()
        resultado = cursor.fetchone()

        idCliente = resultado[0]

        for n in range(3):
            mydb, mycursor = getSucursal(n + 1)
            sentenciaMSQL = insertar["Usuario"] + "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sentenciaMSQL, (
            str(cedula), str(nombre), str(apellidos), str(fecha), str(telefono), str(email), str(direccion),
            str(fechaNac), str(canton)))
            mydb.commit()

            sentenciaMSQL = insertar["Cliente"] + "(%s,%s,0,%s,%s)"
            mycursor.execute(sentenciaMSQL, (str(idCliente), str(cedula), str(fecha),str(fecha)))
            mydb.commit()

    except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction):
        return 1


n = GenerarVendedores(3,1,305070075)
print(n)


#def CrearEmpleado():
"""

def GenerarUsuario(cedula):
    nombre, apellidos = obtenerNombre(cedula)
    if nombre != 1:
        nombreCompleto = nombre + apellidos
        fecha = GenerarFecha()
        fechaNac = GenerarFechaNac()
        telefono = GenerarTel()
        email = GenerarEmail(nombreCompleto)
        direccion = GenerarDireccion()
        canton = random.randint(1, 82)

        sentenciaPSQL = insertar["Usuario"] + "(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sentenciaPSQL, (str(cedula),str(nombre),str(apellidos),str(fecha),str(telefono),str(email),str(direccion),str(fechaNac), str(canton)))
            conexion.commit()
            return fecha
        except psycopg2.errors.UniqueViolation:
            return 1
    return 2



fecha = GenerarUsuario(305070087)
print(fecha)
"""