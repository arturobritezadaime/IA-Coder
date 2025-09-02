import os
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from google.generativeai import GenerativeModel, configure
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from newsapi import NewsApiClient
from utils import guardar_conversacion
from config import Config

# Configura la consola
console = Console()

def obtener_noticias_newsapi(empresa: str, newsapi_key: str):
    """
    Obtiene las 5 noticias principales de una empresa desde NewsAPI.
    
    Args:
        empresa (str): El nombre de la empresa a buscar.
        newsapi_key (str): La clave de API de NewsAPI.
        
    Returns:
        list: Una lista de títulos y descripciones de noticias.
    """
    console.print(f"Buscando 5 noticias de NewsAPI para: [bold]{empresa}[/bold]...")
    noticias = []
    newsapi = NewsApiClient(api_key=newsapi_key)
    try:
        top_headlines = newsapi.get_top_headlines(q=empresa, language='en', page_size=5)
        articles = top_headlines.get('articles', [])
        noticias.extend([f"{articulo.get('title', '')} {articulo.get('description', '')}" for articulo in articles if articulo.get('title') and articulo.get('description')])
    except Exception as e:
        console.print(f"[red]Error al obtener noticias de NewsAPI: {e}[/red]")
    return noticias

def obtener_noticias_gnews(empresa: str, gnews_api_key: str):
    """
    Obtiene las 5 noticias principales de una empresa desde GNews.
    
    Args:
        empresa (str): El nombre de la empresa a buscar.
        gnews_api_key (str): La clave de API de GNews.
        
    Returns:
        list: Una lista de títulos y descripciones de noticias.
    """
    console.print(f"Buscando 5 noticias de GNews para: [bold]{empresa}[/bold]...")
    noticias = []
    try:
        url_gnews = f'https://gnews.io/api/v4/search?q={empresa}&lang=en&token={gnews_api_key}&max=5'
        response = requests.get(url_gnews)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            noticias.extend([f"{articulo.get('title', '')} {articulo.get('description', '')}" for articulo in articles if articulo.get('title') and articulo.get('description')])
        elif response.status_code == 401:
            console.print("[red]Error 401: Clave de API de GNews no válida. Revisa tu archivo .env.[/red]")
        else:
            console.print(f"[red]Error en la API de GNews: Código {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Error al obtener noticias de GNews: {e}[/red]")
    return noticias

def analizar_sentimiento(empresa: str, gemini_api_key: str):
    """Función principal para el análisis de sentimiento."""
    try:
        if not gemini_api_key or not Config.NEWSAPI_API_KEY or not Config.GNEWS_API_KEY:
            raise ValueError("Las claves de API no se proporcionaron. Revisa tu archivo de configuración.")

        # Configura el modelo de Gemini con la clave de API
        configure(api_key=gemini_api_key)

        noticias_newsapi = obtener_noticias_newsapi(empresa, Config.NEWSAPI_API_KEY)
        noticias_gnews = obtener_noticias_gnews(empresa, Config.GNEWS_API_KEY)

        noticias = noticias_newsapi + noticias_gnews
        
        if not noticias:
            console.print("[red]No se encontraron noticias para la empresa especificada.[/red]")
            return

        noticias_str = "\n".join(noticias)
        prompt = f"""Analiza el sentimiento de las siguientes noticias sobre la empresa {empresa}.
        Identifica el sentimiento predominante (positivo, negativo, neutral) y explica brevemente por qué.
        Menciona cualquier riesgo o oportunidad potencial que puedas inferir del sentimiento de las noticias.
        Noticias:
        {noticias_str}
        """

        model = GenerativeModel("gemini-1.5-flash-latest")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("[cyan]Analizando sentimiento con Gemini...", total=1)
            response = model.generate_content(
                prompt,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                }
            )

        console.print("\n[bold]--- ANÁLISIS DE SENTIMIENTO ---[/bold]")
        console.print(response.text)

        guardar_conversacion(f"Análisis Sentimiento {empresa}", prompt, response.text)

    except Exception as e:
        console.print(f"[bold red]Ocurrió un error:[/bold red] {e}")

# Esto permite que el archivo se ejecute por sí mismo
if __name__ == "__main__":
    if not Config.GEMINI_API_KEY or not Config.NEWSAPI_API_KEY or not Config.GNEWS_API_KEY:
        console.print("[bold red]ERROR: No se encontraron las claves de API necesarias en config.py.[/bold red]")
        console.print("Asegúrate de que tu archivo .env existe y contiene las claves correctas.")
    else:
        empresa = console.input("Ingresa el nombre de la empresa (ej. Apple, Microsoft): ")
        analizar_sentimiento(
            empresa,
            gemini_api_key=Config.GEMINI_API_KEY
        )