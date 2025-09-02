import google.generativeai as genai
from rich.console import Console
import os

console = Console()

def analizar_costo_tokens():
    """
    Lee un archivo de texto, calcula los tokens de entrada y salida,
    y estima el costo total basado en los precios de Gemini 2.5 Flash.
    """
    try:
        # 1. Solicitar el nombre del archivo al usuario
        nombre_archivo = console.input("[bold yellow]Ingrese el nombre del archivo .txt a analizar:[/bold yellow] ")

        # 2. Intentar leer desde 'outputs', si no existe usar carpeta actual
        if os.path.exists(os.path.join("outputs", nombre_archivo)):
            file_path = os.path.join("outputs", nombre_archivo)
        else:
            file_path = nombre_archivo  # busca en la raíz

        with open(file_path, "r", encoding="utf-8") as f:
            contenido = f.read()

        # 3. Separar el prompt de entrada y la respuesta de salida
        if "--- RESPUESTA DE GEMINI ---" in contenido:
            partes = contenido.split("--- RESPUESTA DE GEMINI ---")
        elif "--- RESPUESTA ---" in contenido:
            partes = contenido.split("--- RESPUESTA ---")
        else:
            console.print("❌ [bold red]El formato del archivo no es el esperado.[/bold red] "
                          "Debe contener '[bold yellow]--- RESPUESTA DE GEMINI ---[/bold yellow]' o "
                          "'[bold yellow]--- RESPUESTA ---[/bold yellow]'.")
            return

        if len(partes) != 2:
            console.print("❌ [bold red]El archivo no se pudo dividir en PROMPT y RESPUESTA.[/bold red]")
            return

        # 4. Limpiar el prompt y la respuesta
        prompt_enviado = partes[0].replace("--- PROMPT ---", "").strip()
        respuesta_gemini = partes[1].strip()

        # 5. Inicializar modelo para contar tokens
        modelo = genai.GenerativeModel("gemini-2.5-flash")

        tokens_entrada = modelo.count_tokens(prompt_enviado).total_tokens
        tokens_salida = modelo.count_tokens(respuesta_gemini).total_tokens

        # 6. Precios por millón de tokens
        PRECIO_ENTRADA_POR_MILLON = 0.30
        PRECIO_SALIDA_POR_MILLON = 2.50

        costo_entrada = (tokens_entrada / 1_000_000) * PRECIO_ENTRADA_POR_MILLON
        costo_salida = (tokens_salida / 1_000_000) * PRECIO_SALIDA_POR_MILLON
        costo_total = costo_entrada + costo_salida

        # 7. Mostrar resultados
        console.print(f"\n[bold cyan]--- RESUMEN DE COSTOS ({nombre_archivo}) ---[/bold cyan]")
        console.print(f"Tokens de entrada: [bold green]{tokens_entrada}[/bold green]")
        console.print(f"Tokens de salida: [bold green]{tokens_salida}[/bold green]")
        console.print(f"Costo de entrada: [bold yellow]${costo_entrada:.6f} USD[/bold yellow]")
        console.print(f"Costo de salida: [bold yellow]${costo_salida:.6f} USD[/bold yellow]")
        console.print(f"Costo total: [bold magenta]${costo_total:.6f} USD[/bold magenta]")

    except FileNotFoundError:
        console.print(f"❌ [bold red]Error: El archivo '{nombre_archivo}' no se encontró.[/bold red]")
    except Exception as e:
        console.print(f"❌ [bold red]Error inesperado:[/bold red] {e}")
