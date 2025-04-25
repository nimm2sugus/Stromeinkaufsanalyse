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
    else:
        st.warning("Dies ist ein komisches Format für den Upload :/")

        # Verbrauch im Zeitverlauf (alle Einzelvorgänge)
        st.subheader("Normierte Verläufe")
        fig_line_verbrauch = px.line(df, x="Beendet", y="Verbrauch normiert", title="Verbrauch normiert", markers=True)
        fig_line_marktpreis = px.line(df, x="Zeitstempel Day Ahead Marktpreis", y="Day Ahead Marktpreis normiert", title="Day Ahead Marktpreis normiert", markers=True)

        # Neue Figure erstellen und Traces aus beiden px-Figuren übernehmen
        fig_combined = go.Figure()

        # Traces von fig1 und fig2 hinzufügen
        for trace in fig_line_verbrauch.data:
            fig_combined.add_trace(trace)
        for trace in fig_line_marktpreis.data:
            fig_combined.add_trace(trace)

        st.plotly_chart(fig_combined, use_container_width=True)
