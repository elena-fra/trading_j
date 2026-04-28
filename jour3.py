import streamlit as st
import pandas as pd
import sqlite3

from grafico_winrate import mostra_grafico_winrate
from pulsante_salva import carica_trades, salva_trade, init_db
from grafico_pnl import mostra_grafico_pnl


st.set_page_config(page_title="Trading Journal", page_icon="", layout="wide")


# Inizializza database
init_db()


# Stato iniziale
if "apri_journal" not in st.session_state:
    st.session_state.apri_journal = False


# Callback pulsanti
def apri_trade():
    st.session_state.apri_journal = True


def chiudi_trade():
    st.session_state.apri_journal = False


# Input nome
nome = st.text_input("Inserisci il tuo nome")

if nome:
    st.title(f"Trading Journal di {nome}")
else:
    st.title("Trading Journal")


# Bottone apertura journal
st.button("Nuovo Trade", on_click=apri_trade)


# CSS pulsanti
st.markdown("""
<style>
div.stElementContainer.st-key-salva_trade div.stButton > button {
    background-color: #39FF14 !important;
    color: black !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    font-size: 18px !important;
}

div.stElementContainer.st-key-chiudi_journal div.stButton > button {
    background-color: #9400D3 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)


# Apertura journal
if st.session_state.apri_journal:
    st.subheader("Inserimento trade")

    col1, col2, col3 = st.columns([1.2, 1.2, 1])

    with col1:
        trade_numero = st.text_input("Trade n*:", key="trade_numero")

        st.markdown(
            '<p style="font-size:21px;">Barra delle emozioni</p>',
            unsafe_allow_html=True
        )

        emozione = st.select_slider(
            "Umore pre-trade",
            options=["arrabbiato", "sereno", "triste"],
            value="sereno",
            key="emozione"
        )

        st.markdown(
            '<div style="font-size:28px; width:200px; display:flex; justify-content:space-between;">'
            '<span>😡</span><span>😐</span><span>😢</span></div>',
            unsafe_allow_html=True
        )

        data_trade= st.date_input("Data", key="data_trade")

    with col2:
        asset = st.text_input("Inserisci Asset", key="asset")

        risultato = st.selectbox(
            "Come sei uscitx dal Trade",
            ["Stop Loss", "Stop in Pari", "Take Profit", "Trailing Stop"],
            key="risultato"
        )

        mercato = st.text_area("Condizioni di mercato", key="mercato")
        trigger_entrata = st.text_area("Qual è stato il trigger d'entrata?", key="trigger_entrata")
        motivo_uscita = st.text_area("Se hai chiuso tu, perché?", key="motivo_uscita")

        contratti = st.selectbox("N* Contratti", range(1, 11), key="contratti")

        chiusura = ""
        if contratti > 1:
            chiusura = st.selectbox(
                "Come hai chiuso i contratti?",
                [
                    "Tutti insieme",
                    "Parzialmente",
                    "Uno alla volta",
                    "Break even + target",
                    "Stop + target"
                ],
                key="chiusura"
            )

    with col3:
        prezzo_entrata = st.text_input("Prezzo d'entrata", key="prezzo_entrata")
        prezzo_uscita = st.text_input("Prezzo d'uscita", key="prezzo_uscita")
        pnl = st.number_input("Profit/Loss (€)", step=1.0, format="%.2f", key="pnl")

        direzione = st.selectbox(
            "Side",
            ["Long", "Short"],
            key="direzione"
        )

    # Pulsanti
    col_spazio, col_chiudi, col_salva = st.columns([4, 1, 1])

    with col_chiudi:
        st.button(
            "Chiudi Trade",
            key="chiudi_journal",
            use_container_width=True,
            on_click=chiudi_trade
        )

    with col_salva:
        salva = st.button(
            "Salva Trade",
            key="salva_trade",
            use_container_width=True
        )

    # Azione salvataggio
    if salva:
        dati_trade = (
            nome,
            trade_numero,
            data_trade,
            emozione,
            asset,
            risultato,
            mercato,
            trigger_entrata,
            motivo_uscita,
            contratti,
            chiusura,
            prezzo_entrata,
            prezzo_uscita,
            direzione,
            pnl
        )

        salva_trade(dati_trade)
        st.success("Trade salvato con successo")


# Carica dati dal DB
df = carica_trades()


# Tabella trades
# Stato visualizzazione tabella
if "mostra_tutti_trades" not in st.session_state:
    st.session_state.mostra_tutti_trades = False

# Tabella
if not df.empty:
    st.subheader("Trade salvati")

    df_visibile = df if st.session_state.mostra_tutti_trades else df.head(5)
    st.dataframe(df_visibile, use_container_width=True)

    if len(df) > 5:
        testo_bottone = (
            "Mostra solo ultimi 5"
            if st.session_state.mostra_tutti_trades
            else "Visualizza tutto"
        )

        if st.button(testo_bottone, key="toggle_trades"):
            st.session_state.mostra_tutti_trades = not st.session_state.mostra_tutti_trades
            st.rerun()


# Statistiche finali
if not df.empty:
    st.markdown("---")
    st.subheader("Statistiche")

    mostra_grafico_winrate(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Scarica CSV",
        data=csv,
        file_name="trades.csv",
        mime="text/csv",
        key="download_csv_trades"
    )


mostra_grafico_pnl(df)