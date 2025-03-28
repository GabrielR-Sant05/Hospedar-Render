FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expor a porta usada pela aplicação
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
