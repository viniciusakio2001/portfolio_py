# %%

import pandas as pd
import streamlit as st
import streamlit.components as components
from datetime import datetime as dt
import plotly.express as px

# %%
caminho_icons = 'assets/icons'
caminho_html = 'html/'
caminho_main = ''
caminho_html_body = f'{caminho_html}home.html'
caminho_dataset = 'datasets/pandas_cases_datasets'
markdown_style = f'{caminho_html}markdown_style.html'

with open(file=f'{caminho_html}svg-page-home.txt', mode='r', encoding='utf-8') as svg_home:
    css_custom = svg_home.read()

st.set_page_config(page_title='Vendas', layout='wide', initial_sidebar_state='expanded')

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

# %%

df_vendas = pd.read_excel(io=f'{caminho_dataset}.xlsx',sheet_name=0)


# %%
df_vendas['data']=pd.to_datetime(df_vendas['data'])
df_vendas['data_fmt'] = df_vendas['data'].dt.strftime('%d/%m/%Y')

# %%

replace_cidade = {
    'SP': 'São Paulo',
    'sao Paulo': 'São Paulo',
    'sao paulo': 'São Paulo',
    'Sao paulo': 'São Paulo',
    'RJ': 'Rio de Janeiro',
    'rio de janeiro': 'Rio de Janeiro',
    'rio de Janeiro': 'Rio de Janeiro',
    'Rio de janeiro': 'Rio de Janeiro'  
}
df_vendas['cidade'] = df_vendas['cidade'].replace(replace_cidade)

# %%
df_vendas['faturamento'] = df_vendas['preco'] * df_vendas['quantidade']

# %%
df_vendas_filtrado = df_vendas.copy()

# %%
st.title('Análise de Vendas')

filt_expander = st.expander('Filtros')

with filt_expander:
    filt_column1, filt_column2, filt_column3, filt_column4 = st.columns(4)
    with filt_column1:
        filtro_cidade = st.multiselect(
            'Cidade',
            options=sorted(df_vendas['cidade'].unique()),
            default=sorted(df_vendas['cidade'].unique())
            )
        
        
# %%
    with filt_column2:
        filtro_categoria = st.multiselect(
            'Categoria',
            options=sorted(df_vendas['categoria'].unique()),
            default=sorted(df_vendas['categoria'].unique())
        )
    with filt_column3:
        min_data = df_vendas['data'].min()
        max_data = df_vendas['data'].max()
        filtro_periodo_ini, filtro_periodo_fim = st.date_input(
            'Período',
            min_value=min_data,
            max_value=max_data,
            value=(min_data,max_data)
        )

    with filt_column4:
        filtro_produto = st.multiselect(
            'Produto',
            options=sorted(df_vendas['produto'].unique()),
            default=sorted(df_vendas['produto'].unique())
        )
# %%        
df_vendas_filtrado = df_vendas[
    (df_vendas['cidade'].isin(filtro_cidade)) &
    (df_vendas['produto'].isin(filtro_produto)) &
    (df_vendas['categoria'].isin(filtro_categoria)) &
    (df_vendas['data'] >= pd.to_datetime(filtro_periodo_ini)) &
    (df_vendas['data'] <= pd.to_datetime(filtro_periodo_fim))
]

if df_vendas_filtrado.empty:
    st.warning('⚠️ Nenhum dado encontrado com os filtros selecionados.')
    st.info('Tente alterar os filtros ou expandir o período.')
    st.stop()
# %%
col1, col2,col3 = st.columns(3)
with col1:
    card1 = st.container(border=True, height=200)
    fat_total = round(df_vendas_filtrado['faturamento'].sum(),2)    
    card1.write('Faturamento Total')
    card1.subheader(fat_total,help=f'Calculo: Soma total do faturamento: {df_vendas_filtrado['preco'].sum()} * {df_vendas_filtrado['quantidade'].sum()}')

with col2:
    card2 = st.container(border=True, height=200)
    fat_medio = df_vendas_filtrado['faturamento'].sum() / len(df_vendas_filtrado)
    card2.write('Faturamento médio por Venda')
    card2.subheader(round(fat_medio,2),help=f'Calculo: faturamento total: {fat_total} / quantidade de vendas: {len(df_vendas_filtrado)}')
# %%

with col3:
    card3 = st.container(border=True, height=200)
    card3.write('Dia com maior Faturamento')
    dia_com_mais_venda = (df_vendas_filtrado[['faturamento']]
                          .groupby(by=df_vendas_filtrado['data_fmt'])
                          .sum()
                          .sort_values(by='faturamento', ascending=False)
                          .head(1))
    data = dia_com_mais_venda.index[0]
    valor = round(dia_com_mais_venda['faturamento'].iloc[0],2)
    card3.subheader(data)
    card3.subheader(f'R$ {valor}')

# %%
graph_bar = st.container()

