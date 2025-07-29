import os # El buen amigo para interactuar con el sistema operativo
import re # Expresiones regulares, ¡el martillo para clavar clavos y a veces tornillos!
import sys # Para salir con estilo si las cosas se ponen feas
import time # Porque a veces hay que darle un respiro al programa (o al usuario)
import getpass # Para que las contraseñas no anden de mironas en la pantalla
import json  # Nuestro traductor universal para historiales y preferencias

import google.generativeai as genai # La estrella del show, el SDK de Google Gemini
from google.generativeai.types import HarmCategory, HarmBlockThreshold # Para no ofender a la IA (ni que ella nos ofenda)

# --- Dependencias para encriptación ---
try:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.fernet import Fernet, InvalidToken
    import base64
except ImportError:
    print(
        "¡Houston, tenemos un problema! Falta 'cryptography'. Sin ella, tus secretos no están a salvo. Instálala con: pip install cryptography"
    )
    sys.exit(1)


# --- Definición de colores ANSI para la terminal ---
# ¡Que la vida (y la terminal) no sea solo en blanco y negro! Un poco de estilo con ANSI.
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# --- Constantes ---
# Nombres de nuestros pequeños archivos secretos. El puntito al inicio es para que se escondan un poco.
ENCRYPTED_API_KEY_FILE = ".gemini_api_key_encrypted"  # Aquí guardamos la llave del tesoro, ¡pero con candado!
UNENCRYPTED_API_KEY_FILE = ".gemini_api_key_unencrypted" # La llave a la vista... no es lo ideal, pero ahí está la opción.
PREFERENCES_FILE = ".gemini_chatbot_prefs.json"  # Para recordar qué modelo te gustó más la última vez.
SALT_SIZE = 16  # Un puñadito de sal para hacer la encriptación más sabrosa (y segura). 16 bytes, como mandan los cánones.
ITERATIONS = 390_000  # ¡A darle vueltas! Cuantas más, mejor para despistar a los curiosos. OWASP dice que con esto vamos bien.


# --- Funciones de Encriptación/Desencriptación ---
# Aquí empieza la magia negra (o blanca, según se mire) para proteger esa valiosa API Key.
def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend(),
    )
    # Convertimos la contraseña en algo que Fernet pueda digerir. Base64 para que no haya sorpresas.
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def save_encrypted_api_key(api_key: str, password: str):
    """Toma tu API Key, una contraseña, y ¡zas! La guarda encriptadita."""
    try:
        salt = os.urandom(SALT_SIZE)
        derived_key = _derive_key(password, salt)
        f = Fernet(derived_key)
        encrypted_api_key = f.encrypt(api_key.encode())

        with open(ENCRYPTED_API_KEY_FILE, "wb") as key_file:
            key_file.write(salt)
            key_file.write(encrypted_api_key)
        print(
            f"{Colors.GREEN}API Key encriptada y guardada en {ENCRYPTED_API_KEY_FILE}{Colors.RESET}"
        )
        # En sistemas Unix, ponemos el archivo en modo "solo yo puedo tocarlo".
        if os.name != "nt":
            os.chmod(ENCRYPTED_API_KEY_FILE, 0o600)
    except Exception as e:
        print(f"{Colors.RED}Error al guardar la API Key encriptada: {e}{Colors.RESET}")


def load_decrypted_api_key(password: str) -> str | None:
    """Si tienes la contraseña correcta, te devuelvo tu API Key desencriptada. Si no... pues nada."""
    if not os.path.exists(ENCRYPTED_API_KEY_FILE):
        return None
    try:
        with open(ENCRYPTED_API_KEY_FILE, "rb") as key_file:
            salt = key_file.read(SALT_SIZE)
            encrypted_api_key = key_file.read()

        derived_key = _derive_key(password, salt)
        f = Fernet(derived_key)
        decrypted_api_key = f.decrypt(encrypted_api_key).decode()
        return decrypted_api_key
    except InvalidToken: # ¡Contraseña incorrecta! O alguien jugó con el archivo...
        return None
    except Exception as e:
        print(f"{Colors.RED}Error al cargar la API Key encriptada: {e}{Colors.RESET}")
        return None


def save_unencrypted_api_key(api_key: str):
    """Guarda la API Key tal cual, sin encriptar. Bajo tu propio riesgo, ¿eh?"""
    try:
        with open(UNENCRYPTED_API_KEY_FILE, "w") as key_file:
            key_file.write(api_key)
        print(
            f"{Colors.YELLOW}{Colors.BOLD}ADVERTENCIA:{Colors.RESET}{Colors.YELLOW} API Key guardada SIN ENCRIPTAR en {UNENCRYPTED_API_KEY_FILE}.{Colors.RESET}"
        )
        # Aunque no esté encriptada, al menos que no cualquiera pueda leer el archivo fácilmente.
        if os.name != "nt":
            os.chmod(UNENCRYPTED_API_KEY_FILE, 0o600)
    except Exception as e:
        print(
            f"{Colors.RED}Error al guardar la API Key sin encriptar: {e}{Colors.RESET}"
        )


