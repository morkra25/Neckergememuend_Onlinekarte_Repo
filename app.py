import streamlit as st
import folium
import geopandas as gpd

from folium.plugins import (
    MeasureControl,
    Draw,
    Fullscreen,
    MousePosition,
    MarkerCluster,
    MiniMap
)

from streamlit_folium import st_folium

# -------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Kühle Karte Neckargemünd",
    page_icon="🧊",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f4f8f4;
}

h1 {
    color: #1f4d3a;
}

section[data-testid="stSidebar"] {
    background-color: #e8f3ea;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DATEN LADEN
# -------------------------------------------------

@st.cache_data
def load_data():

    gdf = gpd.read_file(
        "baenke_neckergemuend.geojson"
    )

    return gdf


gdf = load_data()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("🧊 Kühle Karte")

st.sidebar.markdown("""
Diese interaktive Karte zeigt Aufenthaltsorte
und Sitzmöglichkeiten in Neckargemünd.

Die Anwendung unterstützt dabei,
kühle und angenehme Orte im Stadtgebiet
zu finden.
""")

st.sidebar.markdown("---")

st.sidebar.subheader("🗺️ Kartenoptionen")

show_baenke = st.sidebar.checkbox(
    "Sitzbänke anzeigen",
    value=True
)

cluster = st.sidebar.checkbox(
    "Marker clustern",
    value=True
)

kartenstil = st.sidebar.selectbox(
    "Kartenstil",
    [
        "OpenStreetMap",
        "CartoDB positron",
        "CartoDB dark_matter"
    ]
)

zoom = st.sidebar.slider(
    "Zoom",
    min_value=10,
    max_value=18,
    value=13
)

st.sidebar.markdown("---")

st.sidebar.subheader("🪑 Legende")

st.sidebar.markdown("""
🪑 Sitzbank  
📏 Messwerkzeug  
✏️ Zeichenwerkzeug  
🌍 Interaktive Karte
""")

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("🧊 Kühle Karte Neckargemünd")

st.markdown("""
Willkommen bei der interaktiven Kühlen Karte für
Neckargemünd.

Die Karte unterstützt Bürger dabei,
angenehme Aufenthaltsorte im Stadtgebiet
zu entdecken und Sitzmöglichkeiten
im öffentlichen Raum zu finden.
""")

# -------------------------------------------------
# KARTE
# -------------------------------------------------

m = folium.Map(
    location=[49.392, 8.795],
    zoom_start=zoom,
    tiles=kartenstil,
    control_scale=True
)

# -------------------------------------------------
# TOOLS
# -------------------------------------------------

MeasureControl(
    position="topright",
    primary_length_unit="meters",
    secondary_length_unit="kilometers",
    primary_area_unit="sqmeters"
).add_to(m)

Draw(
    export=True
).add_to(m)

Fullscreen().add_to(m)

MousePosition().add_to(m)

MiniMap().add_to(m)

# -------------------------------------------------
# BÄNKE
# -------------------------------------------------

if show_baenke:

    # -----------------------------------------
    # CLUSTER OPTIONAL
    # -----------------------------------------

    if cluster:
        ziel_layer = MarkerCluster().add_to(m)
    else:
        ziel_layer = m

    # -----------------------------------------
    # MARKER
    # -----------------------------------------

    for _, row in gdf.iterrows():

        popup_text = """
        <div style="
            width:220px;
            font-size:14px;
            font-family:Arial;
        ">
        """

        popup_text += "<h4>🪑 Sitzbank</h4>"

        felder = [
            ("Material", "material"),
            ("Sitzplätze", "seats"),
            ("Rückenlehne", "backrest"),
            ("Überdacht", "covered"),
            ("Ausrichtung", "direction"),
            ("Beschreibung", "description"),
            ("Typ", "bench:type")
        ]

        for label, feld in felder:

            if feld in row:

                wert = row[feld]

                if wert is not None and str(wert) != "nan":

                    popup_text += f"<b>{label}:</b> {wert}<br>"

        popup_text += "</div>"

        folium.Marker(

            location=[
                row.geometry.y,
                row.geometry.x
            ],

            popup=folium.Popup(
                popup_text,
                max_width=250
            ),

            icon=folium.DivIcon(
                html="""
                    <div style="
                        font-size:14px;
                        transform: translate(-7px, -7px);
                    ">
                        🪑
                    </div>
                """
            )

        ).add_to(ziel_layer)

# -------------------------------------------------
# LAYER CONTROL
# -------------------------------------------------

folium.LayerControl().add_to(m)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown("---")

st.markdown("""
Die Karte basiert auf Daten aus
OpenStreetMap und dient der Visualisierung
von Aufenthalts- und Sitzmöglichkeiten
im öffentlichen Raum.
""")

# -------------------------------------------------
# KARTE ANZEIGEN
# -------------------------------------------------

st_folium(
    m,
    width=None,
    height=850,
    returned_objects=[]
)