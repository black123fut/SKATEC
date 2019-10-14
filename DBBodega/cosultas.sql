
SELECT * FROM factura;

UPDATE articulo
SET estado = 'embodegado';

DELETE FROM ListaEnvio;
DELETE FROM envio;
ALTER SEQUENCE envio_idenvio_seq RESTART WITH 1;

SELECT * FROM factura;
DELETE FROM cliente; 
DELETE FROM empleado;
DELETE FROM usuario;
DELETE FROM Vendedor;
DELETE FROM venta;
DELETE FROM factura;

ALTER SEQUENCE empleado_idempleado_seq RESTART 1;
ALTER SEQUENCE cliente_idcliente_seq RESTART 1;
ALTER SEQUENCE vendedor_idvendedor_seq RESTART 1;
ALTER SEQUENCE factura_idfactura_seq RESTART 1;