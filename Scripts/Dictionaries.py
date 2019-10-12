codigoArticulo = {
    1: "DR-7-",
    2: "JY-2-",
    3: "FR-8-",
    4: "LP-2-",
    5: "QW-3-",
    6: "SQ-6-",
    7: "QC-8-",
    8: "HT-9-",
    9: "KU-5-",
    10: "PO-2-",
    11: "TH-5-",
    12: "RT-6-",
    13: "JA-1-",
    14: "NB-2-",
    15: "XZ-9-",
    16: "ZX-3-",
    17: "FV-7-",
    18: "LV-4-",
    19: "OW-5-",
    20: "BQ-4-"
}

insertar = {
    "Articulo": "INSERT INTO  Articulo(IdArticulo,CodigoArticulo,Estado,FechaRegistro,IdProducto,IdSucursal) VALUES ",
    "ListaSolicitud": "INSERT INTO  ListaSolicitud(IdProducto,IdSolicitudPedido,Cantidad) VALUES ",
    "ListaRecibido": "INSERT INTO  ListaRecibido(IdArticulo,IdPedidoRecibido) VALUES ",
    "SolicitudPedido": "INSERT INTO  SolicitudPedido(IdSolicitudPedido,IdProveedor,FechaSolicitud) VALUES ",
    "PedidoRecibido": "INSERT INTO  PedidoRecibido(IdPedidoRecibido,IdSolicitudPedido,IdProveedor,FechaRecibido) VALUES ",
    "Envio": "INSERT INTO Envio (FechaEnvio,IdSucursal) VALUES ",
    "ListaEnvio": "INSERT INTO ListaEnvio (IdArticulo,IdEnvio) VALUES ",
    "Factura": "INSERT INTO Factura (IdFactura,IdSucursal,IdCliente,FechaCompra,MontoTotal,FechaVenceGarantia) VALUES ",
    "EmpleadoMes": "INSERT INTO EmpleadoMes(IdEmpleado, FechaEmpleadoMes) VALUES ",
    "Venta": "INSERT INTO Venta(IdFactura,IdArticulo,Precio) VALUES ",
    "Usuario": "INSERT INTO  Usuario(Cedula,Nombre,Apellido,FechaHoraRegistro,Telefono,Email,DetalleDireccion,IdCanton) VALUES ",
    "Cliente": "INSERT INTO Cliente(IdCliente,Cedula) VALUES",
    "Vendedor": "INSERT INTO Vendedor(IdEmpleado,IdSucursal,NumVentas) VALUES "
}

insertarMySQL = {
    "Articulo": "INSERT INTO  Articulo(IdArticulo,IdProducto,IdSucursal,CodigoArticulo,Estado,FechaRegistro,"
                "DetalleDireccion,IdCanton) VALUES ",
    "PedidoRecibido": "INSERT INTO  PedidoRecibido(IdSolicitudPedido,FechaRecibido) VALUES ",
    "SolicitudPedido": "INSERT INTO  SolicitudPedido(FechaSolicitud) VALUES ",
    "ListaRecibido": insertar["ListaRecibido"],
    "ListaSolicitud": insertar["ListaSolicitud"],
    "Promocion": "INSERT INTO Promocion(CodigoProducto,CodigoSucursal,FechaHoraInicio,FechaHoraFin,Descuento,IdProducto) VALUES ",
    "EmpleadoMes": "INSERT INTO EmpleadoMes(IdEmpleado, FechaEmpleadoMes) VALUES ",
    "Factura": "INSERT INTO Factura (IdFactura,IdEmpleado,IdCliente,FechaCompra,PuntosObtenidos,MontoTotal,FechaVenceGarantia) VALUES "
}

nombres = ["Carlos","Kevin","Luis","Isaac","Joseph","Vanesa","Jessica","Elena","Katherine","Capilla","Cañosanto",
               "Camino","Buen suceso","Salud","Vasco","Valvanera","Yedra","Triana","Palma","Blasco","Mayte","Medir",
               "Melodía","Mencía","Mercedario","Munio","Muño","Nela","Nelia","Luscinda","Luzdivina","Mabel","Reyes",
               "Mairena","Lulú","Lobo","Lucinda","Lluvia","Llanos","Liria","Lirios","Lirio","Maite","Maravilla","Marín",
               "Maritere","Marisol","Marisa","Mariola","Mariluz","Marilena","Marilén","Maricruz","Maribel","Marianela",
               "Mariam","Maravillas","Librado","Librada","Libertad","Lesmes","Lágrimas","Gutierre","Florida","Fina",
               "Fraternidad","Fuencisla","Fuensanta","Emeterio","Encina","Escarlata","Espino","Fadrique","Felicidad",
               "Fernán","García","Garcilaso","Indalecia","Gozos","Graciosa","Granada"]

apellidos = ["González","Rodríguez","Gómez","Fernández","López","Díaz","Pérez","García","Sánchez","Romero","Sosa",
                 "Torres","Álvarez","Ruiz","Ramírez","Flores","Benítez","Acosta","Medina","Herrera","Suárez","Aguirre",
                 "Giménez","Gutiérrez","Pereyra","Rojas","Molina","Castro","Ortiz","Silva","Núñez","Luna","Juárez",
                 "Cabrera","Ríos","Morales","Godoy","Moreno","Ferreyra","Domínguez","Carrizo","Peralta","Castillo",
                 "Ledesma","Quiroga","Vega","Vera","Muñoz","Ojeda","Ponce","Villalba","Cardozo","Navarro","Coronel",
                 "Vázquez","Ramos","Vargas","Cáceres","Arias","Figueroa","Córdoba","Correa","Maldonado","Paz","Rivero",
                 "Miranda","Mansilla","Farias","Roldán","Méndez","Guzmán","Aguero","Hernández","Lucero","Cruz","Páez",
                 "Escobar","Mendoza","Barrios","Bustos","Ávila","Ayala","Blanco","Soria","Maidana","Acuña","Leiva","Duarte",
                 "Moyano","Campos","Soto","Martín","Valdez","Bravo","Chávez","Velázquez","Olivera","Toledo","Franco"]