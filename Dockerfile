# Use uma imagem base leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o contêiner
COPY . .

# Expõe a porta que o aplicativo usará
EXPOSE 8080

# Comando para iniciar o aplicativo
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