def load_unencrypted_api_key() -> str | None:
    """Carga la API Key del archivo no encriptado. Más simple, pero menos seguro."""
    if not os.path.exists(UNENCRYPTED_API_KEY_FILE):
        return None
    try:
        with open(UNENCRYPTED_API_KEY_FILE, "r") as key_file:
            api_key = key_file.read().strip()
            if api_key:
                print(
                    f"{Colors.YELLOW}{Colors.BOLD}ADVERTENCIA:{Colors.RESET}{Colors.YELLOW} API Key cargada SIN ENCRIPTAR desde {UNENCRYPTED_API_KEY_FILE}.{Colors.RESET}"
                )
                return api_key
            # Si el archivo existe pero está vacío, pues no hay clave.
            return None
    except Exception as e:
        print(
            f"{Colors.RED}Error al cargar la API Key desde el archivo sin encriptar: {e}{Colors.RESET}"
        )
        return None


# --- Funciones de Preferencias (Nuevo) ---
# Para que el chatbot tenga un poquito de memoria y recuerde tus gustos.
def save_preferences(prefs: dict):
    """Guarda tus preferencias (como el último modelo usado) en un archivo JSON. Calladito, sin hacer ruido."""
    try:
        with open(PREFERENCES_FILE, "w", encoding="utf-8") as f:
            json.dump(prefs, f, ensure_ascii=False, indent=2)
        # No imprimimos nada para no ser pesados. Ya se guardó y punto.
    except Exception as e:
        print(f"{Colors.RED}Error al guardar las preferencias: {e}{Colors.RESET}")


def load_preferences() -> dict:
    """Carga las preferencias desde el archivo JSON. Si no hay, empezamos de cero."""
    if not os.path.exists(PREFERENCES_FILE):
        return {}  # Devuelve un diccionario vacío si no existe
    try:
        with open(PREFERENCES_FILE, "r", encoding="utf-8") as f:
            prefs = json.load(f)
        # Tampoco hacemos ruido al cargar.
        return prefs
    except Exception as e:
        print(
            f"{Colors.RED}Error al cargar las preferencias: {e}. Usando valores por defecto.{Colors.RESET}"
        )
        return {}


# --- Funciones de Historial de Chat (sin cambios en su lógica interna) ---
# Para que no se pierdan esas conversaciones tan interesantes con la IA.
def get_chat_history_filename(model_name: str) -> str:
    """Crea un nombre de archivo seguro para el historial, basado en el modelo. Nada de caracteres raros."""
    safe_model_name = "".join(
        c if c.isalnum() or c in ("-", "_") else "_" for c in model_name
    )
    return f"chat_history_{safe_model_name}.json"


def save_chat_history(chat_session, filename: str):
    """Guarda la conversación actual en un archivo JSON. ¡Para la posteridad!"""
    history_to_save = []
    for content in chat_session.history:
        parts_to_save = []
        for part in content.parts:
            if hasattr(part, "text"):
                parts_to_save.append({"text": part.text})
        history_to_save.append({"role": content.role, "parts": parts_to_save})
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(history_to_save, f, ensure_ascii=False, indent=2) # Con indentación para que sea legible si lo abres.
        print(f"{Colors.GREEN}Historial de chat guardado en {filename}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Error al guardar el historial: {e}{Colors.RESET}")


def load_chat_history(filename: str) -> list | None:
    """Carga un historial de chat previo desde un archivo JSON."""
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "r", encoding="utf-8") as f:
            history = json.load(f)
        print(f"{Colors.GREEN}Historial de chat cargado desde {filename}{Colors.RESET}")
        return history
    except Exception as e:
        print(
            f"{Colors.RED}Error al cargar el historial: {e}. Empezando chat nuevo.{Colors.RESET}"
        )
        return None


