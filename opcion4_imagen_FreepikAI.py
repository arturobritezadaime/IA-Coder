import requests
import json
from datetime import datetime
import os
from rich.console import Console

# Configura la consola para una visualización mejorada
console = Console()

def guardar_respuesta_txt(prompt, respuesta, filename):
    """Guarda el prompt y el valor base64 de la respuesta en un archivo .txt con el formato deseado."""
    try:
        # Asegurarse de que el valor base64 exista
        if "data" in respuesta and len(respuesta["data"]) > 0 and "base64" in respuesta["data"][0]:
            base64_value = respuesta["data"][0]["base64"]
            content_to_save = f'--- PROMPT ---\n{prompt}\n--- RESPUESTA ---\n"base64": "{base64_value}"'
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content_to_save)
            console.print(f"✅ Respuesta guardada en [bold green]{filename}[/bold green]")
        else:
            error_msg = "La respuesta de la API no contiene el valor base64 esperado."
            console.print(f"❌ [bold red]{error_msg}[/bold red]")
            guardar_log(error_msg)
    except Exception as e:
        guardar_log(f"Error al guardar respuesta: {e}")

def guardar_log(mensaje, filename="error_freepik.log"):
    """Guarda mensajes de error en un log con fecha y hora."""
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {mensaje}\n")
        console.print(f"⚠️ [bold yellow]Error registrado en {filename}[/bold yellow]")
    except Exception as e:
        console.print("❌ [bold red]Error crítico al guardar el log:[/bold red]", e)

def generar_imagen_freepik(prompt, freepik_api_key):
    """
    Realiza una solicitud a la API de Freepik para generar una imagen.
    
    Args:
        prompt (str): La descripción de la imagen a generar.
        freepik_api_key (str): La clave de la API de Freepik.
    """
    # Asegúrate de que el directorio 'outputs' exista
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # URL de la API de Freepik
    url = "https://api.freepik.com/v1/ai/text-to-image"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-freepik-api-key": freepik_api_key
    }

    # La solicitud de imagen
    data = {
        "prompt": prompt,
        "aspect_ratio": "widescreen_16_9"
    }

    # Genera el nombre del archivo con fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_opcion = 'Imagen_FreepikAI'
    nombre_archivo = f"outputs/{nombre_opcion}_{timestamp}.txt"
    
    console.print(f"\nGenerando imagen para el prompt: '[bold]{prompt}[/bold]'...")

    try:
        # Realizar la solicitud POST a la API de Freepik
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            respuesta_json = response.json()
            guardar_respuesta_txt(prompt, respuesta_json, nombre_archivo)
        else:
            error_msg = f"Error {response.status_code}: {response.text}"
            console.print(f"❌ [bold red]{error_msg}[/bold red]")
            guardar_log(error_msg)
    except requests.exceptions.RequestException as e:
        error_msg = f"Excepción en la solicitud: {e}"
        console.print(f"❌ [bold red]{error_msg}[/bold red]")
        guardar_log(error_msg)
