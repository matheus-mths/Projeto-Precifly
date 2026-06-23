# PreciFly - Sistema Inteligente de Precificação

O **PreciFly** é uma aplicação desktop desenvolvida como projeto acadêmico para auxiliar microempreendedores e lojistas a calcularem o preço ideal de venda de seus produtos. O sistema automatiza a análise de custos, integra impostos em tempo real baseados na localização e simula margens de lucro líquidas e taxas de marketplaces parceiros de forma simplificada.

---

## Intuído do Projeto

Precificar um produto no mercado brasileiro vai muito além de aplicar uma simples porcentagem sobre o custo de compra. É necessário considerar variações tributárias estaduais, taxas de cartões/maquininhas e as pesadas comissões cobradas por plataformas de e-commerce. 

O **PreciFly** resolve essa dor de cabeça centralizando esses cálculos em uma interface intuitiva, garantindo que o empreendedor saiba exatamente qual será sua margem de lucro real e evite vender no prejuízo.

---

## Tecnologias Utilizadas

O projeto foi construído utilizando o ecossistema Python e ferramentas modernas de interface e armazenamento:

* **Python 3**: Linguagem base do projeto.
* **Tkinter & ttkbootstrap**: Frameworks utilizados para criar uma interface gráfica (GUI) moderna, limpa e responsiva (Tema: *Superhero*).
* **SQLite**: Banco de dados relacional e local, ideal para persistência de dados ágil e sem necessidade de servidores externos.
* **Requests, Gzip & JSON**: Módulos responsáveis por consumir, descompactar e processar os dados tributários vindos da API pública do IBPT.
* **Pillow (PIL)**: Biblioteca utilizada para a renderização de elementos visuais e logotipos na interface.

---

## Como o Sistema Funciona

O fluxo do sistema é dividido em três etapas principais: Autenticação, Consulta/Gerenciamento de Estoque e Cálculo Dinâmico.

### 1. Autenticação Segura
O sistema possui um controle de acesso via tela de login integrada ao banco de dados, protegendo as informações comerciais e o estoque do usuário.

### 2. Sincronização de Impostos (API IBPT)
Ao selecionar um produto e o estado (UF) de venda, o sistema realiza uma requisição para buscar as alíquotas de imposto atualizadas (Nacional, Estadual e Municipal) correspondentes ao código **NCM** (Nomenclatura Comum do Mercosul) do item. Para poupar dados e acelerar consultas futuras, o PreciFly implementa um sistema de **cache local** gerando arquivos JSON para os estados já consultados.

### 3. Motores de Precificação
O usuário insere a taxa da maquininha de cartão e a margem de lucro desejada. A partir disso, o app calcula:
* **Custo Total**: Custo base somado ao valor nominal bruto dos impostos do IBPT.
* **Preço Mínimo**: O valor limite de venda para cobrir os custos operacionais (ponto de equilíbrio, sem lucro).
* **Preço Ideal**: O valor final recomendado para obter exatamente a margem de lucro pretendida.
* **Simulador de Marketplaces**: Exibe valores corrigidos para venda direta nas plataformas mais utilizadas, aplicando as comissões oficiais do **Mercado Livre (14%)**, **Shopee (13%)**, **Amazon (15%)** e **Magalu (12%)**.

---

## Estrutura de Arquivos

* `TelaLogin.py`: Gerencia a interface de login e a inicialização segura do programa.
* `TelaPrincipal.py`: Painel central (Dashboard) onde o usuário busca produtos, preenche as variáveis de venda e visualiza os cards de resultados.
* `calculo.py`: O "coração" lógico do projeto; lida com as chamadas de API, compressão/descompressão de dados tributários e os algoritmos matemáticos de precificação.
* `banco.db`: Arquivo do banco de dados SQLite responsável por armazenar as tabelas do sistema.

---

## Estrutura do Banco de Dados

O banco de dados armazena informações estruturadas de forma relacional:

* **Tabela `usuarios`**: Controla o acesso ao sistema (ID, Nome, Email e Senha).
* **Tabela `produtos`**: Guarda os dados técnicos e comerciais dos itens (ID, Nome, UF, código NCM, código CEST, Custo e Margem de Lucro).
* **Tabela `sqlite_sequence`**: Controle interno para autoincremento de IDs de tabelas.

---

## Como Executar o Projeto

### Pré-requisitos
Antes de começar, você precisará ter o Python instalado em sua máquina. Também são necessárias as bibliotecas de interface e requisições.
* Instale as dependências necessárias: pip install ttkbootstrap requests pillow
* Execute a aplicação através da tela de login: python TelaLogin.py
* Para utilização, o banco de dados já conta com um usuário administrador previamente cadastrado: 
    * E-mail: admin@gmail.com
    * Senha: 123456
