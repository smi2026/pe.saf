import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analizador Flexible", layout="wide")

def main():
    st.title("📋 Analizador de Inasistencias Personalizado")
    
    url_input = st.text_input("Pega el enlace de tu Google Sheet:")

    if url_input:
        try:
            # 1. LEER LOS DATOS
            base_url = url_input.split('/edit')[0]
            csv_url = f"{base_url}/export?format=csv"
            df = pd.read_csv(csv_url)
            
            st.success("¡Archivo leído con éxito!")
            
            # 2. SELECCIÓN DE COLUMNAS (Para evitar el error de 'no existe')
            st.sidebar.header("Configuración de Columnas")
            st.sidebar.write("Dime qué columna es cada una:")
            
            todas_las_columnas = df.columns.tolist()
            
            # El programa intenta adivinar, pero tú confirmas:
            col_nombre = st.sidebar.selectbox("Columna de NOMBRES:", todas_las_columnas)
            col_apellido = st.sidebar.selectbox("Columna de APELLIDOS:", todas_las_columnas)
            col_grado = st.sidebar.selectbox("Columna de GRADO/AÑO:", todas_las_columnas)

            # 3. PROCESAMIENTO
            # Creamos el nombre completo uniendo las dos columnas elegidas
            df['Alumno'] = df[col_nombre].astype(str) + " " + df[col_apellido].astype(str)
            
            # Agrupamos usando las columnas que TÚ elegiste arriba
            resumen = df.groupby('Alumno').agg({
                col_grado: 'first',
                'Alumno': 'count'
            }).rename(columns={'Alumno': 'Total Inasistencias', col_grado: 'Grado'}).reset_index()

            resumen = resumen.sort_values(by='Total Inasistencias', ascending=False)

            # 4. MOSTRAR RESULTADOS
            st.header("🔍 Resultados del Análisis")
            
            # Tarjetas con datos rápidos
            c1, c2 = st.columns(2)
            c1.metric("Total de Alumnos analizados", len(resumen))
            c2.metric("Total de Inasistencias", resumen['Total Inasistencias'].sum())

            # Tabla y Gráfico
            st.subheader("Listado por Alumno y Grado")
            st.dataframe(resumen, use_container_width=True)

            st.subheader("Top 15 Alumnos con más inasistencias")
            st.bar_chart(data=resumen.head(15), x='Alumno', y='Total Inasistencias')

        except Exception as e:
            st.error("Hubo un problema al procesar los datos.")
            st.info(f"Asegúrate de seleccionar las columnas correctas en la barra lateral. Error: {e}")
    else:
        st.info("Por favor, pega el link de Google Sheets.")

if __name__ == "__main__":
    main()
