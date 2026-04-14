import streamlit as st
import pandas as pd

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
    salva = st.button("Salva Trade", key="salva_trade", use_container_width=True)

    

















    import streamlit as st
import pandas as pd
import os
from datetime import datetime

def salva_trade_dati():
    """Salva i dati del trade corrente in trades.csv"""
    
    # Recupera tutti i dati dai session_state
    nuovo_trade = {
        "data_ora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": st.session_state.get("nome", ""),
        "trade_numero": st.session_state.get("trade_numero", ""),
        "emozione": st.session_state.get("emozione", ""),
        "asset": st.session_state.get("asset", ""),
        "risultato": st.session_state.get("risultato", ""),
        "mercato": st.session_state.get("mercato", ""),
        "trigger_entrata": st.session_state.get("trigger_entrata", ""),
        "motivo_uscita": st.session_state.get("motivo_uscita", ""),
        "contratti": st.session_state.get("contratti", 1),
        "chiusura": st.session_state.get("chiusura", ""),
        "prezzo_entrata": st.session_state.get("prezzo_entrata", ""),
        "prezzo_uscita": st.session_state.get("prezzo_uscita", ""),
        "direzione": st.session_state.get("direzione", "")
    }
    
    FILE_TRADES = "trades.csv"
    
    # Crea il file se non esiste
    if not os.path.exists(FILE_TRADES):
        df = pd.DataFrame(columns=nuovo_trade.keys())
        df.to_csv(FILE_TRADES, index=False)
    
    # Aggiunge il nuovo trade
    df = pd.read_csv(FILE_TRADES)
    df = pd.concat([df, pd.DataFrame([nuovo_trade])], ignore_index=True)
    df.to_csv(FILE_TRADES, index=False)
    
    return True

def mostra_statistiche():
    """Mostra statistiche base dai trade salvati"""
    FILE_TRADES = "trades.csv"
    
    if os.path.exists(FILE_TRADES):
        df = pd.read_csv(FILE_TRADES)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Trade totali", len(df))
        with col2:
            st.metric("Win Rate", f"{len(df[df['risultato'].str.contains('Profit', na=False)])/len(df)*100:.1f}%")
        with col3:
            st.metric("Long", len(df[df['direzione']=='Long']))
        with col4:
            st.metric("Short", len(df[df['direzione']=='Short']))
        
        st.dataframe(df.tail(10))
    else:
        st.info("Nessun trade salvato ancora")