import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from romania_data import ROMANIA_MAP, CITY_COORDINATES, ALL_CITIES
from algorithms import greedy_bfs, a_star_search

st.set_page_config(
    page_title="Romania Problem - Informed Search",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    a.header-anchor {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] button[kind="header"] {
        display: none !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1565C0;
        color: white;
    }
    table th, table td {
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

def draw_romania_map(highlight_path=None, path_color="red"):
    G = nx.Graph()
    for u, neighbors in ROMANIA_MAP.items():
        for v, dist in neighbors.items():
            G.add_edge(u, v, weight=dist)

    path_edges = set()
    if highlight_path and len(highlight_path) > 1:
        for i in range(len(highlight_path) - 1):
            u, v = highlight_path[i], highlight_path[i+1]
            path_edges.add((u, v))
            path_edges.add((v, u))

    edge_colors = [path_color if (u, v) in path_edges else '#B0BEC5' for u, v in G.edges()]
    edge_widths = [2.5 if (u, v) in path_edges else 1 for u, v in G.edges()]
    node_colors = ['orange' if n in (highlight_path or []) else '#90CAF9' for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    nx.draw(G, CITY_COORDINATES, ax=ax, with_labels=True,
            node_color=node_colors, edge_color=edge_colors, width=edge_widths,
            node_size=550, font_size=8)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, CITY_COORDINATES, edge_labels=labels, ax=ax, font_size=7)

    plt.tight_layout()
    return fig

with st.sidebar:
    st.header("Pengaturan Rute")

    default_start_idx = ALL_CITIES.index("Arad") if "Arad" in ALL_CITIES else 0
    default_goal_idx = ALL_CITIES.index("Bucharest") if "Bucharest" in ALL_CITIES else len(ALL_CITIES) - 1

    start_city = st.selectbox("Kota Asal:", ALL_CITIES, index=default_start_idx)
    goal_city = st.selectbox("Kota Tujuan:", ALL_CITIES, index=default_goal_idx)

    st.markdown("---")
    mode = st.selectbox(
        "Strategi Algoritma:",
        ["A* Search", "Greedy Best-First Search"]
    )

    btn_solve = st.button("Cari Rute")

st.title("Romania Problem - Informed Search")

if start_city == goal_city:
    st.warning("Kota asal dan kota tujuan sama. Silakan pilih dua kota yang berbeda.")
else:
    if mode == "A* Search":
        res = a_star_search(start_city, goal_city)
    else:
        res = greedy_bfs(start_city, goal_city)

    col1, col2 = st.columns([1.1, 0.9], gap="medium")

    with col1:
        st.subheader("Visualisasi Jalur pada Peta")
        fig = draw_romania_map(res['path'])
        st.pyplot(fig)

    with col2:
        st.subheader("Hasil Pencarian")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Total Jarak", f"{res['total_cost']} km")
        with m2:
            st.metric("Kota Dilewati", f"{len(res['path'])} kota")

        route_str = " ➔ ".join(res['path'])
        st.markdown(f"<div style='font-size: 1.15rem; margin: 10px 0;'><strong>Rute Solusi:</strong> <code style='font-size: 1.05rem; padding: 3px 6px;'>{route_str}</code></div>", unsafe_allow_html=True)
        st.write("")
        st.subheader("Log Langkah")
        df_steps = pd.DataFrame(res['steps'])
        if mode == "Greedy Best-First Search":
            df_steps = df_steps[['step', 'city', 'h', 'f']]
            df_steps.columns = ['Langkah #', 'Kota yang Diekspansi', 'h(n)', 'f(n)']
        else:
            df_steps = df_steps[['step', 'city', 'g', 'h', 'f']]
            df_steps.columns = ['Langkah #', 'Kota yang Diekspansi', 'g(n)', 'h(n)', 'f(n)']
        
        st.table(df_steps, hide_index=True)
