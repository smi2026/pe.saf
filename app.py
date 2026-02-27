import streamlit as st
import pandas as pd

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Analizador Cloud de Google Sheets", layout="wide")

def main():
    st.title("🚀 Mi Aplicación en la Nube")
    st.write("Esta app vive en internet y lee tus Google Sheets.")

    # ENTRADA DEL ENLACE
    url_input = st.text_input("Pega el enlace de tu Google Sheet (Debe estar compartido como 'Cualquier persona con el enlace'):")

    if url_input:
        try:
            # LIMPIEZA DEL ENLACE PARA QUE SEA LEGIBLE
            # AQUÍ ES DONDE SE TRANSFORMA EL LINK DE GOOGLE EN DATOS
            base_url = url_input.split('/edit')[0]
            csv_url = f"{base_url}/export?format=csv"
            
            df = pd.read_csv(csv_url)
            
            st.success("¡Datos cargados correctamente!")
            
            # MOSTRAR TABLA
            st.dataframe(df)

            # GRÁFICO INTERACTIVO
            columnas = df.columns.tolist()
            col1, col2 = st.columns(2)
            
            with col1:
                eje_x = st.selectbox("Eje horizontal (X):", columnas)
            with col2:
                eje_y = st.selectbox("Eje vertical / Valores (Y):", columnas)

            # BOTÓN PARA GENERAR
            if st.button("Actualizar Gráfico"):
                st.bar_chart(data=df, x=eje_x, y=eje_y)

        except Exception as e:
            st.error("Error: Asegúrate de que el enlace sea de Google Sheets y sea público.")
            st.info(f"Nota para el CTO: {e}")
    else:
        st.warning("Copia el link de tu hoja de Google y pégalo arriba.")

if __name__ == "__main__":
    main()
