# %%
import pandas as pd
import streamlit as st
import streamlit.components as components
from datetime import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import requests as r

url = url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

geojson = r.get(url=url).json()
# %%
caminho_main = ''
caminho_icons = f'/assets/icons'
caminho_html = f'html'
caminho_html_body = f'{caminho_html}/home.html'
caminho_dataset = f'{caminho_main}datasets//'
markdown_style = f'{caminho_html}markdown_style.html'

# %%
with open(file=f'{caminho_html}/svg-page-home.txt', mode='r', encoding='utf-8') as svg_home:
    css_custom = svg_home.read()

st.set_page_config(page_title='Estoque', layout='wide')

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

st.title('Análise de Estoque')
# %%
df_pedidos = pd.read_csv(f'{caminho_dataset}olist_orders_dataset.csv')
df_itens = pd.read_csv(f'{caminho_dataset}olist_order_items_dataset.csv')
df_clientes = pd.read_csv(f'{caminho_dataset}olist_customers_dataset.csv')



# %%
df_pedidos["order_delivered_carrier_date"] = pd.to_datetime(df_pedidos["order_delivered_carrier_date"])
df_pedidos["order_delivered_customer_date"] = pd.to_datetime(df_pedidos["order_delivered_customer_date"])
df_pedidos["order_estimated_delivery_date"] = pd.to_datetime(df_pedidos["order_estimated_delivery_date"])
df_pedidos["order_purchase_timestamp"] = pd.to_datetime(df_pedidos["order_purchase_timestamp"])
# %%
df_pedidos["time_delivered"] = df_pedidos["order_delivered_customer_date"] - df_pedidos["order_delivered_carrier_date"]
df_pedidos["time_delivered"] = round(df_pedidos["time_delivered"].dt.total_seconds() / 86400,2)

# %%
media_entrega = round(df_pedidos["time_delivered"].mean(),2)


# %%


def sla(estimado,entregue):
    if pd.isna(estimado) or pd.isna(entregue):
        return "PRAZO NÃO DEFINIDO"
    if estimado >= entregue:
        return "DENTRO DO PRAZO"
    elif estimado < entregue:
        return "FORA DO PRAZO"
    else:
        return "Erro"

df_pedidos["teste"] = df_pedidos.apply(
    lambda row: sla(
        row["order_estimated_delivery_date"],
        row["order_delivered_customer_date"]
    ),
    axis=1
)
# %%
df_itens['price_total'] = df_itens['price'] + df_itens['freight_value']

# %%
total_receita = df_itens['price'].sum() + df_itens['freight_value'].sum()
round(total_receita,2)

# %%
columns_kpi1, columns_kpi2 = st.columns(2)
with columns_kpi1:
    media_receita = total_receita / df_itens['order_id'].nunique()
    media_receitakpi = go.Figure(
            go.Indicator(
                mode="number",
                title='Receita média por pedido',
                value=round(media_receita,2),
        )
    )

    media_receitakpi.update_layout(
        height = 250
    )
    st.plotly_chart(figure_or_data=media_receitakpi, use_container_width=True)
with columns_kpi2:
    tempo_medio_entrega = go.Figure(
        go.Indicator(
            mode="number",
            title={"text": "Tempo Médio de Entrega"},
            value=media_entrega
        )
    )

    tempo_medio_entrega.update_layout(
        height = 250
    )
    st.plotly_chart(figure_or_data=tempo_medio_entrega, use_container_width=True)
# %%
columns_paineis_01,columns_paineis_02 = st.columns(2)
with columns_paineis_01:
    conteiner_df_01 = st.container(border=True)
   
    # %%
    with conteiner_df_01:
        prod_mais_vendidos = pd.DataFrame((df_itens['product_id']
                    .groupby(by=df_itens['product_id'])
                    .size()
                    .sort_values(ascending=False)
                    .head(20)
                    .reset_index(name='produto')
))
    # %%
        st.subheader('Produtos mais vendidos')
        st.data_editor(
            prod_mais_vendidos,
            column_config={
                'product_id': st.column_config.TextColumn('Produto'),
                'produto':st.column_config.NumberColumn('Quantidade')
            },
            use_container_width=True,
            disabled=True,
            hide_index=True,
            height=445
        )
