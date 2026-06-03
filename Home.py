# %% 
import streamlit as st
import streamlit.components.v1 as components

#  %%
caminho_icons = 'assets/icons'
caminho_html = 'html'
caminho_main = ''
caminho_html_body = f'{caminho_html}/home.html'
markdown_style = f'{caminho_html}/markdown_style.html'

with open(file=f'{caminho_html}/svg-page-home.txt', mode='r', encoding='utf-8') as svg_home:
    css_custom = svg_home.read()

st.set_page_config(page_title='Sobre Mim', page_icon=f'{caminho_icons}/page_icon_home.svg', layout='wide', initial_sidebar_state='expanded')

with open(file=markdown_style, mode='r', encoding='utf-8') as style_st:
    markdown_streamlit = style_st.read()
    st.markdown(markdown_streamlit, unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-block">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Perfil</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item active">', unsafe_allow_html=True)
    st.page_link("Home.py", label="🏠  Home")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Projetos</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">', unsafe_allow_html=True)
    st.page_link("pages/Case_Vendas.py", label=":money_with_wings:  Case de Vendas")
    st.markdown('</div>', unsafe_allow_html=True)

    st.page_link("pages/case_Estoque.py", label=":card_file_box:  Case Estoque")
    st.markdown('</div>', unsafe_allow_html=True)

    #st.markdown('<div class="sidebar-section">Perfil</div>', unsafe_allow_html=True)
    #st.markdown('<div class="nav-item">', unsafe_allow_html=True)
    #st.markdown('</div>', unsafe_allow_html=True)
    #st.markdown('</div>', unsafe_allow_html=True)
    
with open(file=caminho_html_body, mode='r', encoding='utf-8') as body:
    html = body.read()
    components.html(html, height=700, scrolling=False)