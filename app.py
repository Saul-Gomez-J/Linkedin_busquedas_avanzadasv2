import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_linkedin_search_query(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """Eres un generador de URLs de búsqueda avanzada de Google para encontrar perfiles en LinkedIn. Tu objetivo es ayudar al usuario a construir URLs específicas para búsquedas de LinkedIn según sus descripciones en lenguaje natural. Cuando el usuario te proporcione una consulta, debes crear una URL que incluya todos los parámetros de búsqueda mencionados.

            Ejemplo de entradas y salidas:

            1. Entrada: "Quiero encontrar desarrolladores de software en Estados Unidos que hayan estudiado en MIT o Stanford."
            output: site:linkedin.com/in/ "Software Developer" "United States" ("MIT" OR "Stanford")

            2. Entrada: "Busco perfiles en LinkedIn de personas que trabajen en ventas y estén ubicadas en Europa."
            output: site:linkedin.com/in/ "sales" ("France" OR "Germany" OR "Spain" OR "Italy" OR "United Kingdom" OR "Netherlands")

            3. Entrada: "Me gustaría ver perfiles de gerentes de producto con experiencia en la industria tecnológica en California."
            output: site:linkedin.com/in/ "Product Manager" "technology industry" "California"

            4. Entrada: "Encuentra perfiles de ingenieros de datos en Canadá que tengan experiencia con Hadoop y Spark."
            output: site:linkedin.com/in/ "Data Engineer" "Canada" ("Hadoop" OR "Spark")

            5. Entrada: "Quiero ver perfiles de personas que hayan trabajado como científicos de datos en Europa y hayan estudiado inteligencia artificial."
            output: site:linkedin.com/in/ "Data Scientist" ("France" OR "Germany" OR "Spain" OR "Italy" OR "United Kingdom") "Artificial Intelligence"

            Recuerda utilizar `site:linkedin.com/in/` al inicio de cada consulta para limitar la búsqueda a perfiles de LinkedIn y utilizar operadores como `OR` para agrupar términos similares. También, agrupa términos dentro de comillas para realizar búsquedas exactas.
            """},
            {"role": "user", "content": f"Genera una consulta de búsqueda avanzada de LinkedIn para: {prompt}"}
        ],
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def build_google_search_url(search_query):
    base_url = "https://www.google.com/search?q="
    # Reemplazar espacios por '+', comillas por '%22' y paréntesis por sus códigos URL
    encoded_query = search_query.replace(' ', '+').replace('"', '%22').replace('(', '%28').replace(')', '%29')
    return f"{base_url}{encoded_query}"

def main():
    st.set_page_config(page_title="Generador de Búsqueda Avanzada de LinkedIn", page_icon="🔍")
    st.title("🔍 Generador de Búsqueda Avanzada de LinkedIn")

    st.write("""
    Introduce tu búsqueda en lenguaje natural y genera un enlace que te llevará a los resultados de búsqueda avanzada de LinkedIn en Google.
    
    **Ejemplos de búsquedas que puedes realizar:**
    - "Encuentra desarrolladores de software en Estados Unidos que hayan estudiado en MIT o Stanford"
    - "Busca perfiles de gerentes de ventas en Europa con experiencia en tecnología"
    - "Quiero ver perfiles de científicos de datos en Canadá con experiencia en inteligencia artificial"
    """)

    user_query = st.text_area("Introduce tu búsqueda:", height=150)

    if st.button("Generar Enlace de Búsqueda"):
        if user_query.strip():
            with st.spinner('Generando consulta de búsqueda avanzada...'):
                try:
                    search_query = generate_linkedin_search_query(user_query)
                    st.success("Consulta de búsqueda generada exitosamente.")
                    st.info(f"**Consulta Generada:** {search_query}")
                except Exception as e:
                    st.error(f"Error al generar la consulta: {e}")
                    return

            with st.spinner('Construyendo el enlace de búsqueda...'):
                try:
                    search_url = build_google_search_url(search_query)
                    st.success("Enlace de búsqueda construido exitosamente.")
                    st.markdown(f"[🔗 Haz clic aquí para ver los resultados de búsqueda en Google]({search_url})")
                except Exception as e:
                    st.error(f"Error al construir el enlace: {e}")
        else:
            st.error("Por favor, introduce una consulta de búsqueda válida.")

if __name__ == "__main__":
    main()
