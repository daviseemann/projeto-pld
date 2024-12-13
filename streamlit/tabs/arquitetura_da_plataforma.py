import streamlit as st
import graphviz as gv


def arquitetura_da_plataforma():
    st.header("Arquitetura da Plataforma")

    st.markdown(
        """
    Este projeto é um painel interativo desenvolvido com Streamlit para visualizar e analisar os preços de liquidação diária (PLD) no mercado de energia elétrica. A aplicação permite que os usuários baixem, limpem e visualizem dados históricos de preços, além de aplicar filtros para refinar as análises.

    ### Funcionamento do Projeto

    1. **Download e Limpeza de Dados**:
       - A função `download_pld` faz uma requisição ao site da CCEE para baixar o arquivo Excel contendo os dados históricos de preços.
       - A função `clean_pld_data` processa o arquivo Excel, transformando-o em um formato adequado para análise e salvando os dados limpos em um arquivo CSV.

    2. **Carregamento de Dados**:
       - A função `load_data` carrega o arquivo CSV mais recente contendo os dados limpos e os converte em um DataFrame do Pandas.

    3. **Aplicação de Filtros**:
       - A função `apply_filters` permite que os usuários selecionem um intervalo de datas e submercados específicos para filtrar os dados exibidos.

    4. **Visualização de Dados**:
       - O painel possui várias abas, cada uma dedicada a uma métrica específica, como PLD Médio Diário, PLD Médio Mensal, PLD Máximo e Mínimo, Desvio Padrão e Spread Diário, PLD Total Mensal e Número de Dias Acima da Média.
       - Cada aba aplica os filtros selecionados e exibe gráficos interativos utilizando Plotly.

    5. **Arquitetura da Plataforma**:
       - Uma aba adicional exibe um diagrama da arquitetura da plataforma, mostrando a interação entre os componentes do sistema, como o usuário, a aplicação Streamlit, o pipeline de dados, o site da CCEE, o armazenamento de dados brutos e limpos, e as visualizações de KPIs.
    """
    )

    st.write("Diagrama da arquitetura da plataforma:")

    # Criar o diagrama
    diagram = gv.Digraph(format="svg")

    # Adicionar nós
    diagram.node("A", "Usuário", rank="same")
    diagram.node("B", "Streamlit App", rank="same")
    diagram.node("C", "Data Pipeline", rank="same")
    diagram.node("D", "CCEE Website", rank="same")
    diagram.node("E", "Raw Data Storage", rank="same")
    diagram.node("F", "Clean Data Storage", rank="same")
    diagram.node("G", "Visualizações e KPIs", rank="same")

    # Adicionar subgráficos para criar blocos
    with diagram.subgraph(name="cluster_0") as c:
        c.attr(style="filled", color="lightgrey")
        c.node_attr.update(style="filled", color="white")
        c.edges([("A", "B"), ("B", "C")])
        c.attr(label="Frontend")

    with diagram.subgraph(name="cluster_1") as c:
        c.attr(style="filled", color="lightgrey")
        c.node_attr.update(style="filled", color="white")
        c.edges([("C", "D"), ("C", "E"), ("C", "F")])
        c.attr(label="Backend")

    with diagram.subgraph(name="cluster_2") as c:
        c.attr(style="filled", color="lightgrey")
        c.node_attr.update(style="filled", color="white")
        c.edges([("B", "G"), ("F", "B")])
        c.attr(label="Data Storage & Visualization")

    # Renderizar o diagrama
    st.graphviz_chart(diagram)
