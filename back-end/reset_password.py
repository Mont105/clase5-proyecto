from loggin import hash_password, load_users, save_users


def reset_user_password(username, email, new_password, confirm_password):
    """
    Restablece la contraseña de un usuario existente.
    Verifica que el usuario exista y que el correo coincida.
    Retorna un diccionario con 'success' (bool) y 'message' (str).
    """
    # Validar que los campos no estén vacíos
    if not username or not username.strip():
        return {"success": False, "message": "El nombre de usuario no puede estar vacío."}

    if not email or not email.strip():
        return {"success": False, "message": "El correo electrónico no puede estar vacío."}

    if not new_password:
        return {"success": False, "message": "La nueva contraseña no puede estar vacía."}

    if new_password != confirm_password:
        return {"success": False, "message": "Las contraseñas no coinciden."}

    if len(new_password) < 4:
        return {"success": False, "message": "La contraseña debe tener al menos 4 caracteres."}

    username = username.strip()
    email = email.strip()

    # Cargar usuarios existentes
    users = load_users()

    # Verificar si el usuario existe
    if username not in users:
        return {"success": False, "message": "Usuario no encontrado."}

    # Verificar que el correo coincida con el del usuario
    if users[username].get("email") != email:
        return {"success": False, "message": "El correo electrónico no coincide con el usuario."}

    # Hashear la nueva contraseña
    salt, hashed_password = hash_password(new_password)

    # Actualizar la contraseña del usuario
    users[username]["salt"] = salt
    users[username]["hash"] = hashed_password

    save_users(users)
    return {"success": True, "message": f"Contraseña de '{username}' restablecida exitosamente."}
