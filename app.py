import streamlit as st
from login import show_login_page
from vendas import show_sales_page
from cadastro_produto import show_product_registration_page
#C:\Users\ximae\OneDrive\Área de Trabalho\Python\Doceria\vendas.py
# URL para a imagem de fundo (substitua por uma imagem real se desejar)
BACKGROUND_IMAGE_URL = "https://www.confeitariaboa.com.br/wp-content/uploads/2023/12/Culinaria-e-confeitaria-red.-certo.jpg"
# Injeta CSS para um fundo com imagem, camada transparente e estilo de login
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{BACKGROUND_IMAGE_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white; /* Cor do texto padrão */
    }}
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6); /* Camada semitransparente preta */
        z-index: 0;
    }}
    .stApp > header {{
        background-color: transparent !important;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1;
    }}
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.1); /* Fundo da caixa de login */
        backdrop-filter: blur(10px); /* Efeito de vidro fosco */
        border-radius: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        max-width: 500px;
        margin: auto;
        margin-top: 10vh;
        z-index: 10;
        position: relative;
    }}
    h1 {{
        color: #FFD700; /* Cor dourada para títulos */
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
    }}
    label {{
        color: #FFD700 !important; /* Cor dourada para rótulos */
    }}
    .stButton > button {{
        background-color: #FFD700;
        color: black;
        border-radius: 10px;
        font-weight: bold;
        transition: background-color 0.3s;
    }}
    .stButton > button:hover {{
        background-color: #e6b800;
    }}
    .stTextInput > div > div > input, .stSelectbox > div > div, .stNumberInput > div > input {{
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 8px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializa o estado de sessão para controlar o login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Vendas"

# Verifica o estado de login
if st.session_state.logged_in:
    # Se o usuário estiver logado, exibe o menu de navegação na barra lateral
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Navegar", ["Vendas", "Cadastro de Produto"])
    st.session_state.current_page = page

    # Roteia para a página correta
    if st.session_state.current_page == "Vendas":
        show_sales_page()
    elif st.session_state.current_page == "Cadastro de Produto":
        show_product_registration_page()
else:
    # Se o usuário não estiver logado, exibe a página de login
    show_login_page()
