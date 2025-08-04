import streamlit as st
import pandas as pd
import json
import os

def load_sales_history():
    """
    Carrega a lista de histórico de vendas do arquivo JSON.
    """
    if os.path.exists('historico_vendas.json'):
        with open('historico_vendas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def show_sales_history_page():
    """
    Exibe o conteúdo da página de histórico de vendas.
    """
    st.title("📜 Histórico de Vendas")

    sales_history = load_sales_history()

    if not sales_history:
        st.info("Nenhuma venda no histórico ainda.")
        return

    sales_df = pd.DataFrame(sales_history)

    # Reorganiza colunas na ordem esperada
    expected_columns = ["Produto", "Total", "Cliente", "Quantidade", "Data Venda", "Status"]
    sales_df = sales_df[[col for col in expected_columns if col in sales_df.columns]]

    # Converte "Total" para float caso esteja em string
    sales_df["Total"] = pd.to_numeric(sales_df["Total"], errors='coerce')

    # Mostra total das vendas pagas
    total_pago = sales_df[sales_df["Status"] == "Pago"]["Total"].sum()
    st.metric("💰 Total Vendido (Pagos)", f"R$ {total_pago:,.2f}")

    st.markdown("---")
    st.dataframe(sales_df, use_container_width=True)

# Chamada direta (para testes locais)
# show_sales_history_page()