with columns_paineis_02:
    conteiner_df_02 = st.container(border=True)
        # %%
    with conteiner_df_02:
        receitas_vendedor = (df_itens[['price_total']].
                             groupby(by=df_itens['seller_id']).
                             sum().
                             sort_values(by='price_total', ascending=False).
                             head(10).
                             reset_index())
        receitas_vendedor['price_total_soma'] = round(receitas_vendedor['price_total'].sum(),2)
        # %%
        receitas_vendedor['% vendido'] = round((receitas_vendedor['price_total'] / receitas_vendedor['price_total_soma']) *100,2)
        # %%
        vendedor_bar = go.Figure()
        vendedor_bar.add_trace(
            go.Bar(
                x=receitas_vendedor['seller_id'],
                y=receitas_vendedor['price_total'],
                name='Faturamento Total'
            )
        )
        vendedor_bar.add_trace(
            go.Scatter(
                x=receitas_vendedor['seller_id'],
                y=receitas_vendedor['% vendido'],
                mode='lines+markers',
                name='Percentual Vendido',
                yaxis='y2'
            )
        )
        vendedor_bar.update_layout(
            title='Venda por Analistas',
            barcornerradius = 6,
            xaxis=dict(
                title='Vendedor',
                tickangle=90
            ),
            yaxis=dict(
                title='Faturamento Total'
            ),
            yaxis2=dict(
                title='Percentual (%)',
                overlaying='y',
                side='right',
                ticksuffix = '%',
                range=[0, 100]
            ),
            height=515,
            legend=dict(
                x=1.08,
                y=1
            )
        )
        st.plotly_chart(figure_or_data=vendedor_bar, use_container_width=True)
# %%
df_status = (
    df_pedidos.
    groupby(by=df_pedidos["teste"]).
    size().
    reset_index(name="qtd")
)
# %%
columns_sla01, columns_sla02 = st.columns(2)
with columns_sla01:
    status_pie = go.Figure(
        go.Pie(
            title={"text": "Status do SLA"},
            values= df_status["qtd"],
            labels=df_status["teste"],
            hole=0.5
        ) 
    )
    st.plotly_chart(figure_or_data=status_pie, use_container_width=True)

##with columns_sla02:
    # %%
    df_pedidos_clientes = df_pedidos.merge(
        right=df_clientes,
        how='inner',
        on=['customer_id']
    ).merge(
        right=df_itens,
        how='inner',
        on=['order_id']
    )
# %%
with columns_sla02:
    df_custo_estado = (df_pedidos_clientes[['price_total','customer_state']]
                        .groupby(by='customer_state')
                        .sum()
                        .sort_values(by='price_total', ascending=False)
                        .reset_index())

# %%

    mapa_custo = px.choropleth(
            data_frame=df_custo_estado,
            title="Custo por Estado",
            geojson=geojson,
            locations='customer_state',
            featureidkey='properties.sigla',
            color = 'price_total',
            color_continuous_scale=[
            [0, "#0F172A"],
            [0.35, "#1D4ED8"],
            [0.70, "#38BDF8"],
            [1, "#E0F2FE"]
            ],
            scope= 'south america'
        )
    
    mapa_custo.update_layout(
    paper_bgcolor="#0B1020",
    plot_bgcolor="#0B1020",
    font=dict(color="#F8FAFC"),
    margin=dict(l=0, r=0, t=20, b=0),
    )

    mapa_custo.update_geos(
        bgcolor="#0B1020",
        showland=True,
        landcolor="#111827",
        showocean=True,
        oceancolor="#0B1020",
        showcountries=True,
        countrycolor="#334155",
        showcoastlines=True,
        coastlinecolor="#334155",
    )
    st.plotly_chart(figure_or_data= mapa_custo, use_container_width=True)

