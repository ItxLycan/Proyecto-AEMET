import sys
import os
import json

# 1. Subimos dos niveles de forma limpia en el árbol de carpetas
ruta_script = os.path.dirname(__file__)                  # Pipeline PROVINCE
ruta_pipelines = os.path.dirname(ruta_script)            # Pipelines
ruta_raiz_oracle = os.path.dirname(ruta_pipelines)       # Data Pipelines Oracle

# 2. Construimos la ruta hacia los clientes de conexión
ruta_conexion = os.path.join(ruta_raiz_oracle, "ConexionClient")

# 3. Añadimos la ruta al path de Python si no está ya
if ruta_conexion not in sys.path:
    sys.path.append(ruta_conexion)

# 4. Importamos el cliente
from OracleClient import OracleClient

ruta=os.path.dirname(__file__)
ruta_json = os.path.join(ruta, "Comunidad autonoma.json")

db = OracleClient()
with open(ruta_json, "r", encoding="utf-8") as archivo:
    datosProvincia = json.load(archivo)
# Preparamos los datos
print("ETL basica para la inserción de datos en AUT_COMM en Oracle")

for elemento in datosProvincia:
    # Encadenamos los reemplazos sobre la plantilla base
    insert = "INSERT INTO AUT_COMM (ID_AEMET_COMM,NAM_COMM) VALUES(:1,:2) " \
             .replace(":1", "'" + elemento["id_aemet_comm"] + "'") \
             .replace(":2", "'" + elemento["nam_comm"] + "'")
    db.execute(insert)
db.close()