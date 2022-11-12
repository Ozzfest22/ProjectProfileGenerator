from ProjectProfileGenerator.ConexionDB.conexion import obtener_conexion

def acceso_usuario(email, clave):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("exec sp_AccesoUsuario ?, ?", email, clave)
        usuario = cursor.fetchone()

    conexion.close()
    return usuario
