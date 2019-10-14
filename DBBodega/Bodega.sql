/*
        Direccion
 */
CREATE TABLE IF NOT EXISTS Pais (
    IdPais SERIAL PRIMARY KEY,
    Nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Provincia (
    IdProvincia SERIAL PRIMARY KEY,
    IdPais INTEGER NOT NULL,
    Nombre TEXT NOT NULL,
    FOREIGN KEY (IdPais) REFERENCES Pais (IdPais)
);

CREATE TABLE IF NOT EXISTS Canton (
    IdCanton SERIAL PRIMARY KEY,
    IdProvincia INTEGER NOT NULL,
    Nombre TEXT NOT NULL,
    FOREIGN KEY (IdProvincia) REFERENCES Provincia (IdProvincia)
);
/*
        Persona - Cliente
 */
CREATE TABLE IF NOT EXISTS Usuario (
    Cedula INTEGER UNIQUE NOT NULL,
    Nombre TEXT NOT NULL,
    Apellido TEXT NOT NULL,
    FechaRegistro DATE NOT NULL,
    Telefono TEXT,
    Email TEXT,
    DetalleDireccion TEXT,
    FechaNacimiento DATE NOT NULL,
    IdCanton INTEGER NOT NULL,
    FOREIGN KEY (IdCanton) REFERENCES Canton(IdCanton)
);


CREATE TABLE IF NOT EXISTS Cliente (
    IdCliente SERIAL PRIMARY KEY,
    Cedula INTEGER NOT NULL,
    Puntos INTEGER NOT NULL,
    FechaInicio DATE NOT NULL,
    FechaExpiracion DATE NOT NULL,
    FOREIGN KEY (Cedula) REFERENCES Usuario(Cedula)
);

/*
        Sucursal
 */
CREATE TABLE IF NOT EXISTS Sucursal (
    IdSucursal SERIAL PRIMARY KEY,
    CodigoSucursal TEXT NOT NULL,
    Nombre TEXT NOT NULL,
    Descripcion TEXT NOT NULL,
    Estado TEXT NOT NULL,
    DetalleDireccion TEXT,
    IdCanton INTEGER NOT NULL,
    FOREIGN KEY (IdCanton) REFERENCES Canton(IdCanton)
);

/*
        Empleados
 */
CREATE TABLE IF NOT EXISTS Empleado (
    IdEmpleado SERIAL PRIMARY KEY,
    Cedula INTEGER NOT NULL,
    CodigoEmpleado TEXT UNIQUE NOT NULL,
    Estado TEXT NOT NULL,
    FechaIngreso DATE NOT NULL,
    NumVentas INTEGER NOT NULL,
    Puesto TEXT NOT NULL,
    Salario FLOAT NOT NULL,
    FOREIGN KEY (Cedula) REFERENCES Usuario(Cedula)
);

CREATE TABLE IF NOT EXISTS Administrador (
    IdAdmin SERIAL PRIMARY KEY,
    IdSucursal INTEGER UNIQUE NOT NULL,
    IdEmpleado INTEGER NOT NULL,
    InicioAdmin DATE NOT NULL,
    FinAdmin DATE NOT NULL,
    FOREIGN KEY (IdEmpleado) REFERENCES Empleado(IdEmpleado),
    FOREIGN KEY (IdSucursal) REFERENCES Sucursal(IdSucursal)
);

CREATE TABLE IF NOT EXISTS EmpleadoBodega (
    IdEmpleado INTEGER NOT NULL,
    FOREIGN KEY (IdEmpleado) REFERENCES Empleado(IdEmpleado)
);

CREATE TABLE IF NOT EXISTS Vendedor (
    IdVendedor SERIAL PRIMARY KEY,
    IdEmpleado INTEGER NOT NULL,
    IdSucursal INTEGER NOT NULL,
    NumVentas INTEGER NOT NULL,
    FOREIGN KEY (IdEmpleado) REFERENCES Empleado(IdEmpleado),
    FOREIGN KEY (IdSucursal) REFERENCES Sucursal(IdSucursal)
);

CREATE TABLE IF NOT EXISTS EmpleadoMes (
    IdEmpleado INTEGER NOT NULL,
    FechaEmpleadoMes DATE NOT NULL,
    FOREIGN KEY (IdEmpleado) REFERENCES Empleado(IdEmpleado)
);

/*
        Envios a sucursal
 */

/*
        Mercaderia
 */
CREATE TABLE IF NOT EXISTS Proveedor (
    IdProveedor SERIAL PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Telefono TEXT NOT NULL,
    CedulaJuridica TEXT NOT NULL,
    DetalleDireccion TEXT,
    IdCanton INTEGER NOT NULL,
    FOREIGN KEY (IdCanton) REFERENCES Canton(IdCanton)
);

CREATE TABLE IF NOT EXISTS Producto (
    IdProducto SERIAL PRIMARY KEY,
    CodigoProducto TEXT NOT NULL,
    Nombre TEXT NOT NULL,
    Descripcion TEXT,
    CategoriaActivo TEXT,
    Precio FLOAT,
    IdProveedor INTEGER NOT NULL,
    FOREIGN KEY (IdProveedor) REFERENCES Proveedor(IdProveedor)
);

CREATE TABLE IF NOT EXISTS SolicitudPedido (
    IdSolicitudPedido SERIAL PRIMARY KEY,
    IdProveedor INTEGER NOT NULL,
    FechaSolicitud DATE NOT NULL,
    FOREIGN KEY (IdProveedor) REFERENCES Proveedor(IdProveedor)
);

CREATE TABLE IF NOT EXISTS PedidoRecibido (
    IdPedidoRecibido SERIAL PRIMARY KEY,
    IdSolicitudPedido INTEGER NOT NULL,
    IdProveedor INTEGER NOT NULL,
    FechaRecibido DATE NOT NULL,
    FOREIGN KEY (IdSolicitudPedido) REFERENCES SolicitudPedido(IdSolicitudPedido),
    FOREIGN KEY (IdProveedor) REFERENCES Proveedor(IdProveedor)
);

CREATE TABLE IF NOT EXISTS Articulo (
    IdArticulo SERIAL PRIMARY KEY,
    IdProducto INTEGER NOT NULL,
    IdSucursal INTEGER NOT NULL,
    CodigoArticulo TEXT UNIQUE NOT NULL,
    Estado TEXT NOT NULL, --Embodegado, EnCamino, Disponible, Vendido
    FechaRegistro DATE NOT NULL,
    FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto),
    FOREIGN KEY (IdSucursal) REFERENCES Sucursal(IdSucursal)
);

