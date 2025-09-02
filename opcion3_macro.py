import pandas as pd
import pandas_datareader.data as web
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from google.generativeai import GenerativeModel, configure
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from utils import guardar_conversacion
from config import Config

# Configura la consola
console = Console()

def get_fred_data(start_date, end_date, fred_api_key):
    """Descarga datos macroeconómicos desde la API de FRED."""
    indicators = {
        'CPIAUCSL': 'inflacion',  # Consumer Price Index
        'FEDFUNDS': 'tasa_fed',   # Federal Funds Rate
        'NASDAQCOM': 'retorno_nasdaq', # NASDAQ Composite Index
        'VIXCLS': 'vix', # CBOE Volatility Index
        'UMCSENT': 'sentimiento_consumidor' # University of Michigan Consumer Sentiment
    }
    
    data_df = pd.DataFrame()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Descargando datos de FRED...", total=len(indicators))
        for symbol, name in indicators.items():
            try:
                temp_df = web.DataReader(symbol, 'fred', start_date, end_date, api_key=fred_api_key)
                temp_df.columns = [name]
                if data_df.empty:
                    data_df = temp_df
                else:
                    data_df = data_df.join(temp_df, how='outer')
            except Exception as e:
                console.print(f"[red]Error al descargar {symbol}: {e}[/red]")
            progress.update(task, advance=1)
    
    return data_df.ffill().bfill() # Rellenar valores nulos

def build_prompt(yearly_averages: dict) -> str:
    """Construye el prompt basado en promedios anuales."""
    indicators = {
        "inflacion": "Inflación",
        "tasa_fed": "Tasa Fed",
        "retorno_nasdaq": "Retorno Nasdaq (12 meses)",
        "vix": "VIX (Índice de Volatilidad)",
        "sentimiento_consumidor": "Sentimiento del Consumidor (UMich)",
    }
    
    metrics_str = "=== DATOS PROMEDIO ANUALES (últimos 5 años) ===\n"
    for year, data in yearly_averages.items():
        metrics_str += f"\n--- {year} ---\n"
        for key, name in indicators.items():
            value = data.get(key)
            if value is not None:
                suffix = "%" if key not in ["vix", "sentimiento_consumidor"] else ""
                metrics_str += f"{name}: {value:.2f}{suffix}\n"

    prompt = f"""
Actúa como un economista senior en mercados financieros y genera un análisis basado SÓLO en los datos promedio anuales proporcionados.
    
**Análisis de Tendencias Anuales:**
Analiza la evolución de los indicadores macroeconómicos y su relación.
    
**Contexto y Futuro:**
Basándote en las tendencias observadas y el contexto actual, proporciona una perspectiva sobre la dirección probable del mercado y riesgos principales.
    
**Pronóstico:**
* **Pronóstico {datetime.now().year}:** Situación actual.
* **Pronóstico {datetime.now().year + 1}:** Perspectiva de mediano plazo.
    
---
Datos de la FED y Mercados:
""" + metrics_str
    
    return prompt

def analizar_macro(fred_api_key: str, gemini_api_key: str):
    """Función principal para el análisis macroeconómico."""
    try:
        if not fred_api_key or not gemini_api_key:
            raise ValueError("Las claves de API para FRED o Gemini no se proporcionaron.")
            
        configure(api_key=gemini_api_key)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5 * 365) # Últimos 5 años
        
        df = get_fred_data(start_date, end_date, fred_api_key)
        
        # Calcular promedios anuales
        yearly_averages = df.resample('YE').mean().to_dict('index')
        
        # Formatear el diccionario para el prompt
        formatted_yearly_averages = {year.year: values for year, values in yearly_averages.items()}
        
        prompt = build_prompt(formatted_yearly_averages)
        
        model = GenerativeModel("gemini-1.5-flash")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("[cyan]Generando análisis con Gemini...", total=1)
            response = model.generate_content(
                prompt,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
        
        console.print("\n[bold]--- ANÁLISIS MACROECONÓMICO ---[/bold]")
        console.print(response.text)
        
        guardar_conversacion("Análisis Macroeconómico", prompt, response.text)
        
    except Exception as e:
        console.print(f"[bold red]Ocurrió un error:[/bold red] {e}")

# Esto permite que el archivo se ejecute por sí mismo
if __name__ == "__main__":
    if not Config.FRED_API_KEY or not Config.GEMINI_API_KEY:
        console.print("[bold red]ERROR: No se encontraron las claves de API necesarias en config.py.[/bold red]")
        console.print("Asegúrate de que tu archivo .env existe y contiene las claves 'FRED_API_KEY' y 'GEMINI_API_KEY'.")
    else:
        analizar_macro(
            fred_api_key=Config.FRED_API_KEY,
            gemini_api_key=Config.GEMINI_API_KEY
        )