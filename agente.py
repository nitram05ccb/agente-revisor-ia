import os
import requests
from dotenv import load_dotenv
from github import Github

# Cargar configuración desde el archivo .env
load_dotenv()
LM_STUDIO_URL = os.getenv("LLM_API_BASE", "http://localhost:1234/v1/chat/completions")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def revisar_codigo(diff_texto):
    """Envía el código al LLM local para su revisión."""
    payload = {
        "model": "local-model",
        "temperature": 0.2,
        "messages": [
            {
                "role": "system", 
                "content": "Eres un revisor de código experto y estricto. Analiza el código proporcionado. Si encuentras problemas de seguridad o malas prácticas, explícalas de forma concisa. Formatea tu respuesta usando Markdown para que se vea bien en GitHub."
            },
            {
                "role": "user", 
                "content": f"Por favor, revisa las siguientes líneas de código añadidas:\n\n{diff_texto}"
            }
        ]
    }

    try:
        respuesta = requests.post(LM_STUDIO_URL, json=payload)
        respuesta.raise_for_status()
        datos = respuesta.json()
        return datos["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error al conectar con el LLM: {e}"

def obtener_diff_pr(repo_nombre, pr_numero):
    """Conecta con GitHub y extrae el código modificado de una PR."""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_nombre)
    pr = repo.get_pull(pr_numero)
    
    diff_completo = ""
    for archivo in pr.get_files():
        diff_completo += f"--- Archivo modificado: {archivo.filename} ---\n"
        diff_completo += f"{archivo.patch}\n\n"
        
    return diff_completo

def publicar_comentario_pr(repo_nombre, pr_numero, comentario):
    """Publica el análisis del LLM como un comentario en la Pull Request."""
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(repo_nombre)
        # En la API de GitHub, los comentarios generales de una PR se tratan como comentarios de "Issue"
        issue = repo.get_issue(number=pr_numero) 
        
        # Formateamos un poco el mensaje para darle personalidad al bot
        mensaje_final = f"🤖 **Revisión Automática de IA (Local)**\n\n{comentario}\n\n*Nota: Análisis generado por el agente revisor de código.*"
        
        # Publicamos el comentario
        issue.create_comment(mensaje_final)
        print("✅ ¡Comentario publicado con éxito en GitHub!")
        return True
    except Exception as e:
        print(f"❌ Error al publicar en GitHub: {e}")
        return False

if __name__ == "__main__":
    # --- CONFIGURACIÓN ---
    # ¡Asegúrate de cambiar esto por tus datos reales!
    NOMBRE_REPO = "nitram05ccb/repo-pruebas" 
    NUMERO_PR = 1
    # ---------------------
    
    print("1. Conectando con GitHub para descargar el código...")
    try:
        diff_texto = obtener_diff_pr(NOMBRE_REPO, NUMERO_PR)
        
        if not diff_texto.strip():
            print("No se encontraron cambios en el código de esta PR.")
        else:
            print("2. Diff extraído correctamente. Analizando con LM Studio...\n")
            comentario_ia = revisar_codigo(diff_texto)
            
            print("3. Análisis completado. Publicando en la Pull Request...\n")
            publicar_comentario_pr(NOMBRE_REPO, NUMERO_PR, comentario_ia)
            
    except Exception as e:
        print(f"❌ Error general en la ejecución: {e}")