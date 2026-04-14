import streamlit as st
import pandas as pd
from pulsante_salva import salva_trade_dati, mostra_statistiche

st.set_page_config(page_title="Trading Journal", page_icon="", layout="wide")


nome = st.text_input("Inserisci il tuo nome")

#titolo
if nome:
    st.title(f"Trading Journal di {nome}")
else:
    st.title("Trading Journal")



if "apri_journal" not in st.session_state:
    st.session_state.apri_journal = False

if st.button("Nuovo Trade"):
    st.session_state.apri_journal = True

if st.session_state.apri_journal:

    st.subheader("Inserimento trade")

    col1, col2, col3 = st.columns([1.2, 1.2, 1])

    # COLONNA 1
    with col1:
        trade_numero = st.text_input("Trade n*:", width=200, key= "trade_numero")

        st.markdown(
            '<p style="font-size:21px;">Barra delle emozioni</p>',
            unsafe_allow_html=True
        )

        emozione = st.select_slider(
            "Umore pre-trade",
            options=["arrabbiato", "sereno", "triste"],
            value="sereno",
            width=200,
            key="emozione"
        )

        st.markdown(
            '<div style="font-size:28px; width:200px; display:flex; justify-content:space-between;">'
            '<span>😡</span><span>😐</span><span>😢</span></div>',
            unsafe_allow_html=True
        )

    # COLONNA 2
    with col2:
        asset = st.text_input("Inserisci Asset", width=200, key="asset")

        risultato = st.selectbox(
            "Come sei uscitx dal Trade",
            ["Stop Loss", "Stop Profit", "Take Profit", "Trailing Stop"],
            width=200,
            key= "risultato"
        )

        mercato = st.text_area("Condizioni di mercato", width=200, key="mercato")

        trigger_entrata = st.text_area("Qual è stato il trigger d'entrata?", width=200, key="trigger_entrata")

        motivo_uscita = st.text_area("Se hai chiuso tu, perché?", width=200, key="motivo_uscita")

        contratti = st.selectbox("N* Contratti", range(1, 11), width=200, key="contratti")

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
                width=200,
                key="chiusura"
            )

    # COLONNA 3
    with col3:
        prezzo_entrata = st.text_input("Prezzo d'entrata", width=200, key= "prezzo_entrata")
        prezzo_uscita = st.text_input("Prezzo d'uscita", width=200, key= "prezzo_uscita")

        direzione = st.selectbox(
            "Side",
            ["Long", "Short"],
            width=200,
            key="direzione"
        )

   


    if "trades" not in st.session_state:
        st.session_state.trades = []
    
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

col_spazio, col_chiudi, col_salva = st.columns([4, 1, 1])

with col_chiudi:
    chiudi = st.button("Chiudi Trade", key="chiudi_journal", use_container_width=True)

with col_salva:
    if st.button("Salva Trade", key="salva_trade", use_container_width=True):
        if salva_trade_dati():
            st.success("✅ Trade salvato con successo!")
            st.session_state.apri_journal = False
            st.rerun()

















    