# --- Funciones de Formateo de Salida ---
# ¡A poner guapa la respuesta del chatbot! Que no todo es texto plano en esta vida.
def process_standard_markdown(text: str) -> str:
    """Aplica formato Markdown estándar (excepto bloques de código multilínea) usando códigos ANSI."""
    # 1. Código en línea (`código`) - Usamos Magenta para diferenciarlo de bloques de código.
    text = re.sub(r"`(.*?)`", rf"{Colors.MAGENTA}\1{Colors.RESET}", text)

    # 2. Encabezados (de más específico ### a menos específico #)
    text = re.sub(r"^### (.*)", rf"{Colors.BOLD}{Colors.GREEN}\1{Colors.RESET}", text, flags=re.MULTILINE)  # H3 Verde
    text = re.sub(r"^## (.*)", rf"{Colors.BOLD}{Colors.CYAN}\1{Colors.RESET}", text, flags=re.MULTILINE)   # H2 Cian
    text = re.sub(r"^# (.*)", rf"{Colors.BOLD}{Colors.BLUE}\1{Colors.RESET}", text, flags=re.MULTILINE)    # H1 Azul

    # 3. Listas - Procesar antes de negritas/itálicas que podrían usar '*'
    # Listas no ordenadas
    text = re.sub(r"^(\s*)\* (.*)", rf"\1{Colors.YELLOW}* {Colors.RESET}\2", text, flags=re.MULTILINE)
    text = re.sub(r"^(\s*)- (.*)", rf"\1{Colors.YELLOW}- {Colors.RESET}\2", text, flags=re.MULTILINE)
    # Listas ordenadas
    text = re.sub(r"^(\s*)(\d+\.) (.*)", rf"\1{Colors.YELLOW}\2 {Colors.RESET}\3", text, flags=re.MULTILINE)

    # 4. Negrita (**texto**)
    text = re.sub(r"\*\*(.*?)\*\*", rf"{Colors.BOLD}\1{Colors.RESET}", text)

    # 5. Itálica/Subrayado (*texto* o _texto_) - Usamos subrayado para la consola.
    # Procesar después de negrita. El `?` hace que `+` y `*` sean no codiciosos.
    text = re.sub(r"\*([^*]+?)\*", rf"{Colors.UNDERLINE}\1{Colors.RESET}", text) # *itálica*
    text = re.sub(r"_(.+?)_", rf"{Colors.UNDERLINE}\1{Colors.RESET}", text)     # _itálica_
    
    return text

def format_gemini_output(text: str) -> str:
    """Formatea la respuesta de Gemini, manejando bloques de código y Markdown estándar."""
    processed_parts = []
    last_end = 0

    # Iterar sobre los bloques de código multilínea (``` ... ```)
    for match in re.finditer(r"```(\w*)\n?(.*?)```", text, flags=re.DOTALL):
        # Texto antes del bloque de código actual (procesar con Markdown estándar)
        pre_match_text = text[last_end:match.start()]
        processed_parts.append(process_standard_markdown(pre_match_text))

        # Formatear el bloque de código
        lang = match.group(1) or ""
        code_content = match.group(2).strip('\n') # Contenido del código
        
        # Indentar el contenido del bloque de código para mejor legibilidad
        indented_code = "\n".join([f"  {line}" for line in code_content.split('\n')])
        
        code_block_formatted = ""
        if lang:
            code_block_formatted = f"{Colors.YELLOW}```{lang}{Colors.RESET}\n{Colors.CYAN}{indented_code}{Colors.RESET}\n{Colors.YELLOW}```{Colors.RESET}"
        else:
            code_block_formatted = f"{Colors.YELLOW}```{Colors.RESET}\n{Colors.CYAN}{indented_code}{Colors.RESET}\n{Colors.YELLOW}```{Colors.RESET}"
        processed_parts.append(code_block_formatted)
        
        last_end = match.end()

    # Texto restante después del último bloque de código (procesar con Markdown estándar)
    remaining_text = text[last_end:]
    processed_parts.append(process_standard_markdown(remaining_text))
    
    return "".join(processed_parts)


