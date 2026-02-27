import streamlit as st
import pandas as pd

# CONFIGURACIÓN
st.set_page_config(page_title="Control de Inasistencias", layout="wide")

def main():
    st.title("📋 Control de Inasistencias por Alumno")
    st.write("Análisis detallado de alumnos y grados.")

    url_input = st.text_input("Pega el enlace de tu Google Sheet:")

    if url_input:
        try:
            base_url = url_input.split('/edit')[0]
            csv_url = f"{base_url}/export?format=csv"
            
            # Cargamos los datos
            df = pd.read_csv(csv_url)
            st.success("¡Datos cargados!")

            # --- NUEVA SECCIÓN: ANÁLISIS POR ALUMNO ---
            st.header("🔍 Resumen de Inasistencias")
            
            # Limpiamos nombres para que no haya errores por espacios
            df['Nombre completo'] = df['Nombre'].astype(str) + " " + df['Apellido'].astype(str)
            
            # AGRUPAMOS: Contamos cuántas veces aparece cada alumno y guardamos su grado
            # Usamos 'first' para el grado porque asumimos que el alumno no cambia de grado
            resumen = df.groupby('Nombre completo').agg({
                'Grado': 'first',
                'Nombre completo': 'count'
            }).rename(columns={'Nombre completo': 'Total Inasistencias'}).reset_index()

            # Ordenamos de mayor a menor inasistencia
            resumen = resumen.sort_values(by='Total Inasistencias', ascending=False)

            # Mostramos la tabla resumen
            st.subheader("Listado de Inasistencias por Alumno")
            st.dataframe(resumen, use_container_width=True)

            # GRÁFICO DE LOS MÁS AUSENTES
            st.subheader("Gráfico: Alumnos con más notificaciones")
            # Mostramos los primeros 15 para que no se vea amontonado
            st.bar_chart(data=resumen.head(15), x='Nombre completo', y='Total Inasistencias')

            # --- SECCIÓN DE DATOS ORIGINALES ---
            with st.expander("Ver todos los datos originales"):
                st.write(df)

        except Exception as e:
            st.error("Error al procesar los datos.")
            st.info(f"Detalle técnico: {e}")
    else:
        st.info("Pega el link de tu hoja '2022' para empezar.")

if __name__ == "__main__":
    main()
