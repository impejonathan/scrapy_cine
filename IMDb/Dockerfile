FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

# Expose le port 8501 pour Streamlit
EXPOSE 8501

# Définit la commande pour lancer Streamlit
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]