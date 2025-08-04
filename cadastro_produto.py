import streamlit as st
import pandas as pd
import json
import os

def load_products():
    """
    Carrega os produtos do arquivo JSON. Se o arquivo não existir, retorna uma lista vazia.
    """
    if os.path.exists('produtos.json'):
        with open('produtos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_products(products):
    """
    Salva a lista de produtos no arquivo JSON.
    """
    with open('produtos.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=4, ensure_ascii=False)
    st.rerun()

def show_product_registration_page():
    """
    Função para exibir o conteúdo da página de cadastro de produtos.
    """
    st.title("Cadastro de Produto")

    products = load_products()
    
    product_map = {p['nome']: p for p in products}
    product_names = [p['nome'] for p in products]

    # Combobox para selecionar um produto ou adicionar um novo
    selected_product_name = st.selectbox(
        "Gerenciar Produto",
        options=["--- Novo Produto ---"] + product_names,
        key="product_selector"
    )

    is_new_product = selected_product_name == "--- Novo Produto ---"
    
    if not is_new_product:
        product_to_manage = product_map[selected_product_name]
        default_name = product_to_manage["nome"]
        default_price = product_to_manage["preco"]
        default_quantity = product_to_manage.get("quantidade", 0)  # Adiciona quantidade padrão
    else:
        default_name = ""
        default_price = 12.00
        default_quantity = 0

    # Campos de entrada para o nome, preço e quantidade em uma única linha
    col1, col2, col3 = st.columns([3,1,1])
    with col1:
        product_name = st.text_input("Nome do Produto", value=default_name, key="product_name_input")
    with col2:
        product_price = st.number_input("Preço", min_value=0.01, format="%.2f", value=default_price, key="product_price_input")
    with col3:
        product_quantity = st.number_input("Quantidade", min_value=0, step=1, value=default_quantity, key="product_quantity_input")
    
    st.markdown("---")
    
    # Botões de ação
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    if is_new_product:
        with col_btn1:
            if st.button("Cadastrar", key="save_button"):
                if product_name and product_price:
                    new_product = {
                        "nome": product_name,
                        "preco": product_price,
                        "quantidade": product_quantity # Adiciona a quantidade
                    }
                    products.append(new_product)
                    st.success(f"Produto '{product_name}' cadastrado com sucesso!")
                    save_products(products)
                else:
                    st.error("Por favor, preencha todos os campos.")
        with col_btn2:
            if st.button("Limpar", key="clear_button_new"):
                st.rerun()
    else:
        with col_btn1:
            if st.button("Salvar Alterações", key="save_changes_button"):
                if product_name and product_price:
                    for p in products:
                        if p['nome'] == selected_product_name:
                            p['nome'] = product_name
                            p['preco'] = product_price
                            p['quantidade'] = product_quantity # Atualiza a quantidade
                            break
                    st.success(f"Produto '{product_name}' editado com sucesso!")
                    save_products(products)
                else:
                    st.error("Por favor, preencha todos os campos.")
        with col_btn2:
            if st.button("Excluir", key="delete_button"):
                products_to_keep = [p for p in products if p['nome'] != selected_product_name]
                save_products(products_to_keep)
                st.success(f"Produto '{selected_product_name}' excluído com sucesso!")
        with col_btn3:
            if st.button("Limpar", key="clear_button_edit"):
                st.rerun()

    st.markdown("---")
    
    # Tabela com os produtos cadastrados
    st.subheader("Produtos Cadastrados")
    if products:
        products_df = pd.DataFrame(products)
        # Reordena as colunas para exibir "quantidade"
        column_order = ["nome", "preco", "quantidade"]
        products_df = products_df[column_order]
        st.dataframe(products_df)

        # Calcula o total do estoque
        total_estoque = sum(p['preco'] * p['quantidade'] for p in products)
        st.metric("Total em Estoque", f"R$ {total_estoque:,.2f}")
    else:
        st.info("Nenhum produto cadastrado ainda.")
