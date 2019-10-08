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
    "PedidoRecibido": "INSERT INTO  PedidoRecibido(IdPedidoRecibido,IdSolicitudPedido,IdProveedor,FechaRecibido) VALUES"
                      " ",
    "Envio": "INSERT INTO Envio (FechaEnvio,IdSucursal) VALUES ",
    "ListaEnvio": "INSERT INTO ListaEnvio (IdArticulo,IdEnvio) VALUES "
}

insertarMySQL = {
    "Articulo": "INSERT INTO  Articulo(IdArticulo,IdProducto,IdSucursal,CodigoArticulo,Estado,FechaRegistro,"
                "DetalleDireccion,IdCanton) VALUES ",
    "PedidoRecibido": "INSERT INTO  PedidoRecibido(IdSolicitudPedido,FechaRecibido) VALUES ",
    "SolicitudPedido": "INSERT INTO  SolicitudPedido(FechaSolicitud) VALUES ",
    "ListaRecibido": insertar["ListaRecibido"],
    "ListaSolicitud": insertar["ListaSolicitud"],
    "Promocion": "INSERT INTO Promocion(CodigoProducto,CodigoSucursal,FechaHoraInicio,FechaHoraFin,Descuento,IdProducto) VALUES "
}