import os
from datetime import datetime
from rich.console import Console

console = Console()

def guardar_conversacion(nombre_opcion: str, prompt: str, respuesta: str):
    """Guarda el prompt y la respuesta en un archivo de texto."""
    try:
        # Crea la carpeta 'outputs' si no existe
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
            
        # Genera el nombre del archivo con fecha y hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"outputs/{nombre_opcion}_{timestamp}.txt"
        
        # Escribe el contenido en el archivo
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("--- PROMPT ---\n")
            f.write(prompt)
            f.write("\n\n--- RESPUESTA DE GEMINI ---\n")
            f.write(respuesta)
            
        console.print(f"\n[green]Conversación guardada en:[/green] [bold]{nombre_archivo}[/bold]")

    except Exception as e:
        console.print(f"[red]Error al guardar la conversación: {e}[/red]")