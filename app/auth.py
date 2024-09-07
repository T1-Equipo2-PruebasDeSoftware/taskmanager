import os
import json

def load_users(file_path='data/auth.json'):
    """
    Carga la lista de usuarios desde un archivo JSON.

    Args:
        file_path (str): Ruta al archivo JSON que contiene los usuarios.

    Returns:
        list: Lista de usuarios cargados desde el archivo. Si ocurre un error, se devuelve una lista vacía.
    """
    if not os.path.isfile(file_path):
        print("Error: El archivo de autenticación no se encuentra.")
        return []

    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: El archivo de autenticación está corrupto.")
        return []
    except Exception as e:
        print(f"Error al cargar el archivo de autenticación: {e}")
        return []

def authenticate(username, password):
    """
    Verifica si el usuario y la contraseña son válidos.

    Args:
        username (str): Nombre de usuario.
        password (str): Contraseña del usuario.

    Returns:
        tuple: (bool, str) donde el primer valor es True si la autenticación es exitosa y False en caso contrario,
               y el segundo valor es un mensaje de error específico.
    """
    users = load_users()
    for user in users:
        if user['username'] == username:
            if user['password'] == password:
                return True, ""
            else:
                return False, "Contraseña incorrecta."
    return False, "Usuario incorrecto."