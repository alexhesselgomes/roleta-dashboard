
import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import os
import datetime

# Google Drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

st.set_page_config(page_title="Painel Roleta com Histórico", layout="wide")
st.title("🎰 Painel de Análise de Roleta com Salvamento Local e Google Drive")

# Setup para salvar localmente
HISTORICO_LOCAL = "historico_jogadas.csv"

# Função para salvar localmente
def salvar_local(df):
    df.to_csv(HISTORICO_LOCAL, index=False)
    st.success("💾 Histórico salvo localmente.")

# Função para salvar no Google Drive
def salvar_drive(df):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("credentials.json")
    drive = GoogleDrive(gauth)

    filename = f"historico_roleta_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    f = drive.CreateFile({'title': filename})
    f.SetContentFile(filename)
    f.Upload()
    st.success(f"📤 Histórico enviado ao Google Drive: {filename}")
    os.remove(filename)

# Carregamento de arquivo
uploaded_file = st.file_uploader("📥 Envie um arquivo .csv com uma coluna de números", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if df.shape[1] > 1:
        df = df.iloc[:, [0]]
    df.columns = ["Número"]
    df.dropna(inplace=True)
    df = df[df["Número"].apply(lambda x: str(x).isdigit())]
    df["Número"] = df["Número"].astype(int)
    st.dataframe(df.tail(10))

    numeros = df["Número"].tolist()
    contagem = Counter(numeros)

    st.subheader("📊 Frequência")
    st.write(contagem.most_common(10))

    st.subheader("🔮 Previsão da Próxima Jogada")
    moda = contagem.most_common(1)[0][0]
    st.write(f"**Número mais provável:** 🎯 {moda}")

    # Salvar
    if st.button("💾 Salvar histórico localmente"):
        salvar_local(df)

    if st.button("☁️ Salvar histórico no Google Drive"):
        salvar_drive(df)
else:
    st.info("📄 Envie um arquivo CSV para começar.")
