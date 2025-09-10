Loja FastAPI - Sistema de Gerenciamento de Vendas
Descrição
O "Loja FastAPI" é um sistema de gerenciamento de loja completo, construído com o framework FastAPI. A aplicação oferece um conjunto de APIs robustas para gerenciar usuários, produtos, vendas e relatórios de contabilidade. A interface do usuário é construída com HTML, CSS e JavaScript, fornecendo um painel intuitivo para as operações diárias da loja.

Funcionalidades
🔐 Autenticação e Usuários
Cadastro de Usuário: Criação de novos usuários com nome de usuário, e-mail e senha.

Login e Token JWT: Autenticação via nome de usuário e senha, retornando um token de acesso JWT.

Atualização de Dados: Capacidade de o usuário autenticado atualizar suas próprias informações.

Deleção de Usuário: Deleção de contas, garantindo que apenas o próprio usuário possa realizar a ação.

📦 Gerenciamento de Produtos
CRUD de Produtos: Endpoints para criar, visualizar (com paginação e filtros por nome ou ID), atualizar e deletar produtos.

Gerenciamento de Estoque: Cada produto possui uma quantidade (QT) que é atualizada automaticamente após cada venda.

🛒 Sistema de Vendas
Criação de Carrinho/Venda: A API permite a criação de uma venda, consumindo o estoque dos produtos e registrando a transação no banco de dados.

Simulação de Pagamento: Um endpoint create-payment que simula a geração de um pagamento (incluindo QR Code em base64) antes de a venda ser confirmada.

📊 Relatórios de Contabilidade
Relatório Diário: Resumo do dia com o total de vendas e o valor total arrecadado.

Relatório por Período: Permite buscar vendas detalhadas dentro de um intervalo de datas específico.

Produtos Mais Vendidos: Um relatório que lista os produtos mais vendidos, ordenados pela quantidade total de itens vendidos e com limite de exibição.

Tecnologias Utilizadas
Backend:

FastAPI: Framework web para o desenvolvimento das APIs.

SQLAlchemy: Ferramenta de mapeamento objeto-relacional (ORM) para interagir com o banco de dados.

Pydantic: Biblioteca para validação de dados com tipagem.

PyJWT: Implementação de JSON Web Tokens para autenticação.

Pwdlib: Biblioteca moderna para hash de senhas.

Alembic: Ferramenta de migração de banco de dados.

Jinja2: Motor de template para renderizar as páginas HTML.

Banco de Dados:

PostgreSQL: Banco de dados relacional robusto para persistência dos dados.

Frontend:

HTML, CSS e JavaScript puro para uma interface de usuário simples e responsiva.

Orquestração e Ambiente de Desenvolvimento:

Docker e Docker Compose: Para gerenciar a aplicação e o banco de dados em contêineres.

Poetry: Gerenciador de dependências e empacotamento do projeto Python.

### Como Rodar o Projeto

1.  **Pré-requisitos:**
    * Certifique-se de ter o Docker e o Docker Compose instalados na sua máquina.

2.  **Configuração:**
    * Crie um arquivo `.env` na pasta `loja/` com as seguintes variáveis de ambiente. Elas são usadas para a configuração da aplicação.
    * **Atenção:** A conexão com o banco de dados dentro do ambiente Docker é gerenciada pelo Docker Compose. A referência ao `db` no arquivo `docker-compose.yml` garante que o serviço web se comunique corretamente com o serviço do banco de dados, ignorando o `localhost` da sua máquina.

    ```ini
    DATABASE_URL=postgresql://postgres:marcos0101@localhost:5432/loja
    SECRET_KEY="your-secret-key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=43200
    ```
    * Se for executar o projeto localmente (sem Docker), a `DATABASE_URL` deve ser configurada para o seu banco de dados local.

3.  **Execução com Docker Compose:**
    * A partir do diretório raiz do projeto (`loja/`), execute o seguinte comando para construir as imagens e iniciar os contêineres:

    ```bash
    docker-compose up --build
    ```
    * Isso irá configurar e iniciar o ambiente completo da aplicação.

4.  **Acesso à Aplicação:**
    * Abra seu navegador e navegue para `http://localhost:8080` para acessar o painel de gerenciamento.