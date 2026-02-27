import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analizador Multi-Año", layout="wide")

def main():
    st.title("📊 Control de Inasistencias Histórico")
    st.write("Análisis comparativo por años y totales acumulados.")

    url_input = st.text_input("Pega el enlace de tu Google Sheet:")

    if url_input:
        try:
            # 1. CARGA DE DATOS
            base_url = url_input.split('/edit')[0]
            csv_url = f"{base_url}/export?format=csv"
            df = pd.read_csv(csv_url)
            
            # 2. CONFIGURACIÓN DE COLUMNAS (Barra lateral)
            st.sidebar.header("Configuración")
            todas = df.columns.tolist()
            
            col_nombre = st.sidebar.selectbox("Nombres:", todas)
            col_apellido = st.sidebar.selectbox("Apellidos:", todas)
            col_grado = st.sidebar.selectbox("Grado:", todas)
            col_fecha = st.sidebar.selectbox("Columna de Fecha:", todas)

            # 3. PROCESAMIENTO INTELIGENTE
            # Convertimos la fecha a formato real y extraemos el AÑO
            df[col_fecha] = pd.to_datetime(df[col_fecha], errors='coerce')
            df['Año'] = df[col_fecha].dt.year.fillna('Sin Fecha')
            
            # Creamos el nombre del alumno
            df['Alumno'] = df[col_nombre].astype(str) + " " + df[col_apellido].astype(str)

            # CREAMOS LA TABLA COMPARATIVA (Pivote)
            # Esto pone los años como columnas y cuenta las inasistencias
            tabla_años = pd.crosstab(
                index=[df['Alumno'], df[col_grado]], 
                columns=df['Año']
            ).reset_index()

            # CALCULAMOS EL TOTAL DE TODOS LOS PERIODOS
            columnas_años = [c for c in tabla_años.columns if c not in ['Alumno', col_grado]]
            tabla_años['TOTAL ACUMULADO'] = tabla_años[columnas_años].sum(axis=1)

            # Ordenamos por el que tiene más inasistencias totales
            tabla_años = tabla_años.sort_values(by='TOTAL ACUMULADO', ascending=False)

            # 4. MOSTRAR RESULTADOS
            st.header("🔍 Resumen por Periodos")
            
            # Métricas generales
            c1, c2, c3 = st.columns(3)
            c1.metric("Alumnos Totales", len(tabla_años))
            c2.metric("Años Detectados", len(columnas_años))
            c3.metric("Total Inasistencias", tabla_años['TOTAL ACUMULADO'].sum())

            # Tabla dinámica
            st.subheader("Inasistencias por Año y Total")
            st.dataframe(tabla_años, use_container_width=True)

            # Gráfico comparativo (Top 10 alumnos)
            st.subheader("Top 10 Alumnos (Histórico)")
            st.bar_chart(data=tabla_años.head(10), x='Alumno', y='TOTAL ACUMULADO')

        except Exception as e:
            st.error("Error al procesar los años. Revisa que la columna de fecha sea correcta.")
            st.info(f"Detalle: {e}")
    else:
        st.info("Pega el link para ver el análisis histórico.")

if __name__ == "__main__":
    main()
