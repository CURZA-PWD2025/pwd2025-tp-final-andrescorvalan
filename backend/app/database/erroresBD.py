class DBErrorData(Exception):
    # Errores de datos (Duplicados, FK, datos inválidos). 
    # Se muestran al usuario.
    pass

class DBException(Exception):
    # Errores técnicos (Conexión, tabla inexistente, sintaxis SQL). 
    # Se loguean para debug.
    pass