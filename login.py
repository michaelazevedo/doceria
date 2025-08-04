import streamlit as st
from PIL import Image

def show_login_page():
    """
    Função para exibir a página de login.
    """
    # Cria duas colunas para alinhar a imagem e o título
    col1, col2 = st.columns([1, 5])
    with col1:
        # Carrega e exibe a imagem do logo
        try:
            image = Image.open("img/logo.jpg")
            st.image(image, width=150)
        except FileNotFoundError:
            st.error("Imagem 'logo.jpg' não encontrada. Verifique o caminho.")

    with col2:
        st.title("Acessar Sistema")

    # Define as credenciais de acesso
    credentials = {
        "username": "loanna",
        "password": "101219"
    }

    # Campos de entrada para o usuário e senha com chaves únicas
    username = st.text_input("Usuário", key="login_username")
    password = st.text_input("Senha", type="password", key="login_password")

    # Botão de login com chave única
    if st.button("Entrar", key="login_button"):
        # Verifica se as credenciais estão corretas
        if username == credentials["username"] and password == credentials["password"]:
            # Se as credenciais estiverem corretas, define o estado de sessão como logado
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
            # O aplicativo principal irá redirecionar para a página de vendas
            st.rerun()
        else:
            # Exibe uma mensagem de erro em caso de credenciais incorretas
            st.error("Usuário ou senha incorretos. Tente novamente.")

def show_logout_button():
    """
    Função para exibir um botão de logout.
    """
    if st.button("Sair", key="logout_button"):
        # Ao clicar no botão, redefine o estado de sessão para deslogado
        st.session_state.logged_in = False
        st.rerun()

# Inicializa o estado de sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login_page()
else:
    # Este bloco é apenas para demonstração do `login.py`
    st.title("Bem-vindo(a) à Página de Vendas")
    st.write("Você está logado.")
    show_logout_button()
