# Projeto PLD

Este repositório contém um painel interativo desenvolvido com **Streamlit** para visualização de dados de Preços de Liquidação Diária (PLD). O painel oferece funcionalidades para análise de diversas métricas relacionadas ao PLD, incluindo médias, máximos, mínimos, desvio padrão e outros indicadores.

## Funcionalidades

- **PLD Médio Diário**: Exibição da média diária dos preços de liquidação.
- **PLD Médio Mensal**: Análise da média mensal dos preços.
- **PLD Máximo e Mínimo**: Visualização dos valores extremos (máximo e mínimo) dos preços de liquidação.
- **Desvio Padrão e Spread Diário**: Análise estatística do desvio padrão e do spread diário dos preços.
- **PLD Total Mensal**: Soma dos preços de liquidação em base mensal.
- **Número de Dias Acima da Média**: Contagem dos dias em que os preços ficaram acima da média diária.
- **Arquitetura da Plataforma**: Descrição detalhada da arquitetura utilizada no projeto.

---

## Instruções de Configuração

### Executando Localmente a Partir do Repositório

1. Clone o repositório:

   ```sh
   git clone https://github.com/daviseemann/projeto-pld.git
   cd projeto-pld
   ```

2. Certifique-se de que o Docker está instalado. Caso não tenha, você pode instalá-lo [aqui](https://www.docker.com/products/docker-desktop).

3. Construa a imagem Docker:

   ```sh
   docker build -t daviseemann/projeto-pld:latest .
   ```

4. Execute o container:

   ```sh
   docker run -p 8501:8501 daviseemann/projeto-pld:latest
   ```

5. Acesse o painel no navegador em: `http://localhost:8501`.

---

### Utilizando o GitHub Container Registry (GHCR)

1. Faça login no GitHub Container Registry:

   ```sh
   echo $CR_PAT | docker login ghcr.io -u daviseemann --password-stdin
   ```

2. Baixe a imagem do GHCR:

   ```sh
   docker pull ghcr.io/daviseemann/projeto-pld:latest
   ```

3. Execute o container:

   ```sh
   docker run -p 8501:8501 ghcr.io/daviseemann/projeto-pld:latest
   ```

4. Acesse o painel no navegador em: `http://localhost:8501`.

---

### Executando Localmente Sem Docker

1. Clone o repositório:

   ```sh
   git clone https://github.com/daviseemann/projeto-pld.git
   cd projeto-pld
   ```

2. Crie e ative um ambiente virtual:

   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

4. Execute a aplicação:

   ```sh
   streamlit run main.py
   ```

5. Acesse o painel no navegador em: `http://localhost:8501`.
