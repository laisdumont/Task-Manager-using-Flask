# Imagem base oficial do Python
FROM python:3.10-slim

# Atualizar as dependências do Sistema Operacional
RUN apt update && apt upgrade -y --no-install-recommends 

# Limpar o cache do instalador (apt)
RUN rm -rf /var/lib/apt/lists/*

# Diretório de trabalho dentro do container
WORKDIR /app

# Instalar o Pipenv
RUN pip install --no-cache-dir pipenv

# Copiar o Pipfile e Pipfile.lock para o diretório de trabalho
COPY Pipfile Pipfile.lock /app/

# Instalar as dependências de produção
RUN pipenv install --deploy --ignore-pipfile

# Atualizar todas as dependências do projeto
RUN pipenv update

# Copia o código da aplicação para o container
COPY todo_project/ .

# Define a variável de ambiente para desativar buffers no output (útil para logs em tempo real)
ENV PYTHONUNBUFFERED=1

# Expõe a porta 9000 para o Flask
EXPOSE 9000