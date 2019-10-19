import psycopg2
import mysql.connector


#Conexion con PostgreSQL
cadConexon = "host='localhost' dbname='bodega' user='postgres' password='admin' port=5432"

conexion = psycopg2.connect(cadConexon)
cursor = conexion.cursor()

#Conexion con MySQL

def getSucursal(numDB):
    config = {
        'user': 'root',
        'password': "{administrador}",
        'host': "127.0.0.1",
        'database': "Sucursal" + str(numDB),
        'auth_plugin': 'mysql_native_password'
    }

    mydb = mysql.connector.connect(
        **config
    )

    mycursor = mydb.cursor()
    return mydb, mycursor


getSucursal(1)