# %% 
doc_dataset = st.expander('Documentação')
with doc_dataset:
    doc, dataset = st.tabs(['documentação','Dataset'])
    with doc:
        doc.markdown("""
        <h4> Documentação da Análise</h4>
        <h5> Fonte dos dados</h5>
        <p>
        Este dataset foi obtido a partir da plataforma Kaggle e disponibilizado pela empresa brasileira Olist. 
        Ele contém dados reais de pedidos realizados entre 2016 e 2018 em múltiplos marketplaces no Brasil. 
        As informações abrangem diferentes dimensões do processo de e-commerce, incluindo clientes, pedidos, pagamentos, produtos, logística e avaliações.
        Os dados foram anonimizados e estruturados pela Olist para fins de análise e aprendizado, não sendo fornecidos detalhes completos sobre o processo de coleta, tratamento ou possíveis vieses.
        </p>
        
        <p> Link Kaggle:  <a href="https://www.kaggle.com/datasets/rathokolokgaboparis/brazilian-e-commerce-public-dataset-by-olist?utm_source=chatgpt.com&select=olist_customers_dataset.csv"> kaggle.com </a> </p>
        <h5> 📊 Insights Gerados:</h5>
        <li> Média por pedido (df_itens): Quanto cada cliente gasta por pedido</li>
        <li> Qual a Porcentagem Vendida de cada vendedor </li>
        <li> Tempo médio da Entrega </li>
        <li> Custo por Região </li>
                     
        <h5> 📌 Criação de novas colunas no DataFrame</h5>
        <li>Receita Total: consiste no frete mais o preço do pedido</li>
        <li> Tempo de Entrega: Diferencia de quando a transportadora recebeu o pedido e quando o cliente recebeu o pedido </li>
        
                     
""",
unsafe_allow_html=True)

    with dataset:
        st.markdown(
        """<div class="container"> <h3> DataSets Utilizados: </h3> </div>
        """,
        unsafe_allow_html=True
        )
        dataset_01,dataset_02,dataset_03 = st.tabs(['Pedidos Realizados','Itens do Pedido','Clientes'])

        with dataset_01:
            df_pedidos

            st.markdown("""
        <div>
            <h4> Estrutura do DataSet</h4> 
                <table border="solid 1px black">
                    <tr>
                        <td> Coluna</td>
                        <td> Tipo de Dado </td>
                        <td> Descrição Resumida </td>
                    </tr>
                    <tr>
                        <td> order_id </td>
                        <td> string </td>
                        <td> Identificador único do pedido </td>
                    </tr>
                    <tr>
                        <td> customer_id </td>
                        <td> string </td>
                        <td> Identificador do cliente (anonimizado) </td>
                    </tr>
                    <tr>
                        <td> order_status </td>
                        <td> string </td>
                        <td> Status atual do pedido</td>
                    </tr>
                    <tr>
                        <td> order_purchase_timestamp </td>                                
                        <td> DateTime</td>                    
                        <td> Data e hora da compra</td>
                    </tr>
                    <tr>
                        <td> order_approved_at </td>
                        <td> DateTime </td>                        
                        <td> Quando o pagamento foi aprovado </td>                        
                    </tr>
                    <tr>
                        <td> order_delivered_carrier_date </td>
                        <td> DateTime </td>                        
                        <td> Quando o pedido foi enviado para transportadora </td>                        
                    </tr>
                    <tr>
                        <td> order_delivered_customer_date </td>                        
                        <td> DateTime </td>
                        <td> Quando o Cliente recebeu o pedido</td>                        
                    </tr 
                    <tr>
                        <td> order_estimated_delivery_date</td>                        
                        <td> DateTime</td>
                        <td> Data estimada de entrega </td>                        
                    </tr>
                </table>
        </div>
                """, unsafe_allow_html=True
        )
        with dataset_02:
            df_itens
            st.markdown(
                """
<div>
    <h4> Estrutura do DataSet</h4> 
        <table border="solid 1px black">
            <tr>
                <td> Coluna</td>
                <td> Tipo de Dado </td>
                <td> Descrição Resumida </td>
            </tr>
            <tr>
                <td> order_id </td>
                <td> string </td>
                <td> Id do pedido </td>
            </tr>
            <tr>
                <td> order_item_id </td>
                <td> int </td>
                <td> Número sequencial do item dentro do pedido </td>
            </tr>
            <tr>
                <td> product_id </td>
                <td> string </td>
                <td> Identificador do produto</td>
            </tr>
            <tr>
                <td> seller_id </td>                                
                <td> string</td>                    
                <td> identificador do vendedor</td>
            </tr>
            <tr>
                <td> shipping_limit_date </td>
                <td> DateTime </td>                        
                <td> Prazo Maximo para o vendedor enviar o produto </td>                        
            </tr>
            <tr>
                <td> price </td>
                <td> float </td>                        
                <td> preco do produto </td>                        
            </tr>
            <tr>
                <td> freight_value </td>                        
                <td> float </td>
                <td> valor do frete</td>                        
            </tr 
        </table>
</div>
""",
unsafe_allow_html=True
            )

        with dataset_03:
            df_clientes
            st.markdown(
                """
<div>
    <h4> Estrutura do DataSet</h4> 
        <table border="solid 1px black">
            <tr>
                <td> Coluna</td>
                <td> Tipo de Dado </td>
                <td> Descrição Resumida </td>
            </tr>
            <tr>
                <td> customer_id </td>
                <td> string </td>
                <td> Identificador do cliente </td>
            </tr>
            <tr>
                <td> customer_unique_id </td>
                <td> string </td>
                <td> Identificador unico do cliente </td>
            </tr>
            <tr>
                <td> customer_zip_code_prefix </td>
                <td> string </td>
                <td> Região(CEP)</td>
            </tr>
            <tr>
                <td> customer_city </td>                                
                <td> string</td>                    
                <td> cidade</td>
            </tr>
            <tr>
                <td> customer_state </td>
                <td> string </td>                        
                <td> Estado </td>                        
            </tr>
        </table>
</div>
""",
unsafe_allow_html=True
            )