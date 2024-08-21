import sys
import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = MySQLdb.connect(self.host, self.user, self.password, self.database)
            self.cursor = self.connection.cursor()
            print("Conexión correcta.")
        except MySQLdb.Error as e:
            print("No se pudo conectar a la base de datos:", e)
            sys.exit(1)

    def create_table(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS EmployeePerformance")
            print("Tabla 'EmployeePerformance' eliminada (si existía).")
            
            self.cursor.execute("""
                CREATE TABLE EmployeePerformance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee__id INT,
                department VARCHAR(50),
                performance_score DECIMAL(10, 2),
                year_with_company INT,
                salary DECIMAL(10, 2)
            )
            """)
            print("Tabla 'EmployeePerformance' creada exitosamente.")
        except MySQLdb.Error as e:
            print("Error al crear o eliminar la tabla:", e)
            self.connection.close()
            sys.exit(1)

    def insert_data(self, data_tuples):
        try:
            insert_query = """
                INSERT INTO EmployeePerformance (id, employee__id, department, performance_score, year_with_company, salary)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.executemany(insert_query, data_tuples)
            print("Datos insertados exitosamente.")
            self.connection.commit()
        except MySQLdb.Error as e:
            print("Error al insertar los datos:", e)

    def close(self):
        if self.connection:
            self.connection.close()

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataframe = None

    def load_data(self):
        try:
            self.dataframe = pd.read_csv(self.file_path)
            print("Datos cargados en DataFrame.")
        except FileNotFoundError as e:
            print("El archivo CSV no se encontró:", e)
            sys.exit(1)
        except pd.errors.EmptyDataError as e:
            print("El archivo CSV está vacío:", e)
            sys.exit(1)
        except pd.errors.ParserError as e:
            print("Error al leer el archivo CSV:", e)
            sys.exit(1)

class DataAnalyzer:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def analyze(self):
        print('Media, mediana y desviación estándar de rendimiento:')
        print(self.dataframe['performance_score'].mean())
        print(self.dataframe['performance_score'].median())
        print(self.dataframe['performance_score'].std())

        print('Media, mediana y desviación estándar de salario:')
        print(self.dataframe['salary'].mean())
        print(self.dataframe['salary'].median())
        print(self.dataframe['salary'].std())

        print('Número total de empleados por departamento:')
        print(self.dataframe.groupby('department').size())

        print('Correlación entre años en la empresa y rendimiento:')
        print(self.dataframe['year_with_company'].corr(self.dataframe['performance_score']))

        print('Correlación entre salario y rendimiento:')
        print(self.dataframe['salary'].corr(self.dataframe['performance_score']))

class DataVisualizer:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def plot(self):
        # Histograma de rendimiento para el departamento de IT
        df_IT = self.dataframe[self.dataframe['department'] == 'IT']
        plt.hist(df_IT['performance_score'], bins=10, edgecolor='black', alpha=0.7)
        plt.title('Histograma de rendimiento para el departamento de IT')
        plt.xlabel('Rendimiento')
        plt.ylabel('Frecuencia')
        plt.show()

        # Gráfico de dispersión de year_with_company vs. performance_score
        plt.scatter(self.dataframe['year_with_company'], self.dataframe['performance_score'], alpha=0.7)
        plt.title('Años con la empresa vs. Rendimiento')
        plt.xlabel('Años con la empresa')
        plt.ylabel('Rendimiento')
        plt.show()

        # Gráfico de dispersión de salary vs. performance_score
        plt.scatter(self.dataframe['salary'], self.dataframe['performance_score'], alpha=0.7)
        plt.title('Salario vs. Rendimiento')
        plt.xlabel('Salario')
        plt.ylabel('Rendimiento')
        plt.show()

def main():
    db = Database("localhost", "root", "", "companydata")
    db.connect()
    db.create_table()

    loader = DataLoader('MOCK_DATA.csv')
    loader.load_data()

    data_analyzer = DataAnalyzer(loader.dataframe)
    data_analyzer.analyze()

    visualizer = DataVisualizer(loader.dataframe)
    visualizer.plot()

    data_tuples = list(loader.dataframe.itertuples(index=False, name=None))
    db.insert_data(data_tuples)

    db.close()

if __name__ == "__main__":
    main()
