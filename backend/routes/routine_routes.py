# backend/routes/routine_routes.py

import os
import unicodedata
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv, find_dotenv
from supabase_helper import save_routine, get_routines, supabase_auth

from google import genai
from google.genai import types

# Carga variables de entorno
load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

routine_bp = Blueprint('routine', __name__, url_prefix='/routine')

# Generar y guardar rutina
@routine_bp.route('', methods=['POST'])
def generate_routine():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if not token:
        return jsonify({"error": "No se proporcionó token"}), 401

    user_resp = supabase_auth.auth.get_user(jwt=token)
    err = getattr(user_resp, 'error', None) or (user_resp.get('error') if isinstance(user_resp, dict) else None)
    if err:
        return jsonify({"error": "Token inválido o expirado"}), 401

    user_obj = getattr(user_resp, 'user', None) or (user_resp.get('user') if isinstance(user_resp, dict) else None)
    user_id = user_obj.get('id') if isinstance(user_obj, dict) else getattr(user_obj, 'id', None)
    if not user_id:
        return jsonify({"error": "No se pudo determinar el usuario autenticado"}), 401

    payload = request.json or {}
    age = payload.get('age')
    weight = payload.get('weight')
    height = payload.get('height')
    gender = payload.get('gender')
    goal = payload.get('goal')
    level = payload.get('level')
    days = payload.get('days')
    if not all([age, weight, height, gender, goal, level, days]):
        return jsonify({"error": "Datos incompletos"}), 400

    raw_prompt = (
        f"Eres un entrenador personal profesional. Crea una rutina de gimnasio de {days} días "
        f"por semana para un usuario de {age} años, {weight} kg, {height} cm, "
        f"género {gender}, objetivo {goal} y nivel {level}. "
        "Incluye ejercicios, series, repeticiones y tiempos de descanso por serie de mínimo 2 minutos y máximo 3 minutos. "
        "En vez de conjuntos escribe series, da correctamente los nombres de los ejercicios y al lado pon en paréntesis sus nombres en inglés. "
        "Sé inteligente en cuanto a los días para entrenar todos los músculos."
    )

    # Normalizar acentos en prompt (ASCII fallback)
    prompt = unicodedata.normalize('NFKD', raw_prompt).encode('ascii', 'ignore').decode('ascii')

    try:
        # Inicializar cliente Gemini con la API key
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)  # Desactiva "pensamiento" para mayor rapidez
            ),
        )

        routine_text = response.text

    except Exception as e:
        return jsonify({"error": f"Error generando rutina con Gemini: {e}"}), 500

    routine_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "gender": gender,
        "goal": goal,
        "level": level,
        "days": days,
        "routine_text": routine_text
    }

    save_res = save_routine(user_id, routine_data)
    save_err = getattr(save_res, 'error', None) or (save_res.get('error') if isinstance(save_res, dict) else None)
    if save_err:
        return jsonify({"error": "Error guardando rutina en la base"}), 500

    return jsonify({"routine": routine_text}), 201


# Listar rutinas guardadas
@routine_bp.route('/list', methods=['GET'])
def list_routines():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if not token:
        return jsonify({"error": "No se proporcionó token"}), 401

    user_resp = supabase_auth.auth.get_user(jwt=token)
    err = getattr(user_resp, 'error', None) or (user_resp.get('error') if isinstance(user_resp, dict) else None)
    if err:
        return jsonify({"error": "Token inválido o expirado"}), 401

    user_obj = getattr(user_resp, 'user', None) or (user_resp.get('user') if isinstance(user_resp, dict) else None)
    user_id = user_obj.get('id') if isinstance(user_obj, dict) else getattr(user_obj, 'id', None)
    if not user_id:
        return jsonify({"error": "No se pudo determinar el usuario autenticado"}), 401

    res = get_routines(user_id)
    rr_err = getattr(res, 'error', None) or (res.get('error') if isinstance(res, dict) else None)
    if rr_err:
        return jsonify({"error": "Error consultando rutinas"}), 500

    rr_data = getattr(res, 'data', None) or (res.get('data') if isinstance(res, dict) else None)
    routines = rr_data or []
    return jsonify(routines), 200
