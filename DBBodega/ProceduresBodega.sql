CREATE OR REPLACE FUNCTION agregarListaEnvio(IN NumEnvio INT, IN Sucursal INT, IN Cantidad INT, IN Producto INT)
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
    SELECT Di.Descripcion, Ca.idcanton FROM Direccion Di
    INNER JOIN Canton Ca ON Di.idcanton = Ca.idcanton
    INNER JOIN Sucursal Su ON Di.iddireccion = Su.iddireccion
    WHERE Su.IdSucursal = Id;
END;
$$ LANGUAGE plpgsql;