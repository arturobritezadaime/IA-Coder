# 🤖 IA-Coder  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)  
![AI](https://img.shields.io/badge/AI-Enabled-green?logo=openai&logoColor=white)  
![License](https://img.shields.io/badge/License-MIT-lightgrey)  

> 💡 **IA-Coder** es un toolkit modular en Python que combina **análisis financiero**, **procesamiento de lenguaje natural**, **indicadores macroeconómicos** y **generación de imágenes con IA** en un solo entorno.  

---

## 📑 Índice  

- [✨ Descripción](#-descripción)  
- [🛠️ Funcionalidades](#️-funcionalidades)  
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)  
- [⚙️ Requisitos](#️-requisitos)  
- [📥 Instalación](#-instalación)  
- [🔧 Configuración](#-configuración)  
- [🚀 Uso](#-uso)  
- [🤝 Contribución](#-contribución)  
- [📜 Licencia](#-licencia)  
- [📬 Contacto](#-contacto)  

---

## ✨ Descripción  

IA-Coder es una herramienta diseñada para analistas, desarrolladores y entusiastas de la **Inteligencia Artificial aplicada a datos financieros y económicos**.  
Permite automatizar análisis fundamentales, evaluar sentimiento en textos, revisar indicadores macroeconómicos y generar imágenes mediante APIs de IA.  

⚡ **Objetivo**: ofrecer un entorno flexible, extensible y moderno para tareas de **Data Science + IA + Finanzas**.  

---

## 🛠️ Funcionalidades  

✅ **Análisis Fundamental** → extracción de datos financieros clave.  
✅ **Análisis de Sentimiento** → evaluación de polaridad en textos.  
✅ **Indicadores Macroeconómicos** → tendencias e impacto económico.  
✅ **Generación de Imágenes IA** → integración con Freepik AI.  
✅ **Cálculo de Tokens** → estimación de costos en modelos de IA.  
✅ **Integración con Gemini AI** → conexión sencilla con modelos de Google.  
✅ **Yahoo Finance API** → acceso a datos financieros globales.  

---

## 📂 Estructura del Proyecto  

```
IA-Coder/
├── config.py                  # Configuración global (API Keys, parámetros)
├── gemini_ai.py               # Conexión con Gemini AI
├── main.py                    # Punto de entrada principal
├── news_data.py               # Manejo de noticias
├── opcion1_fundamental.py     # Análisis fundamental
├── opcion2_sentimiento.py     # Análisis de sentimiento
├── opcion3_macro.py           # Indicadores macroeconómicos
├── opcion4_imagen_FreepikAI.py# Generación de imágenes IA
├── opcion5_costo_tokens.py    # Cálculo de costos en tokens
├── utils.py                   # Funciones auxiliares
├── yahoo_data.py              # Extracción de datos de Yahoo Finance
└── .gitignore
```

---

## ⚙️ Requisitos  

- 🐍 **Python 3.8+**  
- Librerías recomendadas:  
  - `requests`  
  - `pandas`  
  - `yfinance`  
  - `Pillow`  
  - `openai`  

---

## 📥 Instalación  

```bash
# Clona el repositorio
git clone https://github.com/arturobritezadaime/IA-Coder.git
cd IA-Coder

# Crea y activa entorno virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instala dependencias
pip install -r requirements.txt
```

---

## 🔧 Configuración  

En `config.py` agrega tus credenciales de APIs:  

```python
API_KEY_GEMINI = "tu_api_key_gemini"
API_KEY_FREEPIK = "tu_api_key_freepik"
API_URL_YAHOO = "https://..."
```

---

## 🚀 Uso  

Ejecuta el script principal:  

```bash
python main.py
```

👨‍💻 Menú de opciones:  

```
1) Análisis Fundamental
2) Análisis de Sentimiento
3) Indicadores Macroeconómicos
4) Generar Imagen con Freepik AI
5) Calcular Costo de Tokens
6) Salir
```

Ejemplo: selecciona la opción **2** para analizar un texto y obtener su **sentimiento**.

---

## 🤝 Contribución  

¡Las contribuciones son bienvenidas! 🙌  

1. Haz un fork del proyecto.  
2. Crea una rama: `git checkout -b feature-nueva`.  
3. Realiza tus cambios y haz commit: `git commit -m "Agrega nueva funcionalidad"`.  
4. Haz push a tu rama: `git push origin feature-nueva`.  
5. Abre un Pull Request.  

---

## 📜 Licencia  

Este proyecto se distribuye bajo la licencia **MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.  

---

## 📬 Contacto  

📌 Autor: **Arturo Britez Adaime**  
🌍 Repositorio: [IA-Coder](https://github.com/arturobritezadaime/IA-Coder)  

---

💡 *Hecho con pasión por con ayuda de la IA y el análisis de datos.* 🚀  