# --- ¡Aquí empieza la fiesta! La función principal del chatbot ---
def display_welcome_message():
    """Muestra un mensaje de bienvenida chulo con arte ASCII y novedades."""
    pygemai_art = f"""
{Colors.BOLD}{Colors.CYAN}
PPPPPPP   YY    YY   GGGGGG   EEEEEEE  MMMMM    MMMMM      AAAAA      IIIIIIII
PP    PP   YY  YY   GG        EE       MM MMM  MMM MM     AA   AA        II
PP    PP    YYYY    GG   GGG  EEEEEEE  MM  MMMMMM  MM    AAAAAAAAA       II
PPPPPPP      YY     GG    GG  EE       MM   MMMM   MM   AA       AA      II
PP           YY      GGGGGG   EEEEEEE  MM    MM    MM  AA         AA  IIIIIIII
PP_____________________________________________________________________________        
{Colors.RESET}
"""
    welcome_text = f"{Colors.BOLD}{Colors.GREEN}¡Bienvenido a PyGemAi v1.2.0!{Colors.RESET}"
    developer_text = f"Un desarrollo de: {Colors.YELLOW}Julio César Martínez{Colors.RESET}"
    
    changes_title = f"\n{Colors.BOLD}{Colors.MAGENTA}--- Novedades en esta versión ---{Colors.RESET}"
    changes_list = [
        f"{Colors.YELLOW}* {Colors.RESET}¡Ahora las respuestas del chatbot tienen {Colors.BOLD}formato{Colors.RESET}! (negritas, listas, código, etc.)",
        f"{Colors.YELLOW}* {Colors.RESET}Mensaje de bienvenida más {Colors.CYAN}molón{Colors.RESET} (¡lo estás viendo!).",
        f"{Colors.YELLOW}* {Colors.RESET}Pequeñas mejoras y correcciones internas (el trabajo sucio que no se ve).",
    ]

    print(pygemai_art)
    print(f"{welcome_text:^80}") # Centramos un poco el texto de bienvenida
    print(f"{developer_text:^80}") # Y el del desarrollador
    print(changes_title)
    for change in changes_list:
        print(change)
    print(f"\n{Colors.BLUE}--------------------------------------------------------------------------------{Colors.RESET}")
    time.sleep(1.5) # Una pequeña pausa para que se pueda leer antes de que empiece el resto.


