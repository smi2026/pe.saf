import streamlit as st
import pandas as pd

# CONFIGURACIÓN VISUAL
st.set_page_config(page_title="Analizador Inteligente", layout="wide")

def main():
    st.title("📊 Analizador de Datos con Inteligencia")
    st.write("Conectado a tu Google Sheet para darte respuestas rápidas.")

    # ENTRADA DEL ENLACE
    url_input = st.text_input("Pega el enlace de tu Google Sheet aquí:")

    if url_input:
        try:
            # LIMPIEZA DEL ENLACE
            base_url = url_input.split('/edit')[0]
            csv_url = f"{base_url}/export?format=csv"
            
            df = pd.read_csv(csv_url)
            st.success("¡Datos actualizados!")

            # --- SECCIÓN DE RESUMEN INTELIGENTE ---
            st.subheader("💡 Resumen Automático")
            
            # Buscamos solo las columnas que tienen números
            columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
            
            if columnas_numericas:
                col_analizar = st.selectbox("¿Qué columna quieres que analice?", columnas_numericas)
                
                # Hacemos los cálculos
                total = df[col_analizar].sum()
                promedio = df[col_analizar].mean()
                maximo = df[col_analizar].max()

                # Mostramos los resultados en 3 tarjetas bonitas
                c1, c2, c3 = st.columns(3)
                c1.metric("Suma Total", f"{total:,.2f}") # AQUÍ SE MUESTRA EL TOTAL
                c2.metric("Promedio", f"{promedio:,.2f}") # AQUÍ SE MUESTRA EL PROMEDIO
                c3.metric("Valor Más Alto", f"{maximo:,.2f}") # AQUÍ SE MUESTRA EL MÁXIMO
            else:
                st.warning("No encontré columnas con números para analizar.")

            # --- SECCIÓN DE GRÁFICO ---
            st.divider()
            st.subheader("📈 Visualización")
            
            columnas_todas = df.columns.tolist()
            col_x, col_y = st.columns(2)
            
            with col_x:
                eje_x = st.selectbox("Eje X (Nombres):", columnas_todas, key="x")
            with col_y:
                eje_y = st.selectbox("Eje Y (Valores):", columnas_todas, key="y")

            st.bar_chart(data=df, x=eje_x, y=eje_y)

        except Exception as e:
            st.error("Error al leer los datos. Revisa el enlace.")
            st.info(f"Detalle: {e}")
    else:
        st.info("Pega un link para empezar.")

if __name__ == "__main__":
    main()
