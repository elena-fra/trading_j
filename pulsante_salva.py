#PULSANTE SALVA
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