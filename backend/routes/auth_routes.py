# backend/routes/auth_routes.py

from flask import Blueprint, request, jsonify
from supabase_helper import sign_up, sign_in, create_profile, get_profile

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")
    display_name = data.get("display_name")

    if not email or not password or not display_name:
        return jsonify({"error": "Email, contraseña y nombre son obligatorios"}), 400

    # Registro en Supabase Auth
    res = sign_up(email, password)
    error = getattr(res, "error", None)
    if error:
        msg = getattr(error, "message", None) or str(error)
        return jsonify({"error": msg}), 400

    user = getattr(res, "user", None)
    user_id = getattr(user, "id", None)
    if not user_id:
        return jsonify({"error": "No se pudo obtener el ID de usuario"}), 500

    # Crear perfil en la tabla 'profiles' usando Service Role Key
    try:
        create_profile(user_id, display_name)
    except Exception as e:
        return jsonify({"error": f"Error al crear perfil: {e}"}), 500

    # Respuesta de registro exitosa
    user_data = {"id": user_id, "email": getattr(user, "email", None)}
    return jsonify({"user": user_data}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    # Autenticación en Supabase Auth
    res = sign_in(email, password)
    error = getattr(res, "error", None)
    if error:
        msg = getattr(error, "message", None) or str(error)
        return jsonify({"error": msg}), 400

    session = getattr(res, "session", None)
    user = getattr(res, "user", None)
    user_id = getattr(user, "id", None)
    if not user_id:
        return jsonify({"error": "No se pudo obtener el ID de usuario"}), 500

    # Recuperar perfil; si no existe, devolvemos {}
    try:
        profile_res = get_profile(user_id)
        profile_data = getattr(profile_res, "data", {}) or {}
    except Exception:
        profile_data = {}

    return jsonify({
        "access_token": getattr(session, "access_token", None),
        "refresh_token": getattr(session, "refresh_token", None),
        "user": {
            "id": user_id,
            "email": getattr(user, "email", None),
            "profile": profile_data
        }
    }), 200
