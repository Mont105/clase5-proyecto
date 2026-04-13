import os
from flask import Flask, request, jsonify, send_from_directory
from register import register_user
from loggin import load_users, verify_password

# Ruta a la carpeta del front-end
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'front-end')

app = Flask(__name__, static_folder=FRONTEND_DIR)


# ==================== SERVIR ARCHIVOS DEL FRONTEND ====================

@app.route('/')
def serve_index():
    """Sirve la página principal."""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Sirve archivos estáticos del front-end (HTML, CSS, JS, imágenes)."""
    return send_from_directory(FRONTEND_DIR, filename)


# ==================== API ENDPOINTS ====================

@app.route('/register', methods=['POST'])
def api_register():
    """
    Endpoint para registrar un nuevo usuario.
    Espera un JSON con: username, email, password, confirm_password
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No se recibieron datos."}), 400

    username = data.get('username', '')
    email = data.get('email', '')
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    result = register_user(username, email, password, confirm_password)

    status_code = 200 if result["success"] else 400
    return jsonify(result), status_code


@app.route('/login', methods=['POST'])
def api_login():
    """
    Endpoint para iniciar sesión.
    Espera un JSON con: username, password
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No se recibieron datos."}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username:
        return jsonify({"success": False, "message": "El nombre de usuario no puede estar vacío."}), 400

    if not password:
        return jsonify({"success": False, "message": "La contraseña no puede estar vacía."}), 400

    # Cargar usuarios
    users = load_users()

    # Verificar si el usuario existe
    if username not in users:
        return jsonify({"success": False, "message": "Usuario no encontrado."}), 401

    # Verificar la contraseña
    user_data = users[username]
    if verify_password(user_data["salt"], user_data["hash"], password):
        return jsonify({"success": True, "message": f"¡Bienvenido, {username}!"}), 200
    else:
        return jsonify({"success": False, "message": "Contraseña incorrecta."}), 401


if __name__ == '__main__':
    print("=" * 50)
    print("  Servidor Backend - Sistema de Registro y Login")
    print("=" * 50)
    print(f"  Frontend servido desde: {os.path.abspath(FRONTEND_DIR)}")
    print(f"  Abre tu navegador en: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
