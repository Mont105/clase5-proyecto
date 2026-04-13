from loggin import hash_password, load_users, save_users


def register_user(username, email, password, confirm_password):
    """
    Registra un nuevo usuario con los datos proporcionados.
    Retorna un diccionario con 'success' (bool) y 'message' (str).
    """
    # Validar que los campos no estén vacíos
    if not username or not username.strip():
        return {"success": False, "message": "El nombre de usuario no puede estar vacío."}

    if not email or not email.strip():
        return {"success": False, "message": "El correo electrónico no puede estar vacío."}

    if not password:
        return {"success": False, "message": "La contraseña no puede estar vacía."}

    if password != confirm_password:
        return {"success": False, "message": "Las contraseñas no coinciden."}

    if len(password) < 4:
        return {"success": False, "message": "La contraseña debe tener al menos 4 caracteres."}

    username = username.strip()
    email = email.strip()

    # Cargar usuarios existentes
    users = load_users()

    # Verificar si el usuario ya existe
    if username in users:
        return {"success": False, "message": f"El usuario '{username}' ya existe. Intente con otro nombre."}

    # Verificar si el email ya está registrado
    for user_data in users.values():
        if user_data.get("email") == email:
            return {"success": False, "message": "Este correo electrónico ya está registrado."}

    # Hashear la contraseña
    salt, hashed_password = hash_password(password)

    # Guardar el nuevo usuario
    users[username] = {
        "salt": salt,
        "hash": hashed_password,
        "email": email
    }

    save_users(users)
    return {"success": True, "message": f"Usuario '{username}' registrado exitosamente."}