CREATE TABLE IF NOT EXISTS ListaSolicitud (
    IdProducto INTEGER NOT NULL,
    IdSolicitudPedido INTEGER NOT NULL,
    Cantidad INTEGER NOT NULL,
    FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto),
    FOREIGN KEY (IdSolicitudPedido) REFERENCES SolicitudPedido(IdSolicitudPedido)
);

CREATE TABLE IF NOT EXISTS ListaRecibido (
    IdArticulo INTEGER NOT NULL,
    IdPedidoRecibido INTEGER NOT NULL,
    FOREIGN KEY (IdArticulo) REFERENCES Articulo(IdArticulo),
    FOREIGN KEY (IdPedidoRecibido) REFERENCES PedidoRecibido(IdPedidoRecibido)
);

CREATE TABLE IF NOT EXISTS Envio (
    IdEnvio SERIAL PRIMARY KEY,
    IdSucursal INTEGER NOT NULL,
    FechaEnvio DATE NOT NULL,
    FOREIGN KEY (IdSucursal) REFERENCES Sucursal(IdSucursal)
);

CREATE TABLE IF NOT EXISTS ListaEnvio (
    IdArticulo INTEGER NOT NULL,
    IdEnvio INTEGER NOT NULL,
    FOREIGN KEY (IdArticulo) REFERENCES Articulo(IdArticulo),
    FOREIGN KEY (IdEnvio) REFERENCES Envio(IdEnvio)
);

/*
        Ventas por sucursal
 */
CREATE TABLE IF NOT EXISTS Factura (
    IdFactura SERIAL PRIMARY KEY,
    IdFacturaSucursal INTEGER NOT NULL,
    IdSucursal INTEGER NOT NULL,
    IdCliente INTEGER NOT NULL,
    IdEmpleado INTEGER NOT NULL,
    FechaCompra TIMESTAMP NOT NULL,
    FechaVenceGarantia DATE,
    MontoTotal FLOAT,
    MetodoPago TEXT NOT NULL,
    FOREIGN KEY (IdSucursal) REFERENCES Sucursal(IdSucursal),
    FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente),
    FOREIGN KEY (IdEmpleado) REFERENCES Empleado(IdEmpleado)
);


CREATE TABLE IF NOT EXISTS Venta (
    IdFactura INTEGER NOT NULL,
    IdArticulo INTEGER NOT NULL,
    Precio FLOAT NOT NULL,
    FOREIGN KEY (IdFactura) REFERENCES Factura(IdFactura),
    FOREIGN KEY (IdArticulo) REFERENCES Articulo(IdArticulo)
);







