import sys
import MySQLdb

# Conexión a la base de datos
try:
    db = MySQLdb.connect("localhost","root","","companydata" )
except MySQLdb.Error as e:
    print("No se pudo conectar a la base de datos:",e)
    sys.exit(1)
print("Conexión correcta.")

# Crear un cursor para ejecutar consultas
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS EmployeePerformance")
print("Tabla 'EmployeePerformance' eliminada (si existía).")
cursor.execute("""
    CREATE TABLE EmployeePerformance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee__id INT,
    departament VARCHAR(50),
    performance_score DECIMAL(10, 2),
    year_with_company INT,
    salary DECIMAL(10, 2)
)
""")
print("Tabla 'EmployeePerformance' creada exitosamente.")

# Cerrar la conexión a la base de datos
db.close()
