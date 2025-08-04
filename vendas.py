import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Carrega os produtos e vendas existentes
def load_products():
    if os.path.exists('produtos.json'):
        with open('produtos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_products(products):
    with open('produtos.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

def load_sales():
    if os.path.exists('vendas.json'):
        with open('vendas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_sales(sales):
    with open('vendas.json', 'w', encoding='utf-8') as f:
        json.dump(sales, f, indent=4, ensure_ascii=False)
    st.rerun()

def load_sales_history():
    if os.path.exists('historico_vendas.json'):
        with open('historico_vendas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_sales_history_entry(sale):
    if sale["Status"] != "Pago":
        return  # Não salva se não estiver pago
    sales_history = load_sales_history()
    sales_history.append(sale)
    with open('historico_vendas.json', 'w', encoding='utf-8') as f:
        json.dump(sales_history, f, indent=4, ensure_ascii=False)

def show_sales_page():
    st.title("Página de Vendas")

    products = load_products()
    products_map = {p['nome']: p for p in products}
    product_names = [p['nome'] for p in products]
    sales = load_sales()
    
    sales_df = pd.DataFrame(sales)
    
    if not sales_df.empty:
        if 'Quantidade' not in sales_df.columns:
            sales_df['Quantidade'] = 0
        total_vendido = sales_df['Total'].sum()
        total_pago = sales_df[sales_df['Status'] == 'Pago']['Total'].sum()
        total_nao_pago = sales_df[sales_df['Status'] == 'Ñ pago']['Total'].sum()

        st.markdown("---")
        col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
        col_metrics1.metric("Total Vendido", f"R$ {total_vendido:,.2f}")
        col_metrics2.metric("Total Pago", f"R$ {total_pago:,.2f}")
        col_metrics3.metric("Total Não Pago", f"R$ {total_nao_pago:,.2f}")
        st.markdown("---")

    if 'editing_sale_index' not in st.session_state:
        st.session_state.editing_sale_index = None

    sale_options = ["--- Nova Venda ---"] + [f"{s['Cliente']} - {s['Data Venda']}" for s in sales]
    selected_sale_option = st.selectbox("Gerenciar Venda", sale_options, key="sale_selector")
    is_new_sale = selected_sale_option == "--- Nova Venda ---"

    default_quantity = 1
    default_product = None
    default_client = ""
    default_status = "Ñ pago"
    
    if not is_new_sale:
        selected_index = sale_options.index(selected_sale_option) - 1
        editing_sale = sales[selected_index]
        default_quantity = editing_sale.get("Quantidade", 0)
        default_product = editing_sale["Produto"]
        default_client = editing_sale["Cliente"]
        default_status = editing_sale["Status"]
        st.session_state.editing_sale_index = selected_index
    else:
        st.session_state.editing_sale_index = None

    col1, col2 = st.columns([1,3])
    with col1:
        quantity = st.number_input("Quantidade", step=1, value=default_quantity, key="sale_quantity")
    with col2:
        selected_product_name = st.selectbox("Produto", product_names, index=product_names.index(default_product) if default_product else 0, key="sale_product")
    
    client_name = st.text_input("Cliente", value=default_client, key="sale_client")
    
    product_price = 0
    if selected_product_name and selected_product_name in products_map:
        product_price = products_map[selected_product_name]['preco']
    
    total = quantity * product_price
    st.text(f"Total: R$ {total:.2f}")

    status_options = ['Pago', 'Ñ pago', 'Marcar']
    status = st.selectbox("Status", status_options, index=status_options.index(default_status) if default_status in status_options else 0, key="sale_status")   
    

    if is_new_sale:
        if st.button("Vender", key="sell_button"):
            if selected_product_name and quantity > 0:
                current_product = products_map[selected_product_name]
                if current_product.get('quantidade', 0) >= quantity:
                    current_product['quantidade'] -= quantity
                    save_products(products)

                    new_sale = {
                        "Produto": selected_product_name,
                        "Total": total,
                        "Cliente": client_name,
                        "Quantidade": quantity,
                        "Data Venda": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Status": status
                    }
                    sales.append(new_sale)
                    save_sales(sales)
                    save_sales_history_entry(new_sale)  # <- Aqui está a cópia se for "Pago"
                    st.success("Venda registrada com sucesso!")
                else:
                    st.error(f"Quantidade insuficiente em estoque. Disponível: {current_product.get('quantidade', 0)}")
            else:
                st.error("Por favor, preencha a quantidade e o produto.")
    else:
        col_edit1, col_edit2, col_edit3 = st.columns(3)
        with col_edit1:
            if st.button("Salvar Alterações", key="save_changes_button"):
                if selected_product_name and quantity > 0:
                    editing_sale = sales[st.session_state.editing_sale_index]
                    original_product = products_map[editing_sale["Produto"]]
                    original_product['quantidade'] += editing_sale.get("Quantidade", 0)
                    products_map[selected_product_name]['quantidade'] -= quantity
                    save_products(products)

                    editing_sale["Produto"] = selected_product_name
                    editing_sale["Total"] = total
                    editing_sale["Cliente"] = client_name
                    editing_sale["Quantidade"] = quantity
                    editing_sale["Data Venda"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    editing_sale["Status"] = status
                    
                    save_sales(sales)
                    save_sales_history_entry(editing_sale)  # <- Também salva alteração, se for Pago
                    st.success("Venda alterada com sucesso!")
                else:
                    st.error("Por favor, preencha a quantidade e o produto.")
        with col_edit2:
            if st.button("Excluir Venda", key="delete_button"):
                del sales[st.session_state.editing_sale_index]
                save_sales(sales)
                st.success("Venda excluída com sucesso!")
        with col_edit3:
            if st.button("Limpar", key="clear_button"):
                st.rerun()

        
    st.subheader("Vendas Realizadas")
    
    if not sales_df.empty:
        column_order = ["Produto", "Quantidade", "Total", "Cliente", "Data Venda", "Status"]
        sales_df = sales_df[column_order]
        st.dataframe(sales_df)
    else:
        st.info("Nenhuma venda realizada ainda.")    
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()
