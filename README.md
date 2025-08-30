# FIT-U: Tu Entrenador Personal con IA

![FIT-U Logo](frontend/static/images/logo.png)

FIT-U es una aplicación web que te permite generar rutinas de gimnasio personalizadas utilizando inteligencia artificial (Gemini AI) y gestionar tus datos de usuario con Supabase.

## 🚀 Características

*   **Autenticación de Usuarios:** Registro e inicio de sesión seguro con Supabase Auth.
*   **Perfiles de Usuario:** Almacenamiento de nombres de usuario asociados a sus cuentas.
*   **Generación de Rutinas Personalizadas:**
    *   Utiliza Gemini AI para crear rutinas de gimnasio basadas en edad, peso, altura, género, objetivo (masa muscular, pérdida de grasa, resistencia), nivel (principiante, intermedio, avanzado) y días de entrenamiento por semana.
    *   Las rutinas incluyen ejercicios, series, repeticiones y tiempos de descanso.
*   **Almacenamiento de Rutinas:** Guarda las rutinas generadas en Supabase para futuras consultas.
*   **Interfaz Intuitiva:** Formularios sencillos para la entrada de datos y visualización de rutinas.

## 🛠️ Tecnologías Utilizadas

### Backend

*   **Flask:** Microframework web para Python.
*   **Supabase:** Base de datos de código abierto con autenticación, base de datos PostgreSQL y almacenamiento.
    *   `supabase-py`: Cliente Python para interactuar con Supabase.
*   **Google Gemini AI:** Modelo de lenguaje grande para la generación de texto (rutinas).
    *   `google-generativeai`: SDK de Python para Gemini.
*   **python-dotenv:** Para la gestión de variables de entorno.

### Frontend

*   **HTML5:** Estructura de las páginas web.
*   **CSS3:** Estilos personalizados (`style.css`) y Bootstrap para un diseño responsivo.
*   **JavaScript:** Lógica del lado del cliente para la interacción con la API.

## ⚙️ Configuración del Entorno

### Prerrequisitos

*   Python 3.8+
*   Una cuenta de Supabase
*   Una clave API de Google Gemini

### Pasos de Configuración

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/fit-u.git
    cd fit-u/backend
    ```

2.  **Crear y Activar un Entorno Virtual:**
    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Supabase:**
    *   Crea un nuevo proyecto en Supabase.
    *   Obtén tu `SUPABASE_URL` y `SUPABASE_ANON_KEY` desde la sección "API" en la configuración de tu proyecto.
    *   Obtén tu `SUPABASE_SERVICE_ROLE_KEY` desde la sección "API" (esta clave tiene permisos elevados y debe usarse con precaución en el backend).
    *   **Configurar Tablas en Supabase:**
        *   **`profiles` tabla:**
            ```sql
            CREATE TABLE public.profiles (
              id uuid REFERENCES auth.users ON DELETE CASCADE,
              display_name text,
              PRIMARY KEY (id)
            );
            ```
        *   **`routines` tabla:**
            ```sql
            CREATE TABLE public.routines (
              id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
              user_id uuid REFERENCES auth.users ON DELETE CASCADE,
              created_at timestamp with time zone DEFAULT now(),
              data jsonb
            );
            ```
        *   Asegúrate de configurar las políticas de Row Level Security (RLS) adecuadas para `profiles` y `routines` si deseas controlar el acceso a los datos desde el cliente (aunque en este proyecto se usa `SUPABASE_SERVICE_ROLE_KEY` para algunas operaciones de escritura).

5.  **Configurar Variables de Entorno:**
    *   Crea un archivo `.env` en la raíz de la carpeta `backend` (`/fit-u-main/backend/.env`) con el siguiente contenido:
        ```
        SUPABASE_URL="TU_SUPABASE_URL"
        SUPABASE_ANON_KEY="TU_SUPABASE_ANON_KEY"
        SUPABASE_SERVICE_ROLE_KEY="TU_SUPABASE_SERVICE_ROLE_KEY"
        GEMINI_API_KEY="TU_GEMINI_API_KEY"
        ```
    *   Reemplaza los valores con tus propias claves.

## 🚀 Ejecución de la Aplicación

1.  **Asegúrate de estar en el directorio `backend`:**
    ```bash
    cd /fit-u-main/backend
    ```

2.  **Ejecutar la Aplicación Flask:**
    ```bash
    python app.py
    ```

3.  **Acceder a la Aplicación:**
    *   Abre tu navegador web y ve a `http://127.0.0.1:5000/login` para iniciar sesión o registrarte.
    *   Puedes acceder directamente a las rutas:
        *   `/register`: Página de registro.
        *   `/login`: Página de inicio de sesión.
        *   `/routine`: Formulario para generar rutinas (requiere autenticación).
        *   `/dashboard`: Un ejemplo de ruta protegida.

## 📂 Estructura del Proyecto

El proyecto `fit-u-main` se organiza de la siguiente manera:

*   **`backend/`**: Contiene todo el código del servidor Flask.
    *   `app.py`: El archivo principal de la aplicación Flask, donde se inicializa la aplicación y se registran los blueprints.
    *   `requirements.txt`: Lista de todas las dependencias de Python necesarias para el backend.
    *   `supabase_helper.py`: Módulo con funciones auxiliares para interactuar con Supabase (registro, login, creación de perfiles, guardado y obtención de rutinas).
    *   `test.py`: Un archivo de prueba simple.
    *   `__init__.py`: Archivo de inicialización del paquete Python.
    *   `__pycache__/`: Carpeta generada automáticamente para archivos compilados de Python.
    *   `routes/`: Directorio que agrupa los diferentes módulos de rutas de la API.
        *   `auth_routes.py`: Define las rutas relacionadas con la autenticación de usuarios (registro y login).
        *   `routine_routes.py`: Define las rutas para la generación y gestión de rutinas de ejercicio.
        *   `__init__.py`: Archivo de inicialización del paquete `routes`.
        *   `__pycache__/`: Carpeta para archivos compilados de Python dentro de `routes`.
*   **`frontend/`**: Contiene todos los archivos estáticos y plantillas HTML para la interfaz de usuario.
    *   `static/`: Almacena archivos estáticos como CSS e imágenes.
        *   `css/`: Contiene hojas de estilo.
            *   `style.css`: Estilos CSS personalizados para la aplicación.
        *   `images/`: Contiene imágenes.
            *   `logo.png`: El logo de la aplicación.
    *   `templates/`: Contiene los archivos HTML que son renderizados por Flask.
        *   `login.html`: Plantilla para la página de inicio de sesión.
        *   `register.html`: Plantilla para la página de registro de usuarios.
        *   `routine.html`: Plantilla para el formulario de generación de rutinas.
*   **`README.md`**: Este archivo, que proporciona una descripción general del proyecto, instrucciones de configuración y uso.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras un error o tienes una sugerencia de mejora, no dudes en abrir un "issue" o enviar un "pull request".

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
