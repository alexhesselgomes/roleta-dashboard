# Painel Avançado de Roleta 🎰

Este é um dashboard interativo feito com Streamlit para análise de resultados de roleta.

## Funcionalidades

- Upload de resultados (.csv ou .xlsx) ou entrada manual
- Análises por:
  - Setores personalizados
  - Dúzias, colunas, cores, par/ímpar
  - Matriz de transição entre setores
  - Combinações mais frequentes (setor + dúzia)
  - Tempo médio entre repetições
- Previsão de próximo setor baseado em padrão anterior

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run dashboard_roleta_avancado.py
```

Ou publique gratuitamente via [Streamlit Cloud](https://streamlit.io/cloud).