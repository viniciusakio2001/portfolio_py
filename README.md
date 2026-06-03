# Cases - Portfólio Pessoal

Portfólio pessoal desenvolvido em Streamlit para apresentar projetos de análise de dados. O projeto reúne uma página inicial com apresentação profissional e cases interativos criados com Python, Pandas e Plotly.

## Sobre o projeto

Este repositório tem como objetivo demonstrar habilidades em análise de dados, construção de dashboards e exploração de indicadores de negócio. A aplicação possui navegação lateral, página de perfil e dashboards com filtros, KPIs, gráficos e documentação dos dados utilizados.

Perfil apresentado no app:

- Analista de Dados
- Experiência com SQL, Python, Power BI e Excel
- Foco em evolução para Engenharia de Dados

## Cases disponíveis

### Case de Vendas

Dashboard de análise comercial com base em uma planilha de vendas. O case permite filtrar os dados por cidade, categoria, período e produto.

Principais análises:

- Faturamento total
- Faturamento médio por venda
- Dia com maior faturamento
- Faturamento por produto
- Faturamento por categoria
- Faturamento por cidade
- Evolução do faturamento por período

### Case de Estoque

Dashboard baseado em dados públicos de e-commerce da Olist. O case analisa pedidos, itens vendidos, clientes, receita, entrega e distribuição por estado.

Principais análises:

- Receita média por pedido
- Tempo médio de entrega
- Produtos mais vendidos
- Receita por vendedor
- Status de SLA de entrega
- Custo por estado em mapa interativo

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL
- HTML e CSS customizados

## Estrutura do projeto

```text
cases/
|-- Home.py
|-- requirements.txt
|-- assets/
|   |-- icons/
|   `-- image/
|-- datasets/
|   |-- pandas_cases_datasets.xlsx
|   |-- olist_customers_dataset.csv
|   |-- olist_order_items_dataset.csv
|   `-- olist_orders_dataset.csv
|-- html/
|   |-- home.html
|   |-- markdown_style.html
|   `-- svg-page-home.txt
`-- pages/
    |-- Case_Vendas.py
    `-- case_Estoque.py


## Datasets

O projeto utiliza datasets locais armazenados na pasta `datasets/`.

No Case de Estoque, também é usado um arquivo GeoJSON público com os estados do Brasil para renderizar o mapa por UF.

## Contato

- LinkedIn: [Vinicius Sousa](https://www.linkedin.com/in/vinicius-sousa-4400b0199/)
- GitHub: [viniciusakio2001](https://github.com/viniciusakio2001)
- E-mail: [viniciushada2001@gmail.com.br](mailto:viniciushada2001@gmail.com.br)
