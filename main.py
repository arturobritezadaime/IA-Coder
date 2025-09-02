import os
from rich.console import Console
from rich.table import Table

# Importa la clase de configuración
from config import Config

# Importa las funciones de cada módulo
from opcion1_fundamental import analizar_inversion
from opcion2_sentimiento import analizar_sentimiento
from opcion3_macro import analizar_macro
from opcion4_imagen_FreepikAI import generar_imagen_freepik

# Configura la consola para una visualización mejorada
console = Console()

def mostrar_menu():
    """Muestra el menú de opciones al usuario."""
    console.print("\n[bold cyan]Bienvenido al Asistente Unificado de IA[/bold cyan]")
    table = Table(title="Menú de Opciones")
    table.add_column("Opción", style="bold")
    table.add_column("Descripción")

    table.add_row("1", "Análisis Fundamental y Comparativo (Microsoft, Apple, Google)")
    table.add_row("2", "Análisis de Sentimiento de Noticias de Empresas Tecnológicas")
    table.add_row("3", "Análisis Macroeconómico y de Riesgos")
    table.add_row("4", "Generación Visual con IA ")
    table.add_row("0", "Salir")

    console.print(table)

def main():
    """Función principal que maneja el flujo del programa."""
    while True:
        mostrar_menu()
        eleccion = console.input("[bold yellow]Ingresa tu opción:[/bold yellow] ")

        if eleccion == '1':
            console.print("\n[bold green]Iniciando Análisis Fundamental...[/bold green]")
            # Pasa la clave de Gemini desde la clase Config
            analizar_inversion(gemini_api_key=Config.GEMINI_API_KEY)
        elif eleccion == '2':
            console.print("\n[bold green]Iniciando Análisis de Sentimiento...[/bold green]")
            empresa = console.input("Ingresa el nombre de la empresa tecnológica (ej. Apple, Microsoft): ")
            # Pasa las claves de Gemini y NewsAPI desde la clase Config
            analizar_sentimiento(
                empresa,
                gemini_api_key=Config.GEMINI_API_KEY,
                newsapi_key=Config.NEWSAPI_API_KEY
            )
        elif eleccion == '3':
            console.print("\n[bold green]Iniciando Análisis Macroeconómico...[/bold green]")
            analizar_macro(
                fred_api_key=Config.FRED_API_KEY,
                gemini_api_key=Config.GEMINI_API_KEY
            )
        elif eleccion == '4':
            console.print("\n[bold green]Iniciando Generación de Imágenes con Freepik AI...[/bold green]")
            prompt = console.input("Ingresa una descripción para la imagen: ")
            generar_imagen_freepik(
                prompt, 
                freepik_api_key=Config.FREEPIK_API_KEY
            )
        elif eleccion == '0':
            console.print("\n[bold magenta]¡Gracias por usar el asistente! Hasta luego.[/bold magenta]")
            break
        else:
            console.print("\n[bold red]Opción no válida. Por favor, elige una opción del menú.[/bold red]")

if __name__ == "__main__":
    main()