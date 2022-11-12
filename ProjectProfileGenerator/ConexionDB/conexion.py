import pyodbc

def obtener_conexion():
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-IR83M0G;'
                      'Database=DB_RECOG;'
                      'UID=sa;'
                      'PWD=123456')

    return conn
