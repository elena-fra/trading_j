import streamlit as st
import pandas as pd
import plotly.express as px


def mostra_grafico_pnl(df):
    if not isinstance(df, pd.DataFrame):
        st.error("Errore: il grafico PnL non ha ricevuto un DataFrame valido.")
        return

    if df.empty:
        st.info("Nessun trade disponibile per il grafico PnL.")
        return

    colonne_necessarie = ["data_trade", "pnl"]
    for colonna in colonne_necessarie:
        if colonna not in df.columns:
            st.warning("Per mostrare il grafico PnL servono le colonne 'data_trade' e 'pnl'.")
            return

    df = df.copy()

    df["data_trade"] = pd.to_datetime(df["data_trade"], errors="coerce")
    df["pnl"] = pd.to_numeric(df["pnl"], errors="coerce")

    df = df.dropna(subset=["data_trade", "pnl"])

    if df.empty:
        st.info("I dati del grafico PnL non sono validi dopo la pulizia.")
        return

    df["data_trade"] = df["data_trade"].dt.date

    df_giornaliero = (
        df.groupby("data_trade", as_index=False)["pnl"]
        .sum()
        .sort_values("data_trade")
    )


    fig = px.line(
    df_giornaliero,
    x="data_trade",
    y="pnl",
    markers=True,
    title="PnL giornaliero",
    labels={
        "data_trade": "Giorni",
        "pnl": "Profit/Loss (€)"
    }
)

    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    fig.update_traces(
        mode="lines+markers",
        line=dict(color="#00BFFF", width=3),
        marker=dict(size=7)
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        xaxis_title="Data",
        yaxis_title="Profit/Loss (€)",
        title_x=0.5
    )

    fig.update_xaxes(
        tickformat="%d/%m/%Y"
    )

    st.plotly_chart(fig, width='content')