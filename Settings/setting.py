import pyodbc

def test_pyodbc_connection():
    try:
        # Conexión directa con pyodbc
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-0JUDDFN\\SQLEXPRESS;'
            'DATABASE=PRUEBA;'
            'Trusted_Connection=yes;'
        )
        print('Conexión establecida con pyodbc.')
        cursor = connection.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        print("Versión de SQL Server:", row[0])
        connection.close()
    except Exception as e:
        print("Error en la conexión:", e)


def get_sqlalchemy_uri():
    # Retorna el URI de conexión para SQLAlchemy con pyodbc
    db_name = "PRUEBA_C"
    server_name = "DESKTOP-0JUDDFN\\SQLEXPRESS"
    return (
        f"mssql+pyodbc://@{server_name}/{db_name}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )
