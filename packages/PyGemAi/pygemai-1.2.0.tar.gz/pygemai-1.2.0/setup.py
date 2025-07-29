import setuptools

# Intentar leer el contenido de README.md para la descripción larga
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Un chatbot CLI para interactuar con modelos Gemini de Google, con gestión segura de API Keys, historial de chat y selección de modelos."

setuptools.setup(
    name="PyGemAi",  # Nombre del paquete como aparecerá en PyPI
    version="1.2.0",  # ¡Nueva versión con bienvenida molona y formato!
    author="Julio César Martínez",
    author_email="julioglez@gmail.com",
    description="Chatbot CLI para Google Gemini con gestión de API Keys, historial y selección de modelos.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Especifica que el README es Markdown
    url="https://github.com/julesklord/PyGemAi",

    # Define que el código fuente de los paquetes está en el directorio 'src/'
    package_dir={"": "src"},
    # Encuentra automáticamente los paquetes dentro de 'src/'
    # e incluye específicamente 'pygemai_cli' y sus submódulos
    packages=setuptools.find_packages(
        where="src", include=["pygemai_cli", "pygemai_cli.*"]
    ),

    # Lista de dependencias que se instalarán con tu paquete
    install_requires=[
        "google-generativeai>=0.5.0", # Revisa la última versión estable recomendada
        "cryptography>=3.0.0",        # Revisa la última versión estable recomendada
        # Las dependencias como 'os', 'sys', 'json', 'getpass', etc., son parte de la librería estándar de Python
    ],

    # Metadatos para PyPI: clasifica tu paquete
    classifiers=[
        "Development Status :: 4 - Beta",  # O 4 - Beta, 5 - Production/Stable
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Communications :: Chat",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Utilities",
    ],

    python_requires=">=3.8",  # Versión mínima de Python requerida por tu script

    # Define los scripts de consola que se crearán al instalar el paquete
    entry_points={
        "console_scripts": [
            "pygemai = pygemai_cli.main:run_chatbot", # Comando 'pygemai' ejecuta 'run_chatbot' de 'src/pygemai_cli/main.py'
        ],
    },
)
