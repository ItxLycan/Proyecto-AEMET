import requests
import json
class AemetClient:
    def __init__(self):
        """Inicializa el cliente con la API Key global."""
        self.api_key = "***REMOVED***"
        self.headers = {
            'cache-control': 'no-cache',
            'api_key': self.api_key
        }
        
    def _realizar_peticion(self, url_endpoint):
        """Método interno privado para gestionar la doble petición de AEMET."""
        try:
            # Petición 1: Obtener la URL temporal
            response = requests.get(url_endpoint, headers=self.headers)
            response.raise_for_status()
            meta_datos = response.json()
            
            if meta_datos.get("estado") == 200:
                url_datos = meta_datos.get("datos")
                
                # Petición 2: Descargar los datos reales
                datos_response = requests.get(url_datos)
                datos_response.raise_for_status()
                
                # Intentar devolver como JSON; si falla, devolver como Texto plano
                try:
                    return datos_response.json()
                except json.JSONDecodeError:
                    datos_response.encoding = 'utf-8'
                    return datos_response.text
            else:
                print(f"Error API AEMET: {meta_datos.get('descripcion')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión HTTP: {e}")
            return None

    def obtener_prediccion_municipio(self, codigo_municipio):
        """Obtiene la predicción diaria para un municipio específico."""
        url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo_municipio}"
        return self._realizar_peticion(url)

    def obtener_prediccion_ccaa(self, codigo_ccaa, momento="hoy"):
        """Obtiene la predicción de una CCAA ('hoy', 'manana' o 'pasadomanana')."""
        url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{momento}/{codigo_ccaa}"
        return self._realizar_peticion(url)

    def obtener_maestro_municipios(self):
        """Devuelve el listado completo de todos los municipios de España y sus IDs."""
        url = f"https://opendata.aemet.es"
        return self._realizar_peticion(url)
