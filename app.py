import streamlit as st
from openai import OpenAI
import urllib.parse

# Configurar la página de Streamlit debe ser lo primero en el script.
st.set_page_config(page_title="Generador de Búsqueda Avanzada de LinkedIn", page_icon="🔍")

# Inicializar el cliente de OpenAI utilizando las variables de entorno de Streamlit
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Saira:wght@100;300;400;500;600;700&family=Ubuntu:wght@300;400;500;700&display=swap');

    /* Título del sitio */
    .css-18e3th9 {
        font-family: 'Saira', sans-serif;
        font-weight: 500; /* Medium */
        font-size: 30px;
    }

    /* Fuente del cuerpo */
    .css-1d391kg {
        font-family: 'Ubuntu', sans-serif;
        font-weight: 400; /* Regular */
        font-size: 16px;
    }

    /* Estilo para el botón personalizado */
    .custom-button {
        display: inline-block;
        padding: 12px 24px;
        font-size: 18px;
        color: white;
        background-color: #4CAF50;
        border: none;
        border-radius: 8px;
        text-align: center;
        text-decoration: none;
        font-family: 'Saira', sans-serif;
        font-weight: 500;
        cursor: pointer;
        margin: 20px 0;
    }

    .custom-button:hover {
        background-color: #45a049;
    }

    </style>
    """,
    unsafe_allow_html=True
)

def generate_linkedin_search_query(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """Eres un generador de URLs de búsqueda avanzada de Google para encontrar perfiles en LinkedIn. Tu objetivo es ayudar al usuario a construir URLs específicas para búsquedas de LinkedIn según sus descripciones en lenguaje natural. Cuando el usuario te proporcione una consulta, debes crear una URL que incluya todos los parámetros de búsqueda mencionados.

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
    # Utilizar urllib.parse para codificar correctamente la consulta
    encoded_query = urllib.parse.quote(search_query)
    return f"{base_url}{encoded_query}"

def main():
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
                except Exception as e:
                    st.error(f"Error al generar la consulta: {e}")
                    return

            with st.spinner('Construyendo el enlace de búsqueda...'):
                try:
                    search_url = build_google_search_url(search_query)
                    st.success("Enlace de búsqueda construido exitosamente.")
                    # Mostrar el botón con el enlace, sin mostrar la consulta generada
                    st.markdown(f'<a href="{search_url}" class="custom-button" target="_blank">🔍 Click aquí para ver el resultado de tu búsqueda</a>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error al construir el enlace: {e}")
        else:
            st.error("Por favor, introduce una consulta de búsqueda válida.")

if __name__ == "__main__":
    main()
