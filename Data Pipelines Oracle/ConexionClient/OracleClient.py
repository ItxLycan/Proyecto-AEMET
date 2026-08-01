import oracledb
import sys

class OracleClient:
    def __init__(self, user, password, dsn):
        """Inicializa los parámetros de configuración de la base de datos."""
        self.user = user
        self.password = password
        self.dsn = dsn
        self.conexion = None

    def connect(self):
        """Establece la conexión física con el servidor Oracle."""
        try:
            if not self.conexion:
                print("Intentando conectar a la base de datos Oracle...")
                self.conexion = oracledb.connect(
                    user=self.user,
                    password=self.password,
                    dsn=self.dsn
                )
                print(f"¡Conexión establecida con éxito! (Versión: {self.conexion.version})")
            return self.conexion
        except oracledb.Error as e:
            print(f"❌ Error al conectar a Oracle: {e}")
            sys.exit(1)

    def select(self, query, parametros=None):
        """Ejecuta una consulta de lectura (SELECT) y devuelve los resultados."""
        self.connect()
        try:
            with self.conexion.cursor() as cursor:
                if parametros:
                    cursor.execute(query, parametros)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except oracledb.Error as e:
            print(f"❌ Error al ejecutar consulta SQL: {e}")
            return None

    def execute(self, query, parametros=None):
        """Ejecuta una acción de escritura (INSERT, UPDATE, DELETE, CREATE)."""
        self.connect()
        try:
            with self.conexion.cursor() as cursor:
                if parametros:
                    cursor.execute(query, parametros)
                else:
                    cursor.execute(query)
                # Aplicamos commit para guardar los cambios de forma permanente
                self.conexion.commit()
                print("Operación completada y guardada (COMMIT) con éxito.")
                return True
        except oracledb.Error as e:
            print(f"❌ Error en la operación SQL: {e}")
            
            self.conexion.rollback()  # Deshace cambios si hubo un fallo
            return False

    def close(self):
        """Cierra la conexión de forma segura si está abierta."""
        if self.conexion:
            self.conexion.close()
            self.conexion = None
            print("Conexión con Oracle cerrada correctamente.")
