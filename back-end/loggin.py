import hashlib
import os
import secrets
import json

# Configuración del algoritmo de hashing
HASH_ALGORITHM = 'sha256'
PBKDF2_ITERATIONS = 260000
SALT_SIZE = 16

# Nombre del archivo donde se guardarán los datos de usuarios
# Usar ruta absoluta para que funcione desde cualquier directorio
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'USERS_FILE.json')

def hash_password(password):
    """
    Hashea una contraseña utilizando PBKDF2_HMAC con un salt aleatorio.
    Retorna el salt y el hash en formato hexadecimal.
    """
    salt = secrets.token_bytes(SALT_SIZE)
    hashed_password = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode('utf-8'),
        salt,
        PBKDF2_ITERATIONS
    )
    return salt.hex(), hashed_password.hex()

def verify_password(stored_salt_hex, stored_hash_hex, provided_password):
    """
    Verifica si una contraseña proporcionada coincide con un hash almacenado.
    """
    try:
        stored_salt = bytes.fromhex(stored_salt_hex)
        stored_hash = bytes.fromhex(stored_hash_hex)

        hashed_provided_password = hashlib.pbkdf2_hmac(
            HASH_ALGORITHM,
            provided_password.encode('utf-8'),
            stored_salt,
            PBKDF2_ITERATIONS
        )
        return secrets.compare_digest(hashed_provided_password, stored_hash)
    except ValueError:
        print("Error de formato en el hash o salt almacenado. Posible corrupción de datos.")
        return False
    except Exception as e:
        print(f"Error inesperado durante la verificación de contraseña: {e}")
        return False

def load_users():
    """
    Carga los usuarios desde el archivo USERS_FILE.
    Si el archivo no existe, retorna un diccionario vacío.
    """
    if not os.path.exists(USERS_FILE):
        print(f"Advertencia: El archivo '{USERS_FILE}' no existe. Se creará uno vacío.")
        return {}
    
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: El archivo '{USERS_FILE}' no es un JSON válido. Se inicializará vacío.")
        return {}
    except Exception as e:
        print(f"Error al cargar usuarios desde '{USERS_FILE}': {e}")
        return {}

def save_users(users_data):
    """
    Guarda los usuarios en el archivo USERS_FILE.
    """
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=2)
    except Exception as e:
        print(f"Error al guardar usuarios en '{USERS_FILE}': {e}")