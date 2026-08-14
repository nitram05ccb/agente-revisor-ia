# 🤖 Agente Autónomo Revisor de Código

Este proyecto es un **Agente Autónomo** diseñado para integrarse en el flujo de CI/CD de un repositorio de GitHub. Actúa como un revisor de código experto, analizando automáticamente las Pull Requests en busca de vulnerabilidades de seguridad, problemas de rendimiento y malas prácticas, dejando comentarios detallados con sugerencias de refactorización.

El proyecto está diseñado para funcionar en un entorno local de Windows conectándose a modelos de lenguaje (LLMs) que se ejecutan localmente a través de LM Studio. Esta arquitectura permite testear y refinar el comportamiento del agente ("Prompt Engineering") sin incurrir en costes de API.

## 🚀 Arquitectura y Flujo de Trabajo

1.  **Extracción de Datos:** El agente se conecta a la API de GitHub (usando `PyGithub` y un Token de Acceso Personal) y descarga el *diff* exacto (las líneas modificadas) de una Pull Request específica.
2.  **Análisis (El Cerebro):** El *diff* extraído se envía al servidor local de LM Studio (simulando la API de OpenAI). Un *System Prompt* robusto instruye al modelo para que actúe como un desarrollador senior estricto.
3.  **Acción (Tool Calling):** El agente recibe el análisis estructurado del modelo y vuelve a llamar a la API de GitHub para publicar el resultado como un comentario directamente en el hilo de la Pull Request.

## 🛠️ Tecnologías Utilizadas

*   **Lenguaje:** Python 3
*   **Interacción con GitHub:** `PyGithub`
*   **LLM Hosting:** LM Studio (Local / Windows)
*   **Integración API:** `requests`
*   **Gestión de Entorno:** `python-dotenv`

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio y preparar el entorno (Windows)

```powershell
git clone https://github.com/tu_usuario/revisor-codigo-ia.git
cd revisor-codigo-ia

# Crear entorno virtual y activarlo
python -m venv env
.\env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

*(Nota: Si no tienes el archivo `requirements.txt`, las dependencias necesarias son `PyGithub`, `requests` y `python-dotenv`)*.

### 2. Configurar Variables de Entorno

Crea un archivo llamado `.env` en el directorio raíz del proyecto con el siguiente contenido:

```text
# URL de la API de tu modelo local en LM Studio
LLM_API_BASE=http://localhost:1234/v1/chat/completions

# Personal Access Token de GitHub (Necesita permisos 'repo' y 'pull-requests: write')
GITHUB_TOKEN=ghp_tu_token_aqui
```

### 3. Preparar LM Studio

1.  Abre LM Studio en tu equipo.
2.  Carga un modelo enfocado en programación (ej. Llama 3, Qwen Coder o DeepSeek Coder).
3.  Inicia el servidor local en la pestaña **Local Server** (puerto por defecto `1234`).

## 💻 Uso

1.  Abre el archivo principal (ej. `agente.py`).
2.  Configura las variables objetivo al final del script:
    ```python
    NOMBRE_REPO = "usuario/nombre-del-repositorio"
    NUMERO_PR = 1 # Número de la Pull Request a analizar
    ```
3.  Ejecuta el agente:
    ```powershell
    python agente.py
    ```

El script imprimirá el proceso en la terminal y, si tiene éxito, publicará el análisis directamente en la Pull Request de GitHub seleccionada.

## 🔮 Siguientes Pasos (Roadmap)

*   [ ] **Comentarios Inline:** Estructurar la salida del LLM en formato JSON para que el agente pueda comentar directamente en las líneas de código afectadas usando la API de GitHub de comentarios de revisión.
*   [ ] **Migración a la Nube:** Desplegar la lógica en Azure AI / GitHub Actions reales para que el proceso se ejecute de forma 100% autónoma ante el evento `on: pull_request` sin depender del equipo local.
*   [ ] **Memoria con RAG:** Integrar una base de datos vectorial para que el agente tenga contexto sobre revisiones pasadas y el estilo de código del proyecto.
