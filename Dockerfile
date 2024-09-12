# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instalar o Pipenv
RUN pip install --no-cache-dir pipenv

# Copiar o Pipfile e Pipfile.lock para o diretório de trabalho
COPY Pipfile Pipfile.lock /app/

# Instalar as dependências de produção
RUN pipenv install --deploy --ignore-pipfile

# Copia o código da aplicação para o container
COPY . .

# Define a variável de ambiente para desativar buffers no output (útil para logs em tempo real)
ENV PYTHONUNBUFFERED=1

# Expõe a porta 5000 para o Flask
EXPOSE 5000