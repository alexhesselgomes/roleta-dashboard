
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

st.set_page_config(page_title="Painel Roleta", layout="wide")

# Funções auxiliares
def mapear_setor(numero):
    mapa_setores = {
        1: 1, 4: 1, 7: 1, 10: 1, 13: 1, 16: 1, 19: 1, 22: 1, 25: 1, 28: 1, 31: 1, 34: 1,
        2: 2, 5: 2, 8: 2, 11: 2, 14: 2, 17: 2, 20: 2, 23: 2, 26: 2, 29: 2, 32: 2, 35: 2,
        3: 3, 6: 3, 9: 3, 12: 3, 15: 3, 18: 3, 21: 3, 24: 3, 27: 3, 30: 3, 33: 3, 36: 3,
        0: 0
    }
    return mapa_setores.get(numero, -1)

def mapear_duzia(n):
    if n == 0: return 0
    elif 1 <= n <= 12: return 1
    elif 13 <= n <= 24: return 2
    elif 25 <= n <= 36: return 3

def mapear_coluna(n):
    if n == 0: return 0
    elif n % 3 == 1: return 1
    elif n % 3 == 2: return 2
    else: return 3

def mapear_cor(n):
    vermelhos = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    pretos = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
    if n == 0: return 'Verde'
    elif n in vermelhos: return 'Vermelho'
    elif n in pretos: return 'Preto'
    else: return 'Desconhecido'

# Entrada de dados
st.title("🎰 Painel Avançado de Análise de Roleta")
with st.expander("📥 Inserir Dados"):
    modo = st.radio("Escolha o modo de entrada:", ["Upload de Arquivo", "Entrada Manual"])

    if modo == "Upload de Arquivo":
        uploaded_file = st.file_uploader("Envie um arquivo CSV ou Excel com os resultados", type=["csv", "xlsx"])
        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, header=None)
            else:
                df = pd.read_excel(uploaded_file, header=None)
            numeros = df.values.flatten().tolist()
    else:
        entrada_manual = st.text_area("Digite os números separados por vírgula", "6, 35, 0, 9, 12, 14, 10")
        numeros = list(map(int, entrada_manual.split(",")))

# Somente prosseguir se houver números válidos
if 'numeros' in locals() and len(numeros) > 1:
    st.success(f"{len(numeros)} números carregados com sucesso!")

    # Processar características
    setores = [mapear_setor(n) for n in numeros]
    duzias = [mapear_duzia(n) for n in numeros]
    colunas = [mapear_coluna(n) for n in numeros]
    cores = [mapear_cor(n) for n in numeros]
    pares = ["Par" if n != 0 and n % 2 == 0 else "Ímpar" if n != 0 else "Zero" for n in numeros]

    # Frequência
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Frequência por Setor")
        st.bar_chart(pd.Series(setores).value_counts().sort_index())
    with col2:
        st.subheader("🎨 Frequência por Cor")
        st.bar_chart(pd.Series(cores).value_counts())

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("📍 Frequência por Dúzia")
        st.bar_chart(pd.Series(duzias).value_counts().sort_index())
    with col4:
        st.subheader("📌 Frequência por Coluna")
        st.bar_chart(pd.Series(colunas).value_counts().sort_index())

    st.subheader("🔁 Matriz de Transição entre Setores")
    transicoes = [(setores[i], setores[i+1]) for i in range(len(setores)-1)]
    trans_counts = Counter(transicoes)
    matriz = pd.DataFrame(0, index=[0,1,2,3], columns=[0,1,2,3])
    for (i, j), val in trans_counts.items():
        matriz.loc[i, j] = val
    fig, ax = plt.subplots()
    sns.heatmap(matriz, annot=True, fmt="d", cmap="Oranges", ax=ax)
    st.pyplot(fig)

    # Previsão
    ultimo_setor = setores[-1]
    st.subheader(f"🔮 Previsão após o Setor {ultimo_setor}")
    proximos = matriz.loc[ultimo_setor]
    if proximos.sum() > 0:
        probs = (proximos / proximos.sum()).sort_values(ascending=False)
        st.bar_chart(probs)

    # Combinações
    st.subheader("🔥 Combinações Setor + Dúzia Mais Frequentes")
    combinacoes = pd.Series(list(zip(setores, duzias)))
    st.dataframe(combinacoes.value_counts().head(5))

    # Repetição e tempo entre
    st.subheader("⏱️ Tempo entre repetições")
    tempo_rep = {}
    for i, n in enumerate(numeros):
        if n in tempo_rep:
            tempo_rep[n].append(i - tempo_rep[n][-1])
        else:
            tempo_rep[n] = [0]
    tempo_df = {k: np.mean(v[1:]) if len(v) > 1 else 0 for k, v in tempo_rep.items()}
    st.dataframe(pd.DataFrame.from_dict(tempo_df, orient='index', columns=["Intervalo Médio"]))
