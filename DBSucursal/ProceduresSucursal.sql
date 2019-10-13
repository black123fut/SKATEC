DELIMITER //
CREATE PROCEDURE Venta(idFact INT, idArt INT, prec FLOAT)
BEGIN
	INSERT INTO Venta(IdFactura,IdArticulo,Precio) 
    VALUES (idFact,idArt,prec);
    
    UPDATE Articulo
    SET Estado = 'Vendido'
    WHERE Articulo.IdArticulo = idArt;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ObtenerVentas(IN Fecha DATE)
BEGIN
    SELECT * FROM Venta V
    INNER JOIN Factura F ON F.IdFactura = V.IdFactura
    WHERE F.FechaCompra = Fecha;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ActualizarFactura(idFact INT, monto INT, points INT, idClient INT, idEmp INT)
BEGIN
    UPDATE Factura
    SET MontoTotal = monto, PuntosObtenidos = points
    WHERE Factura.IdFactura = idFact;
    
    UPDATE Cliente
    SET Puntos = Puntos + points
    WHERE Cliente.IdCliente = idClient;
    
    UPDATE Empleado
    SET NumVentas = NumVentas + 1
    WHERE Empleado.IdEmpleado = idEmp;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AumentarSalario (IN IdMejorEmpleado INT)
BEGIN
    UPDATE Empleado
    SET Salario = Salario + 20000
    WHERE IdEmpleado = IdMejorEmpleado;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ObtenerEmpleadoMes (IN Dateanterior DATE, IN Dateactual DATE)
BEGIN
    SELECT *, COUNT(E.IdEmpleado) AS Ventas FROM Empleado E
    INNER JOIN Factura F ON F.IdEmpleado = E.IdEmpleado
    WHERE F.FechaCompra BETWEEN Dateanterior AND Dateactual
    GROUP BY E.IdEmpleado
    ORDER BY Ventas DESC
    LIMIT 1;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ComprasRealizadas(IN Fecha DATE)
BEGIN
    SELECT A.IdArticulo, A.Estado FROM Venta V
    INNER JOIN Factura F ON F.IdFactura = V.IdFactura
    INNER JOIN Articulo A ON A.IdArticulo = V.IdArticulo
    WHERE F.FechaCompra = Fecha;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE PuntosClientes(IN Fecha DATE)
BEGIN
    SELECT C.IdCliente, C.Puntos FROM Cliente C
    INNER JOIN Factura F ON F.IdFactura = C.IdCliente
    WHERE F.FechaCompra = Fecha;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ObtenerPuntosGanados(IN IdCli INT, IN Fecha DATE)
BEGIN
    SELECT SUM(C.Puntos) AS PuntosGanados FROM Cliente C
    INNER JOIN Factura F ON F.IdFactura = C.IdCliente
    WHERE F.FechaCompra = Fecha AND F.IdCliente = IdCli;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE CantidadArticulos()
BEGIN
    SELECT P.Nombre AS NombreProducto, P.IdProducto AS IdProducto, COUNT(A.IdProducto) AS Cantidad FROM Articulo A
    INNER JOIN Producto P ON P.IdProducto = A.IdProducto
    GROUP BY A.IdProducto;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ObtenerFacturas(IN Fecha DATE)
BEGIN
    SELECT CU.Cedula AS Cedula, CU.Nombre AS Nombre, F.* FROM Factura F
    INNER JOIN (
        SELECT C.IdCliente AS IdCliente, U.Cedula AS Cedula, U.Nombre AS Nombre FROM Cliente C
        INNER JOIN Usuario U ON U.Cedula = C.Cedula
        ) CU ON CU.IdCliente = F.IdCliente
    WHERE F.FechaCompra = Fecha;
END //
DELIMITER ;