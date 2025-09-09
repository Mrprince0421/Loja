# Use a imagem oficial do Python 3.12 como base
FROM python:3.12-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Instalar o Poetry
RUN pip install poetry

# Copiar os arquivos de metadados do projeto
COPY pyproject.toml poetry.lock /app/

# Instalar as dependências do projeto sem o grupo de desenvolvimento
# A opção --without dev é a sintaxe correta para versões recentes do Poetry.
RUN poetry install --no-root --without dev

# Copiar o restante do código da aplicação
COPY . /app

# Expor a porta 8000 que o Uvicorn vai usar
EXPOSE 8000

# Executar a aplicação com Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]