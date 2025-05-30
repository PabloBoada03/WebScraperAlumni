import streamlit as st
from scrape import scrape, extraer_body, limpiar_body, porcionador
from parse import parse

st.title("Alumni Web Scraper")
url = st.text_input("Ingrese una URL:")

if st.button("Scrape"):
    if not url:
        st.warning("Por favor ingrese una URL válida.")
    else:
        st.write("Scraping...")
        try:
            result = scrape(url)
            if not result:
                st.error("No se pudo obtener el contenido de la página.")
            else:
                body_content = extraer_body(result)
                cleaned_content = limpiar_body(body_content)

                st.session_state.dom_content = cleaned_content

                with st.expander("Ver contenido del DOM"):
                    st.text_area("Contenido del DOM", cleaned_content, height=300)
        except Exception as e:
            st.error(f"Ocurrió un error durante el scraping: {e}")

# Mostrar el área de parseo si hay contenido DOM
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe lo que quieres obtener")

    if st.button("Parse"):
        if not parse_description:
            st.warning("Por favor describe lo que quieres obtener.")
        else:
            st.write("Parsing...")
            try:
                dom_chunks = porcionador(st.session_state.dom_content)
                result = parse(dom_chunks, parse_description)
                st.success("Resultados del parseo:")
                st.write(result)
            except Exception as e:
                st.error(f"Error al parsear el contenido: {e}")
