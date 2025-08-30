from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL             = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY        = os.environ["SUPABASE_ANON_KEY"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

# Cliente para operaciones con supabase.auth (registro, login, lectura RLS)
supabase_auth    = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
# Cliente con permisos elevados para insertar datos (bypass RLS)
supabase_service = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def sign_up(email: str, password: str):
    return supabase_auth.auth.sign_up({"email": email, "password": password})

def sign_in(email: str, password: str):
    return supabase_auth.auth.sign_in_with_password({"email": email, "password": password})

def create_profile(user_id: str, display_name: str):
    payload = {"id": user_id, "display_name": display_name}
    return supabase_service.table("profiles").insert(payload).execute()

def get_profile(user_id: str):
    return supabase_auth.table("profiles").select("*").eq("id", user_id).single().execute()

def save_routine(user_id: str, routine_data: dict):
    """
    Inserta una nueva rutina en la tabla 'routines'.
    """
    return supabase_service.table("routines") \
        .insert({
            "user_id": user_id,
            "data":     routine_data
        }) \
        .execute()

def get_routines(user_id: str):
    """
    Recupera todas las rutinas del usuario ordenadas por fecha descendente.
    """
    return supabase_auth.table("routines") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .execute()
