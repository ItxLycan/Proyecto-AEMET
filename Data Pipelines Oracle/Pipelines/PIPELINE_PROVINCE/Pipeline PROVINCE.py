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

# 4. Ahora sí, importamos el cliente sin errores
from OracleClient import OracleClient

ruta=os.path.dirname(__file__)
ruta_json = os.path.join(ruta, "Provincias.json")
# Preparamos los datos
print("ETL para la inserción de datos en PROVINCE en Oracle")

db = OracleClient()
with open(ruta_json, "r", encoding="utf-8") as archivo:
    datosProvincia = json.load(archivo)

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
ruta_json = os.path.join(ruta, "Provincias.json")
# Preparamos los datos
print("ETL para la inserción de datos en PROVINCE en Oracle")

db = OracleClient()
with open(ruta_json, "r", encoding="utf-8") as archivo:
    datosProvincia = json.load(archivo)

for elemento in datosProvincia:
    insert = "INSERT INTO PROVINCE (ID_COMM,NAM_PROV) VALUES((SELECT DISTINCT ID_COMM FROM AUT_COMM WHERE ID_AEMET_COMM =:1),:2)"\
             .replace(":1", "'" + elemento["aemet__code"] + "'") \
             .replace(":2", "'" + elemento["provincia"] + "'")
    db.execute(insert)

db.close()
