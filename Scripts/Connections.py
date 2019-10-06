import psycopg2
import mysql.connector

#Conexion con PostgreSQL
cadConexon = "host='localhost' dbname='bodega' user='postgres' password='bodega' port=5432"

conexion = psycopg2.connect(cadConexon)
cursor = conexion.cursor()

#Conexion con MySQL

def getSucursal(numDB):
    mydb = mysql.connector.connect(
        host="localhost",
        database="sucursal" + str(numDB),
        user="root",
        passwd="SuContraseñaPrro",
        port=3306
    )

    mycursor = mydb.cursor()
    return mydb, mycursor


