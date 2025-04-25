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
            # Neue Figure erstellen
            fig_combined = go.Figure()

            # Linie für "Verbrauch normiert" - Farbe auf Rot setzen
            fig_combined.add_trace(go.Scatter(
                x=df['Beendet'], 
                y=df['Verbrauch normiert'], 
                mode='lines+markers', 
                name='Verbrauch normiert', 
                line=dict(color='red')
            ))

            # Linie für "Day Ahead Marktpreis normiert" - Farbe auf Blau setzen
            fig_combined.add_trace(go.Scatter(
                x=df['Zeitstempel Day Ahead Marktpreis'], 
                y=df['Day Ahead Marktpreis normiert'], 
                mode='lines+markers', 
                name='Day Ahead Marktpreis normiert', 
                line=dict(color='blue')
            ))

            # Titel und Layout anpassen
            fig_combined.update_layout(
                title="Normierte Verläufe",
                xaxis_title="Zeit",
                yaxis_title="Wert",
                showlegend=True
            )

            # Zeigen des kombinierten Diagramms in Streamlit
            st.plotly_chart(fig_combined, use_container_width=True)
        else:
            st.warning("Nicht alle nötigen Spalten sind in der Excel-Datei enthalten.")
    else:
        st.warning("Dies ist ein komisches Format für den Upload :/")
