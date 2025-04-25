import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_excel_file(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden der Datei: {e}")
        return None

st.set_page_config(page_title="Stromeinkaufsanalyse", layout="wide")
st.title("💶 Stromeinkaufsanalyse")

uploaded_file = st.file_uploader("📁 Bereinigte Excel-Datei hochladen", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = load_excel_file(uploaded_file)

    if df is not None:
        st.write(df)

        # Verbrauch im Zeitverlauf (alle Einzelvorgänge)
        st.subheader("Normierte Verläufe")

        # Prüfen, ob die nötigen Spalten existieren
        required_cols = ["Beendet", "Verbrauch normiert", "Zeitstempel Day Ahead Marktpreis", "Day Ahead Marktpreis normiert"]
        if all(col in df.columns for col in required_cols):
            # Erstellen der beiden Line-Plots
            fig_line_verbrauch = px.line(df, x="Beendet", y="Verbrauch normiert", title="Verbrauch normiert", markers=True)
            fig_line_marktpreis = px.line(df, x="Zeitstempel Day Ahead Marktpreis", y="Day Ahead Marktpreis normiert", title="Day Ahead Marktpreis normiert", markers=True)

            # Neue Figure erstellen und Traces aus beiden px-Figuren übernehmen
            fig_combined = go.Figure()

            # Linie für Verbrauch normiert - Farbe auf Rot setzen
            for trace in fig_line_verbrauch.data:
                fig_combined.add_trace(trace)
                fig_combined.update_traces(line=dict(color='red'), selector=dict(name='Verbrauch normiert'))

            # Linie für Marktpreis normiert - Farbe auf Blau setzen
            for trace in fig_line_marktpreis.data:
                fig_combined.add_trace(trace)
                fig_combined.update_traces(line=dict(color='blue'), selector=dict(name='Day Ahead Marktpreis normiert'))

            # Zeigen des kombinierten Diagramms in Streamlit
            st.plotly_chart(fig_combined, use_container_width=True)
        else:
            st.warning("Nicht alle nötigen Spalten sind in der Excel-Datei enthalten.")
    else:
        st.warning("Dies ist ein komisches Format für den Upload :/")
