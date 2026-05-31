import streamlit as st
import pandas as pd
import time
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Clickstream Analytics",
    page_icon="🖱️",
    layout="wide"
)

st.title("🖱️ Clickstream Analytics — Temps réel")

engine = create_engine("postgresql://admin:admin123@localhost:5433/streaming_db")

def get_data():
    with engine.connect() as conn:
        # Tous les événements
        all_events = pd.read_sql(text("""
            SELECT timestamp, page, element, event_type
            FROM clicks ORDER BY timestamp DESC LIMIT 500
        """), conn)

        # Activité par minute (dernières 10 minutes)
        timeline = pd.read_sql(text("""
            SELECT
                date_trunc('minute', timestamp) AS minute,
                event_type,
                COUNT(*) AS total
            FROM clicks
            WHERE timestamp > NOW() - INTERVAL '10 minutes'
            GROUP BY minute, event_type
            ORDER BY minute
        """), conn)

        # Profondeur de scroll
        scroll_depth = pd.read_sql(text("""
            SELECT element, COUNT(*) as count
            FROM clicks
            WHERE event_type = 'scroll'
            GROUP BY element
            ORDER BY count DESC
            LIMIT 10
        """), conn)

    return all_events, timeline, scroll_depth

placeholder = st.empty()

while True:
    try:
        df, timeline, scroll_depth = get_data()

        with placeholder.container():

            # === KPIs principaux ===
            st.subheader("KPIs en direct")
            c1, c2, c3, c4, c5 = st.columns(5)

            total = len(df)
            clics = int((df["event_type"] == "click").sum())
            scrolls = int((df["event_type"] == "scroll").sum())
            pageviews = int((df["event_type"] == "pageview").sum())

            # Taux d'engagement : clics / pageviews
            engagement = round(clics / pageviews * 100, 1) if pageviews > 0 else 0

            c1.metric("Total événements", total)
            c2.metric("Clics", clics)
            c3.metric("Scrolls", scrolls)
            c4.metric("Pages vues", pageviews)
            c5.metric("Taux d'engagement", f"{engagement}%")

            st.divider()

            # === Ligne 1 : Timeline + Types ===
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("Activité par minute (10 dernières min)")
                if len(timeline) > 0:
                    pivot = timeline.pivot_table(
                        index="minute",
                        columns="event_type",
                        values="total",
                        fill_value=0
                    )
                    st.line_chart(pivot)
                else:
                    st.info("Pas encore assez de données...")

            with col2:
                st.subheader("Répartition des événements")
                types = df["event_type"].value_counts()
                st.bar_chart(types)

            st.divider()

            # === Ligne 2 : Top éléments + Profondeur scroll ===
            col3, col4 = st.columns(2)

            with col3:
                st.subheader("Top 10 éléments cliqués")
                top_clicks = df[df["event_type"] == "click"]["element"].value_counts().head(10)
                if len(top_clicks) > 0:
                    st.bar_chart(top_clicks)
                else:
                    st.info("Aucun clic encore...")

            with col4:
                st.subheader("Profondeur de scroll")
                if len(scroll_depth) > 0:
                    st.bar_chart(scroll_depth.set_index("element")["count"])
                else:
                    st.info("Aucun scroll encore...")

            st.divider()

            # === Flux temps réel ===
            st.subheader("Flux en temps réel")

            # Colorer les lignes par type d'événement
            def color_event(val):
                colors = {
                    "click": "background-color: #1a472a; color: #6bcf7f",
                    "scroll": "background-color: #1a2a47; color: #6b9fff",
                    "pageview": "background-color: #3a1a47; color: #cf6bff",
                    "session_end": "background-color: #472a1a; color: #ffb06b"
                }
                return colors.get(val, "")

            styled = df.head(50).style.map(
                color_event, subset=["event_type"]
            )   
            st.dataframe(styled, width="stretch")

            # Timestamp du dernier refresh
            st.caption(f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        st.error(f"Erreur : {e}")

    time.sleep(2)