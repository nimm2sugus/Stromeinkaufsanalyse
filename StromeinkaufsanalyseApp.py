import streamlit as st
import pandas as pd
import plotly.express as px

def load_excel_file(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
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
        st.subheader("Originaldaten")
        df['Beendet'] = pd.to_datetime(df['Beendet'], errors='coerce')
        df['Verbrauch_kWh'] = pd.to_numeric(df['Verbrauch (kWh)'], errors='coerce')

        df['Monat'] = df['Beendet'].dt.month
        df['Tag'] = df['Beendet'].dt.day
        df['Stunde'] = df['Beendet'].dt.hour

        st.write(df)
