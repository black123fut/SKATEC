CREATE DATABASE IF NOT EXISTS Sucursal3;

USE Sucursal3;

CREATE TABLE IF NOT EXISTS Pais(
    IdPais INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    NombrePais TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Provincia(
    IdProvincia INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    IdPais INTEGER NOT NULL,
    Nombre TEXT NOT NULL,
    FOREIGN KEY (IdPais) REFERENCES Pais(IdPais)
);

CREATE TABLE IF NOT EXISTS Canton(
    IdCanton INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Nombre TEXT NOT NULL,
    IdProvincia INTEGER NOT NULL,
    FOREIGN KEY (IdProvincia) REFERENCES Provincia(IdProvincia)
);

CREATE TABLE IF NOT EXISTS Usuario(
	Cedula INTEGER NOT NULL UNIQUE PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Apellido TEXT NOT NULL,
    FechaRegistro DATE NOT NULL,
    Telefono TEXT,
    Email TEXT,
    DetalleDireccion TEXT,
    FechaNacimiento DATE,
    IdCanton INTEGER,
    FOREIGN KEY (IdCanton) REFERENCES Canton(IdCanton)
);

CREATE TABLE IF NOT EXISTS Empleado(
	IdEmpleado INTEGER NOT NULL PRIMARY KEY,
    CodigoEmpleado VARCHAR(120) NOT NULL UNIQUE,
    Estado TEXT NOT NULL,
    IdSucursal INTEGER NOT NULL,
    Puesto TEXT NOT NULL,
    Salario FLOAT,
    NumVentas INTEGER,
    Cedula INTEGER NOT NULL,
    FechaIngreso DATE,
    FOREIGN KEY (Cedula) REFERENCES Usuario(Cedula)
);

CREATE TABLE IF NOT EXISTS EmpleadoMes(
	IdEmpleado INTEGER NOT NULL,
    FechaEmpleadoMes DATE NOT NULL,
    FOREIGN KEY (IdEmpleado) REFERENCES Empleado(IdEmpleado)
);

CREATE TABLE IF NOT EXISTS Cliente(
	IdCliente INTEGER NOT NULL PRIMARY KEY,
    Cedula INTEGER NOT NULL,
    Puntos INTEGER,
    FechaInicio DATE,
    FechaExpiracion DATE,
    FOREIGN KEY (Cedula) REFERENCES Usuario(Cedula)    
);

CREATE TABLE IF NOT EXISTS Producto(
	IdProducto INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    CodigoProducto VARCHAR(120) NOT NULL UNIQUE,
    Nombre TEXT NOT NULL,
    Descripcion TEXT,
    CategoriaActivo TEXT,
    Precio FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS Articulo(
	IdArticulo INTEGER NOT NULL PRIMARY KEY,
    CodigoArticulo VARCHAR(120) NOT NULL UNIQUE,
    Estado TEXT NOT NULL,
    FechaRegistro DATE NOT NULL,
    IdProducto INTEGER NOT NULL,
    DetalleDireccion TEXT,
    IdCanton INTEGER NOT NULL,
    IdSucursal INTEGER NOT NULL,
    FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto),
    FOREIGN KEY (IdCanton) REFERENCES Canton(IdCanton)
);

CREATE TABLE IF NOT EXISTS Promocion(
	IdPromocion INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    CodigoProducto VARCHAR(120) NOT NULL,
    CodigoSucursal VARCHAR(120) NOT NULL,
    FechaHoraInicio DATETIME NOT NULL,
    FechaHoraFin DATETIME NOT NULL,
    Descuento REAL NOT NULL,
    IdProducto INTEGER NOT NULL,
    FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto)
);

CREATE TABLE IF NOT EXISTS Factura(
	IdFactura INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    IdEmpleado INT NOT NULL,
    IdCliente INT NOT NULL,
    FechaCompra DATETIME NOT NULL,
    PuntosObtenidos INTEGER,
    MontoTotal FLOAT,
    FechaVenceGarantia DATE,
    MetodoPago TEXT,
    FOREIGN KEY (IdEmpleado) REFERENCES Empleado(IdEmpleado),
    FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente)
);

CREATE TABLE IF NOT EXISTS Venta(
	IdFactura INTEGER NOT NULL,
    IdArticulo INTEGER NOT NULL,
    Precio FLOAT,
    FOREIGN KEY (IdFactura) REFERENCES Factura(IdFactura),
    FOREIGN KEY (IdArticulo) REFERENCES Articulo(IdArticulo)
);

CREATE TABLE IF NOT EXISTS SolicitudPedido(
	IdSolicitudPedido INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    FechaSolicitud INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ListaSolicitud(
	IdProducto INTEGER NOT NULL,
    IdSolicitudPedido INTEGER NOT NULL,
    FOREIGN KEY(IdProducto) REFERENCES Producto(IdProducto),
    FOREIGN KEY(IdSolicitudPedido) REFERENCES SolicitudPedido(IdSolicitudPedido)
);

CREATE TABLE IF NOT EXISTS PedidoRecibido(
	IdPedidoRecibido INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    IdSolicitudPedido INTEGER NOT NULL,
    FechaRecibido DATE,
    FOREIGN KEY (IdSolicitudPedido) REFERENCES SolicitudPedido(IdSolicitudPedido)
);

CREATE TABLE IF NOT EXISTS ListaRecibido(
	IdArticulo INTEGER NOT NULL,
    IdPedidoRecibido INTEGER NOT NULL,
    FOREIGN KEY(IdArticulo) REFERENCES Articulo(IdArticulo),
    FOREIGN KEY(IdPedidoRecibido) REFERENCES PedidoRecibido(IdPedidoRecibido)
);