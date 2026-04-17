import streamlit as st
import pandas as pd
import sqlite3


st.set_page_config(page_title="Trading Journal", page_icon="", layout="wide")

conn = sqlite3.connect("trades.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    trade numero TEXT,
    emozione TEXT,
    asset TEXT,
    risultato TEXT,
    mercato TEXT,
    trigger entrata TEXT,
    motivo uscita TEXT,
    contratti INTEGER,
    chiusura TEXT,
    prezzo entrata TEXT,
    prezzo uscita TEXT,
    direzione TEXT
)
""")
conn.commit()

def salva_trade_sql(dati):
    cur.execute("""
    INSERT INTO trades (
        nome, trade numero, emozione, asset, risultato, mercato,
        trigger entrata, motivo uscita, contratti, chiusura,
        prezzo entrata, prezzo uscita, direzione
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, dati)
    conn.commit()

nome = st.text_input("Inserisci il tuo nome")

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

    with col2:
        asset = st.text_input("Inserisci Asset", key="asset")

        risultato = st.selectbox(
            "Come sei uscitx dal Trade",
            ["Stop Loss", "Stop Profit", "Take Profit", "Trailing Stop"],
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

        direzione = st.selectbox(
            "Side",
            ["Long", "Short"],
            key="direzione"
        )

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

if salva and st.session_state.apri_journal:
    dati_trade = (
        "nome",
        "trade numero",
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
        direzione
    )

    salva_trade_sql(dati_trade)
    st.success("Trade salvato nel database.")

if chiudi:
    st.session_state.apri_journal = False

df = pd.read_sql("SELECT * FROM trades ORDER BY id DESC", conn)

if not df.empty:
    st.subheader("Trade salvati")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Scarica CSV",
        data=csv,
        file_name="trades.csv",
        mime="text/csv"
    )