def run_chatbot():
    # --- Configuración de la clave de API ---
    # Primero lo primero: necesitamos la llave mágica (API Key).
    display_welcome_message() # ¡Aquí llamamos a nuestra nueva función de bienvenida!
    API_KEY = None
    key_loaded_from_file = False # Para saber si ya la cargamos de un archivo y no preguntar de nuevo si la guardamos.
    print(
        f"{Colors.YELLOW}Se encontró un archivo de API Key encriptado ({ENCRYPTED_API_KEY_FILE}).{Colors.RESET}"
    )
    password_attempts = 0
    max_password_attempts = 3
    while password_attempts < max_password_attempts: # Damos unos intentos para la contraseña, ¡no somos tan malos!
        password = getpass.getpass(
            f"{Colors.CYAN}Ingresa la contraseña para desencriptar la API Key (Enter para omitir): {Colors.RESET}"
        ) # Esta línea se repite abajo, considerar refactorizar el bucle
        if not password:
            print(
                f"{Colors.YELLOW}Omitiendo carga desde archivo encriptado.{Colors.RESET}"
            )
            break
        temp_api_key = load_decrypted_api_key(password)
        if temp_api_key:
            API_KEY = temp_api_key
            key_loaded_from_file = True
            print(
                f"{Colors.GREEN}API Key cargada y desencriptada exitosamente desde el archivo.{Colors.RESET}"
            )
            break
        else:
            password_attempts += 1
            print(
                f"{Colors.RED}Contraseña incorrecta o archivo corrupto.{Colors.RESET}"
            )
            if password_attempts >= max_password_attempts:
                print(
                    f"{Colors.RED}Demasiados intentos fallidos. No se pudo cargar la API Key desde el archivo encriptado.{Colors.RESET}"
                ) # Si fallas mucho, te preguntamos si quieres borrar el archivo, por si acaso.
                delete_choice = (
                    input(
                        f"{Colors.YELLOW}¿Deseas eliminar el archivo de API Key encriptado ({ENCRYPTED_API_KEY_FILE}) debido a fallos? (s/N): {Colors.RESET}"
                    )
                    .strip()
                    .lower()
                )
                if delete_choice == "s":
                    try:
                        os.remove(ENCRYPTED_API_KEY_FILE)
                        print(
                            f"{Colors.GREEN}Archivo {ENCRYPTED_API_KEY_FILE} eliminado.{Colors.RESET}"
                        )
                    except Exception as e:
                        print(
                            f"{Colors.RED}No se pudo eliminar el archivo: {e}{Colors.RESET}"
                        )
                break

    # Si no la encontramos encriptada (o el usuario omitió), buscamos la versión sin encriptar.
    if API_KEY is None and os.path.exists(UNENCRYPTED_API_KEY_FILE):
        print(
            f"{Colors.YELLOW}Intentando cargar desde archivo de API Key sin encriptar ({UNENCRYPTED_API_KEY_FILE}).{Colors.RESET}"
        )
        temp_api_key = load_unencrypted_api_key()
        if temp_api_key:
            API_KEY = temp_api_key
            key_loaded_from_file = True
            print(
                f"{Colors.GREEN}API Key cargada exitosamente desde el archivo (sin encriptar).{Colors.RESET}"
            )
        elif os.path.exists( # Si el archivo existe pero no pudimos leer la clave (vacío, corrupto...)
            UNENCRYPTED_API_KEY_FILE
        ):  # Si la carga falló pero el archivo existe (ej. vacío o error de lectura)
            delete_choice = (
                input(
                    f"{Colors.YELLOW}El archivo de API Key sin encriptar ({UNENCRYPTED_API_KEY_FILE}) no pudo ser leído correctamente o está vacío. ¿Deseas eliminarlo? (s/N): {Colors.RESET}"
                )
                .strip()
                .lower()
            )
            if delete_choice == "s":
                try:
                    os.remove(UNENCRYPTED_API_KEY_FILE)
                    print(
                        f"{Colors.GREEN}Archivo {UNENCRYPTED_API_KEY_FILE} eliminado.{Colors.RESET}"
                    )
                except Exception as e:
                    print(f"{Colors.RED}No se pudo eliminar el archivo: {e}{Colors.RESET}")

    # 3. Si sigue sin aparecer, probamos con la variable de entorno GOOGLE_API_KEY. ¡Un clásico!
    if API_KEY is None:
        API_KEY = os.getenv("GOOGLE_API_KEY")
        if API_KEY:
            print(
                f"{Colors.GREEN}API Key cargada desde la variable de entorno GOOGLE_API_KEY.{Colors.RESET}"
            )
        else: # ¡Último recurso! Pedírsela directamente al usuario.
            # 4. Si aún no hay clave, pedir al usuario que la ingrese.
            print(
                f"{Colors.YELLOW}La clave de API no se encontró en archivos locales ni en la variable de entorno GOOGLE_API_KEY.{Colors.RESET}"
            )
            print(
                f"{Colors.YELLOW}Puedes configurar la variable de entorno GOOGLE_API_KEY o crear un archivo '.gemini_api_key_encrypted'.{Colors.RESET}"
            )
            print(
                f"{Colors.YELLOW}Alternativamente, puedes ingresarla directamente ahora:{Colors.RESET}"
            )

            API_KEY = input(
                f"{Colors.CYAN}Por favor, ingresa tu clave de API de Gemini: {Colors.RESET}"
            ).strip()
            if not API_KEY:
                print(
                    f"{Colors.RED}Error: No se ingresó ninguna clave de API.{Colors.RESET}"
                )
                sys.exit(1)

    # 5. Si conseguimos la API Key (y no fue de un archivo), preguntamos si quiere guardarla para la próxima.
    if API_KEY and not key_loaded_from_file:
        print(
            f"\n{Colors.CYAN}¿Cómo deseas guardar esta API Key para futuros usos?{Colors.RESET}"
        )
        print(f"  {Colors.CYAN}1. Encriptada (recomendado){Colors.RESET}")
        print(
            f"  {Colors.CYAN}2. Sin encriptar ({Colors.RED}NO RECOMENDADO - RIESGO DE SEGURIDAD{Colors.CYAN}){Colors.RESET}"
        )
        print(f"  {Colors.CYAN}3. No guardar{Colors.RESET}")
        save_choice_input = input(
            f"{Colors.CYAN}Elige una opción (1/2/3, Enter para no guardar): {Colors.RESET}"
        ).strip()

        if save_choice_input == "1":
            while True:
                password = getpass.getpass(
                    f"{Colors.CYAN}Ingresa una contraseña para encriptar la API Key (mínimo 8 caracteres, dejar en blanco para cancelar): {Colors.RESET}"
                )
                if not password:
                    print(f"{Colors.YELLOW}Guardado encriptado cancelado.{Colors.RESET}")
                    break
                if len(password) < 8:
                    print(
                        f"{Colors.RED}La contraseña debe tener al menos 8 caracteres.{Colors.RESET}"
                    )
                    continue
                password_confirm = getpass.getpass(
                    f"{Colors.CYAN}Confirma la contraseña: {Colors.RESET}"
                )
                if password == password_confirm:
                    save_encrypted_api_key(API_KEY, password)
                    break
                else:
                    print(
                        f"{Colors.RED}Las contraseñas no coinciden. Inténtalo de nuevo.{Colors.RESET}"
                    )
        elif save_choice_input == "2":
            save_unencrypted_api_key(API_KEY)
        elif save_choice_input == "3" or not save_choice_input:
            print(f"{Colors.YELLOW}API Key no guardada localmente.{Colors.RESET}")
        else:
            print(
                f"{Colors.YELLOW}Opción inválida. API Key no guardada localmente.{Colors.RESET}"
            )

    # 6. ¡Momento de la verdad! Si no hay API Key, no hay paraíso (ni chatbot).
    if not API_KEY:
        print(
            f"{Colors.RED}Error: No se pudo obtener la API Key por ningún método. Saliendo.{Colors.RESET}"
        )
        sys.exit(1)

    try:
        # Configuramos la API de Gemini con la clave. ¡Crucemos los dedos!
        genai.configure(api_key=API_KEY)
        print(f"\n{Colors.GREEN}API de Gemini configurada correctamente.{Colors.RESET}")
        time.sleep(0.5) # Una pausita para que el mensaje se lea.
    except Exception as e:
        print(
            f"{Colors.RED}Error al configurar la API con la clave proporcionada: {e}{Colors.RESET}"
        )
        print(f"{Colors.RED}Verifica que la clave de API sea correcta.{Colors.RESET}")
        sys.exit(1)

    # --- Selección de Modelo (Modificado) ---
    # Ahora, a elegir el cerebro de la operación.
    print(
    f"\n{Colors.BOLD}{Colors.BLUE}--- Selección de Modelo de Gemini ---{Colors.RESET}"
    )
    all_models_list = []
    available_for_generation = []
    # Si algún día usamos modelos de embedding u otros, aquí se podrían añadir.

    try:
        # Le preguntamos a Gemini qué modelos tiene disponibles.
        all_models_list = list(genai.list_models())
        for m in all_models_list:
            if "generateContent" in m.supported_generation_methods: # Solo nos interesan los que saben "hablar".
                available_for_generation.append(m)
            # elif 'embedContent' in m.supported_generation_methods: # Descomentar si es necesario
            #     available_for_embedding.append(m)
            # else:
            #     other_models.append(m)

        if not available_for_generation:
            # Si no hay modelos para generar contenido, pues... apaga y vámonos.
            print(
                f"{Colors.RED}No se encontraron modelos disponibles para generación de contenido.{Colors.RESET}"
            )
            sys.exit(1)

        def model_sort_key(model_obj): # Función para ordenar los modelos de forma "inteligente".
            name = model_obj.name  # El nombre es algo como 'models/gemini-1.5-pro-latest'
            # Extraer el nombre real del modelo para la ordenación
            actual_name_part = name.split("/")[-1]

            latest_score = 1 if "latest" in actual_name_part.lower() else 0
            pro_score = 1 if "pro" in actual_name_part.lower() else 0
            flash_score = 1 if "flash" in actual_name_part.lower() else 0
            # Para versiones como gemini-1.0-pro, gemini-1.5-pro.
            # Buscamos patrones de versión para ordenarlos numéricamente.
            version_match = re.search(r"(\d+)(?:[.\-_](\d+))?", actual_name_part)
            v_major, v_minor = 0, 0
            if version_match:
                v_major = int(version_match.group(1))
                if version_match.group(2):
                    v_minor = int(version_match.group(2))

            # Criterios de ordenación: los "latest" y "pro" primero, luego por versión, etc.
            return (
                -latest_score,  # Puntuaciones más altas primero (por eso el negativo)
                -pro_score,
                -flash_score,
                -v_major,
                -v_minor,
                actual_name_part,  # Orden alfabético como último recurso
            )

        available_for_generation.sort(key=model_sort_key) # ¡A ordenar se ha dicho!

        # Cargamos las preferencias para ver si ya usó un modelo antes.
        preferences = load_preferences()
        last_used_model_name = preferences.get("last_used_model")
        DEFAULT_MODEL_NAME = None

        if last_used_model_name: # Si hay un modelo guardado...
            # Verificar si el último modelo usado sigue disponible
            for m_obj in available_for_generation:
                if m_obj.name == last_used_model_name:
                    DEFAULT_MODEL_NAME = last_used_model_name
                    # Moverlo al principio de la lista para que sea la opción 0 (o 1 para el usuario)
                    # y también el default si el usuario presiona Enter
                    idx = available_for_generation.index(m_obj)
                    m_pop = available_for_generation.pop(idx)
                    available_for_generation.insert(0, m_pop)
                    print(
                        f"{Colors.YELLOW}Último modelo usado: {DEFAULT_MODEL_NAME}{Colors.RESET}"
                    )
                    break
            if not DEFAULT_MODEL_NAME: # Si el modelo guardado ya no existe o no es válido.
                print(
                    f"{Colors.YELLOW}El último modelo usado ({last_used_model_name}) ya no está disponible o es inválido.{Colors.RESET}"
                )

        if ( # Si no hay un "último modelo usado" válido, el primero de la lista ordenada será el default.
            not DEFAULT_MODEL_NAME and available_for_generation
        ):  # Si no se cargó o no es válido el último usado
            DEFAULT_MODEL_NAME = available_for_generation[0].name

        print(
            f"\n{Colors.BOLD}Modelos disponibles para Generación de Contenido:{Colors.RESET}"
        ) # Mostramos la lista de modelos disponibles.
        print(f"{Colors.BOLD}Selecciona uno por número para chatear:{Colors.RESET}")
        for i, m_enum in enumerate(available_for_generation):
            default_indicator = ""
            if m_enum.name == DEFAULT_MODEL_NAME and m_enum.name == last_used_model_name:
                default_indicator = (
                    f" ({Colors.GREEN}Por defecto - Último usado{Colors.RESET})"
                )
            elif m_enum.name == DEFAULT_MODEL_NAME:
                default_indicator = f" ({Colors.GREEN}Por defecto{Colors.RESET})"
            elif (
                m_enum.name == last_used_model_name
            ):  # Ya no es el default general, pero fue el último usado
                default_indicator = f" ({Colors.YELLOW}Último usado{Colors.RESET})"

            print(f"{Colors.YELLOW}{i + 1}.{Colors.RESET} {m_enum.name}{default_indicator}")

        if DEFAULT_MODEL_NAME: # Si hay un modelo por defecto, se lo decimos al usuario.
            print(
                f"\n({Colors.GREEN}Presiona Enter para usar el modelo por defecto:{Colors.RESET} {DEFAULT_MODEL_NAME})"
            )
        else:  # No debería ocurrir si available_for_generation tiene elementos
            print(f"{Colors.RED}¡Uy! No hay modelo por defecto. Algo raro pasó.{Colors.RESET}")


    except Exception as e:
        print(f"{Colors.RED}Error al listar o procesar modelos: {e}{Colors.RESET}")
        print(
            f"{Colors.RED}Asegúrate de que tu clave de API es correcta y tienes conexión a internet.{Colors.RESET}"
        )
        sys.exit(1)

    if not available_for_generation:  # Por si las moscas, volvemos a chequear.
        print(
            f"{Colors.RED}No se puede seleccionar un modelo para generación ya que no hay disponibles.{Colors.RESET}"
        )
        sys.exit(1)

    MODEL_NAME = None
    while True: # Bucle hasta que el usuario elija un modelo válido.
        prompt_text = f"{Colors.CYAN}Ingresa el número del modelo para chatear"
        if DEFAULT_MODEL_NAME:
            prompt_text += f" o presiona Enter para usar ({DEFAULT_MODEL_NAME})"
        prompt_text += f": {Colors.RESET}"
        user_input_model_choice = input(prompt_text).strip()

        if not user_input_model_choice and DEFAULT_MODEL_NAME:
            # Si presiona Enter y hay default, ¡ese es!
            MODEL_NAME = DEFAULT_MODEL_NAME
            print(f"{Colors.GREEN}Usando modelo por defecto:{Colors.RESET} {MODEL_NAME}")
            break
        elif user_input_model_choice: # Si ingresó algo...
            try:
                selected_index = int(user_input_model_choice) - 1
                if 0 <= selected_index < len(available_for_generation):
                    MODEL_NAME = available_for_generation[selected_index].name
                    print(f"{Colors.GREEN}Modelo seleccionado:{Colors.RESET} {MODEL_NAME}")
                    break
                else:
                    print(
                        f"{Colors.RED}Número fuera de rango. Por favor, ingrese un número válido.{Colors.RESET}"
                    )
            except ValueError:
                print(
                    f"{Colors.RED}Entrada inválida. Por favor, ingrese un número o presiona Enter.{Colors.RESET}"
                ) # Si no ingresó un número...
        elif (
            not DEFAULT_MODEL_NAME
        ):  # Si no hay modelo por defecto y el usuario no ingresó nada
            print(
                f"{Colors.RED}No hay modelo por defecto disponible. Por favor, selecciona un número de la lista.{Colors.RESET}"
            ) # Esto es por si acaso, no debería pasar si hay modelos.

    # Guardamos el modelo elegido en las preferencias para la próxima.
    if MODEL_NAME:
        preferences["last_used_model"] = MODEL_NAME
        save_preferences(preferences)

    time.sleep(0.5) # Otra pausita.

    # --- ¡A CHATEAR! El bucle principal de la conversación ---
    if MODEL_NAME:
        print(f"\n{Colors.GREEN}Iniciando chat con el modelo '{MODEL_NAME}'.{Colors.RESET}")
        print(
            f"{Colors.YELLOW}Escribe 'salir', 'exit' o 'quit' para terminar.{Colors.RESET}"
        )
        # Preparamos el nombre del archivo de historial y vemos si quiere cargar uno anterior.
        history_filename = get_chat_history_filename(MODEL_NAME)
        initial_history = []
        
        load_hist_choice = (
            input(
                f"{Colors.CYAN}¿Deseas cargar el historial anterior para este modelo ({history_filename})? (S/n): {Colors.RESET}"
            )
            .strip()
            .lower()
        )
        if load_hist_choice == "" or load_hist_choice == "s":
            loaded_history = load_chat_history(history_filename)
            if loaded_history:
                initial_history = loaded_history
        else:
            print(f"{Colors.YELLOW}Empezando una nueva sesión de chat.{Colors.RESET}")
        
        try:
            # Configuramos la seguridad del modelo. No queremos que se porte mal.
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
            model = genai.GenerativeModel(MODEL_NAME, safety_settings=safety_settings)
            chat = model.start_chat(history=initial_history) # ¡Y que comience la charla!
        
            while True:
                print(f"{Colors.BOLD}{Colors.CYAN}Tú: {Colors.RESET}", end="")
                user_input = ""
                try:
                    user_input = input().strip()
                except KeyboardInterrupt:  # Si el usuario se cansa y presiona Ctrl+C.
                    print(f"\n{Colors.YELLOW}Saliendo del chat...{Colors.RESET}")
                    break  # Sale del bucle de chat
        
                if user_input.lower() in ["salir", "exit", "quit"]: # Formas educadas de despedirse.
                    break
                if not user_input:
                    continue
        
                print(
                    f"{Colors.BOLD}{Colors.MAGENTA}{MODEL_NAME.split('/')[-1]}: {Colors.RESET}",
                    end="",
                )  # Mostramos el nombre corto del modelo para saber quién habla.
                try:
                    response = chat.send_message(user_input, stream=True)
                    full_response_text_parts = []
                    blocked_by_prompt_feedback = False

                    for chunk in response:
                        # Vamos juntando los pedacitos de la respuesta.
                        if hasattr(chunk, "text"):
                            full_response_text_parts.append(chunk.text)

                        if chunk.prompt_feedback and chunk.prompt_feedback.block_reason:
                            print(
                                f"\n{Colors.RED}Tu prompt fue bloqueado: {chunk.prompt_feedback.block_reason_message}{Colors.RESET}"
                            )
                            blocked_by_prompt_feedback = True
                            break # Si el prompt se bloquea, no hay más que decir.
                    
                    if not blocked_by_prompt_feedback:
                        # Si todo fue bien, juntamos la respuesta, la formateamos y la mostramos.
                        final_text = "".join(full_response_text_parts)
                        formatted_text = format_gemini_output(final_text)
                        print(formatted_text, end="", flush=True) # Usar end="" para que el print() de abajo controle el salto de línea final

                    print() # Asegura un salto de línea después de la respuesta completa o mensaje de bloqueo.
                # Si hay problemas con la API durante el envío/recepción.
                except Exception as e:
                    print(
                        f"\n{Colors.RED}Error al enviar mensaje o recibir respuesta: {e}{Colors.RESET}"
                    )
                    continue
        
        except Exception as e:
            # Un error inesperado en el chat. Suele pasar.
            print(
                f"{Colors.RED}Ocurrió un error inesperado durante el chat: {e}{Colors.RESET}"
            )
            print(f"{Colors.RED}El chat ha terminado.{Colors.RESET}")
    else:
        # Si por alguna razón no se seleccionó modelo (no debería pasar si todo va bien).
        print(f"{Colors.RED}No se seleccionó ningún modelo. Saliendo.{Colors.RESET}")

    # Mover la lógica de guardar historial fuera del try/except del bucle de chat,
    # para que se pregunte incluso si el chat termina abruptamente (Ctrl+C).
    if MODEL_NAME and 'chat' in locals() and chat.history: # Solo si hubo un chat y tiene historial
        save_hist_choice = (
            input(
                f"{Colors.CYAN}¿Deseas guardar el historial de esta sesión en '{history_filename}'? (S/n): {Colors.RESET}"
            )
            .strip()
            .lower()
        )
        if save_hist_choice == "" or save_hist_choice == "s":
            save_chat_history(chat, history_filename)

    print(f"\n{Colors.BOLD}{Colors.BLUE}--- Script finalizado. ¡Hasta la próxima! ---{Colors.RESET}")


# Este es el conjuro para que run_chatbot() se ejecute solo cuando corremos este archivo directamente.
# Si alguien lo importa como módulo, no queremos que el chatbot se inicie solo.
if __name__ == "__main__":
    run_chatbot()

##<PyGemAi.py>
##Copyright (C) <2025> <Julio Cèsar Martìnez> <julioglez@gmail.com>
##
##This program is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##You should have received a copy of the GNU General Public License
##along with this program.  If not, see <https://www.gnu.org/licenses/>.