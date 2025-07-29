# PyGemAi: Chatbot CLI para Modelos Google Gemini

  [English Version](#english-version)

  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  [![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![PyPI version](https://img.shields.io/pypi/v/pygemai.svg)](https://pypi.org/project/pygemai/)
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
  [![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/julesklord/PyGemAi/issues)

  PyGemAi es una aplicación de línea de comandos (CLI) que te permite interactuar de forma sencilla y eficiente con los modelos de Inteligencia Artificial de Google Gemini directamente desde tu terminal.

## Screenshots v1.2

![PyGemAi Screenshot 1](docs/screenshots/screenshot1.png)
![PyGemAi Screenshot 2](docs/screenshots/screenshot2.png)
![PyGemAi Screenshot 3](docs/screenshots/screenshot3.png)

## Características Principales

* **Interfaz de Chat Intuitiva:** Conversa con los modelos Gemini de forma fluida.
* **Gestión Segura de Clave API:**
  * Soporte para carga desde variable de entorno (`GOOGLE_API_KEY`).
  * Opción para guardar la clave API localmente de forma encriptada con contraseña.
  * Opción para guardar sin encriptar (no recomendado) o no guardar localmente.
  * Manejo de intentos de contraseña y eliminación segura de archivos de clave corruptos.
* **Selección Dinámica de Modelos:**
  * Lista y permite seleccionar entre los modelos Gemini disponibles para generación de contenido.
  * Ordena los modelos por relevancia (priorizando "latest", "pro", "flash").
  * Recuerda y sugiere el último modelo utilizado.
* **Historial de Conversaciones:**
  * Opción para cargar el historial de chat previo para un modelo específico.
  * Opción para guardar la sesión de chat actual al finalizar.
  * Los historiales se guardan en archivos `.json` separados por modelo.
* **Personalización:**
  * Guarda las preferencias del último modelo usado.
  * Uso de colores ANSI para una mejor legibilidad en la terminal.
* **Empaquetado y Listo para Usar:** Configurado con `setup.py` y `pyproject.toml` para una fácil instalación y uso del comando `pygemai`.

## Requisitos Previos

* Python 3.8 o superior.
* `pip` (el gestor de paquetes de Python).
* Una Clave API de Google Gemini válida (puedes obtenerla en [Google AI Studio](https://aistudio.google.com/)).

## Instalación

1. **Clona el Repositorio:**

    ```bash
    git clone https://github.com/julesklord/PyGemAi.git
    cd PyGemAi
    ```

2. **Crea y Activa un Entorno Virtual (Recomendado):**

    ```bash
    python3 -m venv .venv
    ```

    Activación (ejemplos):
    * Linux/macOS (bash/zsh): `source .venv/bin/activate`
    * Linux/macOS (fish): `source .venv/bin/activate.fish`
    * Windows (cmd): `.venv\Scripts\activate.bat`
    * Windows (PowerShell): `.venv\Scripts\Activate.ps1`

3. **Instala PyGemAi y sus Dependencias:**
    Desde el directorio raíz del proyecto (donde está `setup.py`), ejecuta:

    ```bash
    pip install -e .
    ```

    Esto instalará el paquete `PyGemAi` en modo editable y el comando `pygemai` estará disponible mientras tu entorno virtual esté activado. Las dependencias principales son `google-generativeai` y `cryptography`.

## Configuración de la Clave API

Al ejecutar `pygemai` por primera vez, o si no se detecta una clave API, se te guiará para configurarla. Tienes varias opciones:

* Usar la variable de entorno `GOOGLE_API_KEY`.
* Ingresarla manualmente y elegir guardarla de forma encriptada (recomendado), sin encriptar, o no guardarla.

Para más detalles sobre la configuración y gestión de la clave API, consulta la [Guía de Uso detallada (`GUIDE_OF_USE.md`)](GUIDE_OF_USE.md).

## Uso Básico

Una vez instalado y configurada la clave API:

1. **Ejecuta el Chatbot:**
    Abre tu terminal (con el entorno virtual activado) y escribe:

    ```bash
    pygemai
    ```

2. **Selecciona un Modelo:** Sigue las instrucciones en pantalla para elegir un modelo de IA.
3. **Chatea:** Escribe tus mensajes y presiona Enter.
4. **Sal del Chat:** Escribe `salir`, `exit`, `quit`, o presiona `Ctrl+C`.
5. **Guarda el Historial:** Se te preguntará si deseas guardar el historial de la sesión.

Para una explicación completa de todas las características, opciones de línea de comandos (si las hubiera en el futuro), y solución de problemas, por favor consulta la [**Guía de Uso (`GUIDE_OF_USE.md`)**](GUIDE_OF_USE.md).

## Estructura del Proyecto (para Desarrolladores)

Este proyecto utiliza una estructura `src/` donde el paquete principal `pygemai_cli` contiene la lógica de la aplicación (`main.py`).

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un *issue* para discutir cambios importantes o reportar errores. Si deseas contribuir con código, considera hacer un *fork* del repositorio y enviar un *pull request*.

## Licencia

Este proyecto está licenciado bajo los términos de la **GNU General Public License v3.0 o posterior**.
Consulta el archivo [LICENSE](LICENSE) para más detalles.

Copyright (C)  <Julio César Martínez> <julioglez@gmail.com>

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la Licencia Pública General GNU publicada por la Fundación
para el Software Libre, ya sea la versión 3 de la Licencia, o (a su opción)
cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil, pero SIN NINGUNA
GARANTÍA; sin siquiera la garantía implícita de COMERCIABILIDAD o IDONEIDAD
PARA UN PROPÓSITO PARTICULAR. Consulte la Licencia Pública General GNU para más detalles.  

Usted debería haber recibido una copia de la Licencia Pública General GNU junto
con este programa. Si no, consulte <https://www.gnu.org/licenses/>.  

## Contacto

Julio César Martínez - <julioglez@gmail.com>

### **Desarrollado con ❤️ y Python.**

---

#### English Version

[English Version](#english-version)

## PyGemAi: CLI Chatbot for Google Gemini Models

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/pygemai.svg)](https://pypi.org/project/pygemai/) <!-- Replace with your package name if different or remove if not on PyPI -->
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/YOUR_GITHUB_USERNAME/PyGemAi/issues) <!-- Replace YOUR_GITHUB_USERNAME/PyGemAi -->

PyGemAi is a command-line interface (CLI) application that allows you to easily and efficiently interact with Google Gemini Artificial Intelligence models directly from your terminal.

## Main Features

* **Intuitive Chat Interface:** Converse fluently with Gemini models.
* **Secure API Key Management:**
  * Support for loading from environment variable (`GOOGLE_API_KEY`).
  * Option to save the API key locally encrypted with a password.
  * Option to save unencrypted (not recommended) or not save locally.
  * Password attempt handling and secure deletion of corrupted key files.
* **Dynamic Model Selection:**
  * Lists and allows selection from available Gemini models for content generation.
  * Sorts models by relevance (prioritizing "latest", "pro", "flash").
  * Remembers and suggests the last used model.
* **Conversation History:**
  * Option to load previous chat history for a specific model.
  * Option to save the current chat session upon exiting.
  * Histories are saved in separate `.json` files per model.
* **Customization:**
  * Saves preferences for the last used model.
  * Use of ANSI colors for better readability in the terminal.
* **Packaged and Ready to Use:** Configured with `setup.py` and `pyproject.toml` for easy installation and use of the `pygemai` command.

## Prerequisites

* Python 3.8 or higher.
* `pip` (the Python package manager).
* A valid Google Gemini API Key (you can get one at Google AI Studio).

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/pygemai/PyGemAi.git 
    cd PyGemAi
    ```

2. **Create and Activate a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv .venv
    ```

    Activation (examples):
    * Linux/macOS (bash/zsh): `source .venv/bin/activate`
    * Linux/macOS (fish): `source .venv/bin/activate.fish`
    * Windows (cmd): `.venv\Scripts\activate.bat`
    * Windows (PowerShell): `.venv\Scripts\Activate.ps1`

3. **Install PyGemAi and its Dependencies:**
    From the project's root directory (where `setup.py` is located), run:

    ```bash
    pip install -e .
    ```

    This will install the `PyGemAi` package in editable mode, and the `pygemai` command will be available as long as your virtual environment is activated. The main dependencies are `google-generativeai` and `cryptography`.

## API Key Configuration

When running `pygemai` for the first time, or if no API key is detected, you will be guided to configure it. You have several options:

* Use the `GOOGLE_API_KEY` environment variable.
* Enter it manually and choose to save it encrypted (recommended), unencrypted, or not save it.

For more details on API key configuration and management, refer to the detailed User Guide (`GUIDE_OF_USE.md`).

## Basic Usage

Once installed and the API key is configured:

1. **Run the Chatbot:**
    Open your terminal (with the virtual environment activated) and type:

    ```bash
    pygemai
    ```

2. **Select a Model:** Follow the on-screen instructions to choose an AI model.
3. **Chat:** Type your messages and press Enter.
4. **Exit the Chat:** Type `salir`, `exit`, `quit`, or press `Ctrl+C`.
5. **Save History:** You will be asked if you want to save the session history.

For a complete explanation of all features, command-line options (if any in the future), and troubleshooting, please refer to the **User Guide (`GUIDE_OF_USE.md`)**.

## Project Structure (for Developers)

This project uses an `src/` structure where the main `pygemai_cli` package contains the application logic (`main.py`).

## Contributions

Contributions are welcome. Please open an issue to discuss important changes or report bugs. If you wish to contribute code, consider forking the repository and submitting a pull request.

## License

This project is licensed under the terms of the **GNU General Public License v3.0 or later**.
See the LICENSE file for more details.

Copyright (C) <Julio César Martínez> <julioglez@gmail.com>

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

## Contact

Julio César Martínez - <julioglez@gmail.com>

---

Developed with ❤️ and Python.
