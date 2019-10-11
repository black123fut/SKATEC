DELIMITER //
CREATE PROCEDURE Venta(idFact INT, idArt INT, prec FLOAT)
BEGIN
	INSERT INTO Venta(IdFactura,IdArticulo,Precio) 
    VALUES (idFact,idArt,prec);
    
    UPDATE Articulo
    SET Estado = 'Vendido-Garantia-Activa'
    WHERE Articulo.IdArticulo = idArt;
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