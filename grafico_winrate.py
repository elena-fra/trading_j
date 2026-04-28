import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

def mostra_grafico_winrate(df):
    if df.empty:
        st.info("Nessun trade salvato.")
        return

    counts = df["risultato"].value_counts()

    take_profit = counts.get("Take Profit", 0)
    stop_loss = counts.get("Stop Loss", 0)

    totale = take_profit + stop_loss

    if totale == 0:
        st.info("Non ci sono ancora Take Profit o Stop Loss da mostrare.")
        return

    values = [take_profit, stop_loss]
    colors = ["#22c55e", "#ef4444"]

    fig, ax = plt.subplots(figsize=(2, 2), facecolor="none")

    wedges, texts, autotexts = ax.pie(
        values,
        colors=colors,
        startangle=110,
        autopct=lambda p: f"{p:.0f}%" if p > 0 else "",
        pctdistance=0.58,
        shadow=True,
        radius=0.55,
        wedgeprops=dict(linewidth=0),
        textprops=dict(color="white", fontsize=5.5, fontweight="bold")
    )

    ax.axis("equal")
    ax.set_title("WIN RATE", fontsize=11, fontweight="bold", color="#ff00ff", pad=6)

    for t in texts:
        t.set_text("")

    plt.tight_layout(pad=0.2)

    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", dpi=200)
    buf.seek(0)

    st.image(buf, width=240)

    plt.close(fig)