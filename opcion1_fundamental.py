import os
import yfinance as yf
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from google.generativeai import GenerativeModel, configure
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from utils import guardar_conversacion
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

# Configura la consola
console = Console()

def obtener_datos_financieros(tickers):
    """Obtiene datos financieros de Yahoo Finance."""
    data = {}
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Descargando datos financieros...", total=len(tickers))
        for ticker in tickers:
            try:
                empresa = yf.Ticker(ticker)
                balance_sheet = empresa.balance_sheet
                income_statement = empresa.financials
                market_info = empresa.info

                # Extrae métricas clave
                current_ratio = balance_sheet.loc['Current Ratio'].iloc[0] if 'Current Ratio' in balance_sheet.index else "N/A"
                revenue = income_statement.loc['Total Revenue'].iloc[0] if 'Total Revenue' in income_statement.index else "N/A"
                roe = market_info.get('returnOnEquity', "N/A")

                data[ticker] = {
                    "Current Ratio": current_ratio,
                    "Revenue": revenue,
                    "ROE": roe
                }
            except Exception as e:
                console.print(f"[red]Error al obtener datos para {ticker}: {e}[/red]")
            progress.update(task, advance=1)
    return data

def analizar_inversion(gemini_api_key: str):
    """Función principal para el análisis de inversión."""
    try:
        if not gemini_api_key:
            raise ValueError("La clave de API de Gemini no se proporcionó.")
        
        # Configura el modelo de Gemini con la clave proporcionada
        configure(api_key=gemini_api_key)

        # Define los tickers de las empresas
        empresas = {
            "MSFT": "Microsoft",
            "AAPL": "Apple",
            "GOOG": "Google"
        }

        datos_financieros = obtener_datos_financieros(empresas.keys())
        
        # Construye el prompt con los datos obtenidos
        analysis_input = "\n".join(
            [f"--- {empresas[ticker]} ---\n{datos_financieros[ticker]}" for ticker in datos_financieros]
        )
        
        prompt = f"""Actúa como un analista financiero. Analiza los últimos informes anuales de Microsoft, Apple y Google. Compara sus indicadores de rentabilidad (ROE), liquidez (Current Ratio) y crecimiento de ingresos. También incluye percepción del mercado según noticias recientes. Datos disponibles: {analysis_input}. Genera un informe que destaque los puntos fuertes y débiles de cada una y un resumen de 300 palabras sobre cuál presenta una mejor oportunidad de inversión a largo plazo, justificando tu respuesta."""

        model = GenerativeModel("gemini-2.5-flash") # No se necesita api_key aquí si ya se usó `configure`
        
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
            
        console.print("\n[bold]--- INFORME DE ANÁLISIS FINANCIERO ---[/bold]")
        console.print(response.text)
        
        guardar_conversacion("Análisis Fundamental", prompt, response.text)

    except Exception as e:
        console.print(f"[bold red]Ocurrió un error:[/bold red] {e}")

# Esto permite que el archivo se ejecute por sí mismo
if __name__ == "__main__":
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    analizar_inversion(gemini_api_key)