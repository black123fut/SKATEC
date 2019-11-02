from GeneradorReportes import *
from AbastecerSucursal import *
from EmpleadoMes import *
from LlenarBodega import llenarArticulosAgotados

# Genera los reportes de cada sucursal
for i in range(1, 4):
    hacerReportes(i)

# Llena los articulos de cada sucursal si hay menos de 5
for i in range(1, 4):
    pedirArticulosFaltantes(i)

# Selecciona el empleado del mes
dia = time.strftime('%d')
if dia == '01':
    mes = time.strftime('%m')
    anio = time.strftime('%Y')
    for i in range(1, 4):
        seleccionarEmpleadoMes(i, int(mes), int(anio))

# Llena los articulos agotados o por agotar de la bodega
llenarArticulosAgotados()
