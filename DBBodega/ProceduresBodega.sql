
CREATE OR REPLACE FUNCTION AgregarListaEnvio(IN NumEnvio INT, IN Sucursal INT, IN Cantidad INT, IN Producto INT)
RETURNS INT AS $$
BEGIN
    UPDATE Articulo
    SET Estado = 'EnCamino'
    WHERE CTID IN (
        SELECT CTID FROM Articulo
        WHERE IdSucursal = Sucursal AND Estado = 'embodegado' AND IdProducto = Producto
        LIMIT Cantidad
        );

    INSERT INTO ListaEnvio(IdArticulo, IdEnvio)
    SELECT IdArticulo, NumEnvio FROM Articulo
    WHERE Estado = 'EnCamino' AND IdSucursal = Sucursal;
	RETURN 1;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION ColocadosEnSucursal()
RETURNS INT AS $$
BEGIN
    UPDATE Articulo
    SET Estado = 'Disponible'
    WHERE Estado = 'EnCamino';
    RETURN 1;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ObtenerDireccionSucursal(IN Id INT)
RETURNS TABLE(Descripcion TEXT, IdCanton INTEGER)
AS $$
BEGIN
    RETURN QUERY
    SELECT S.DetalleDireccion, S.IdCanton FROM Sucursal S
    WHERE S.IdSucursal = Id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION AumentarSalario (IN IdMejorEmpleado INT)
RETURNS INT AS $$
BEGIN
    UPDATE Empleado
    SET Salario = Salario + 20000
    WHERE IdEmpleado = IdMejorEmpleado;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION RegistrarCliente(ced INT, fechaIn DATE, fechaExp DATE)
RETURNS TABLE(IdCliente INT) AS $$
BEGIN
    INSERT INTO Cliente(Cedula,Puntos,FechaInicio,FechaExpiracion)
    VALUES (ced, 0, fechaIn, fechaExp);

    RETURN QUERY
    SELECT C.IdCliente FROM Cliente C
    WHERE C.Cedula = ced;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION RegistrarEmpleado(ced INT, codigo VARCHAR(30), fechaIn DATE, puest VARCHAR(30), salar FLOAT)
RETURNS TABLE(IdEmpleado INT) AS $$
BEGIN
    INSERT INTO Empleado(Cedula,CodigoEmpleado,Estado,FechaIngreso,NumVentas,Puesto,Salario)
    VALUES (ced, codigo, 'Activo', fechaIn, 0, puest, salar);

    RETURN QUERY
    SELECT E.IdEmpleado FROM Empleado E
    WHERE E.Cedula = ced;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION ActualizarCliente(IN Id INT, IN PuntosGanados INT)
RETURNS INT AS $$
BEGIN
    UPDATE Cliente
    SET Puntos = Puntos + PuntosGanados
    WHERE IdCliente = Id;

    RETURN 1;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION ActualizarArticulo(IN IdArt INT, IN Est TEXT)
RETURNS INT AS $$
BEGIN
    UPDATE Articulo
    SET Estado = Est
    WHERE IdArticulo = IdArt;
	RETURN 1;
END;
$$ LANGUAGE plpgsql;

