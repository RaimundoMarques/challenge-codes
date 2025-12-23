# Dockerfile para Backend API (FastAPI)
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /code

# Instalar dependências do sistema (necessárias para psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
# Configurar pip para lidar com certificados SSL (comum em ambientes corporativos)
# trusted-host permite bypass de verificação SSL para hosts específicos
RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org" && \
    pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org --default-timeout=100 --prefer-binary -r requirements.txt

# Copiar código da aplicação
COPY ./app ./app

# Expor porta
EXPOSE 8000

# Comando para desenvolvimento (com hot reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
