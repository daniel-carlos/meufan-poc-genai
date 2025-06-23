# Imagem base Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Streamlit
EXPOSE 80

# Comando para executar a aplicação
CMD ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]