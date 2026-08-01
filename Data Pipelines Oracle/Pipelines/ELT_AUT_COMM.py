from xmlrpc.client import DateTime
import sys
import os

#  Calculamos la ruta de la carpeta "Data Pipelines Oracle" (un nivel arriba de Pipelines)
ruta_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Construimos la ruta exacta hacia la carpeta donde están tus clientes
ruta_conexion = os.path.join(ruta_padre, "ConexionClient")

# Le decimos a Python que busque módulos dentro de "ConexionClient"
if ruta_conexion not in sys.path:
    sys.path.append(ruta_conexion)

# Ahora la importación funcionará de forma limpia y directa
from OracleClient import OracleClient

# Configurar e instanciar del cliente de Oracle
db = OracleClient(
    user="aemet",
    password="12345",
    dsn="localhost:1521/XE"
)
# Preparamos los datos
print("ELT basica para la inserción de datos en AUT_COMM en Oracle")

listaCodCommAemet = ["'and'","'ara'","'ast'","'bal'","'can'","'coo'","'cle'","'clm'","'cat'","'val'","'ext'","'gal'","'mad'","'mur'","'nav'","'pva'","'rio'"]
listaNamComm = ["'Andalucía'","'Aragón'","'Principado de 'Asturias'","'Illes Balears'","'Cantabria'","'Canarias'","'Castilla y León'","'Castilla - La Mancha'","'Cataluña'","'Comunitat Valenciana'","'Extremadura'","'Galicia'","'Comunidad de Madrid'","'Región de Murcia'","'Comunidad Foral de Navarra'","'País Vasco'","'La Rioja'"]
x=0

for i in range(len(listaCodCommAemet)):
    #Preparamos el INSERT
    insertAutComm = "INSERT INTO AUT_COMM (ID_AEMET_COMM,NAM_COMM,DATE_OPRTN_INSERT) VALUES(:1,:2,SYSDATE)"

    idAemet = listaCodCommAemet[x]
    namComm = listaNamComm[x]

    #Reemplazamos para realizar el insert con los datos
    insertAutComm=insertAutComm.replace(":1",idAemet)
    insertAutComm=insertAutComm.replace(":2",namComm)

    db.execute(insertAutComm)
    x += 1

# 5. Al finalizar la ejecución del pipeline, cerramos la conexión
db.close()