with graph_bar:

    graph_01, graph_02 = st.columns(2)
    with graph_01:
        tab_prod, tab_categoria = st.tabs(['Produto','Categoria'])
        fat_produto = (df_vendas_filtrado[['faturamento']]
                .groupby(by=df_vendas_filtrado['produto'])
                .sum()
                .sort_values(by=['faturamento'], ascending=False)
                .reset_index())
    with tab_prod:
        show_graph_bar_prod = px.bar(
            fat_produto, 
            x='faturamento',
            y='produto', 
            orientation='h',
            title='Faturamento por Produto',
            hover_data=['produto','faturamento']
        )

        show_graph_bar_prod.update_traces(
            marker=dict(
                cornerradius=8
            )
        )
        st.plotly_chart(show_graph_bar_prod, use_container_width=True)

        fat_categoria = (df_vendas_filtrado[['faturamento']]
                .groupby(by=df_vendas_filtrado['categoria'])
                .sum()
                .sort_values(by='faturamento', ascending=False)
                .reset_index())
    with tab_categoria: 
        show_graph_bar_cat = px.bar(
            fat_categoria,
            x='faturamento',
            y='categoria',
            orientation='h',
            title='Faturamento por Categoria'
        )
        show_graph_bar_cat.update_traces(
            marker=dict(
                cornerradius=8
            )
        )
        st.plotly_chart(show_graph_bar_cat, use_container_width=True)

# %%

    fat_cidade = (df_vendas_filtrado[['faturamento']]
            .groupby(by=df_vendas_filtrado['cidade'])
            .sum()
            .sort_values(by='faturamento', ascending=False)
            .reset_index())
# %%
    show_graph_pie = px.pie(
        fat_cidade,
        values='faturamento',
        names='cidade',
        hole=0.5,
        title='Faturamento por Cidade'
    )
    graph_02.plotly_chart(show_graph_pie, use_container_width=True)

# %%
fat_periodo = (df_vendas_filtrado[['faturamento']]
               .groupby(by=df_vendas_filtrado['data'])
                .sum()
                .reset_index()
            )
# %%
show_graph_line = px.area(
    fat_periodo,
    x='data',
    y='faturamento'
)
st.plotly_chart(show_graph_line, use_container_width=True)
# %%
docs = st.expander('Documentação')
with docs:
    data, doc = st.tabs(['Dados Planilha', 'Documentação'])
    with data:
        df_vendas
    with doc:
        st.markdown("""
        <h4>📌 Descrição geral<h4>
        <p>Este dataset representa transações de vendas realizadas em diferentes cidades, contendo informações sobre produtos, categorias, preços e quantidades vendidas.</p><br>

        <p>O objetivo é permitir análises exploratórias e geração de indicadores de desempenho comercial.</p>

        <h4>🧱 Estrutura dos Dados </h4>
        <table border="1">
            <thead>
                <tr>
                    <th>Coluna</th>
                    <th>Tipo</th>
                    <th>Descrição</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>data</td>
                    <td>datetime</td>
                    <td>Data da venda</td>
                </tr>
                <tr>
                    <td>produto</td>
                    <td>string</td>
                    <td>Nome do produto vendido</td>
                </tr>
                <tr>
                    <td>categoria</td>
                    <td>string</td>
                    <td>Categoria do produto</td>
                </tr>
                <tr>
                    <td>preco</td>
                    <td>float</td>
                    <td>Preço unitário do produto</td>
                </tr>
                <tr>
                    <td>quantidade</td>
                    <td>int</td>
                    <td>Quantidade vendida</td>
                </tr>
                <tr>
                    <td>cidade</td>
                    <td>string</td>
                    <td>Cidade onde a venda ocorreu</td>
                </tr>
            </tbody>
        </table>
        <h4>⚙️ Métricas Principais</h4>
                    
        <li>💰 Faturamento Total</li>
        <li>Soma de todas as vendas realizadas.</li>
        <li>faturamento = preco * quantidade</li>
        <li>📦 Faturamento por Produto</li>
        <li>Permite identificar quais produtos geram maior receita.</li>
        <li>🏆 Top 5 Produtos Mais Vendidos</li>
        <li>Ranking baseado na quantidade total vendida por produto.</li>
        <li>🌎 Faturamento por Cidade</li>
        <li>Analisa a distribuição geográfica da receita.</li>
        <li>🎯 Ticket Médio por Venda</li>
        <li>Média de valor por transação.</li>
        <li>ticket_medio = faturamento_total / numero_de_vendas</li>
        <li>Faturamento por Período.</li>
        <li>Gráfico de linha para mostrar a faturamento mês a mês</li><br>          
        ⚠️ Importante: considerar cada linha como uma venda (ou ajustar conforme o modelo do dataset).

        <h4>🧠 Conceitos Técnicos Trabalhados</h4>
        <li>groupby() → agregação de dados</li>
        <li>criação de colunas derivadas</li>
        <li>ordenação e ranking (sort_values)</li>
        <li>manipulação de datas</li>
                    
        <h4>🚀 Desafios Propostos</h4>
        <li>🔍 Dia com Maior Faturamento</li>
        <li>Identificar a data com maior volume de vendas.</li>         
        <li>📊 Ranking por Categoria</li>
        <li>Ordenar categorias com base no faturamento total.</li>
                    
        <h4>⚠️ Pontos de Atenção</h4>
        <li>Padronização de dados (ex: cidades com nomes diferentes)</li>
        <li>Conversão correta de datas</li>
        <li>Cálculo correto de faturamento (preço * quantidade)</li>
        <li>Interpretação correta do que representa uma “venda”</li><br>
                    
        <h4>💡 Possíveis Extensões</h4>
        <li>Análise temporal (por mês, semana, dia)</li>
        <li>Comparação entre cidades</li>
        <li>Identificação de tendências de vendas</li>
        <li>Criação de dashboards interativos</li>
        """,
        unsafe_allow_html=True
    )

