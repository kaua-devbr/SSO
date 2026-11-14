FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY app.py ./
COPY auth ./auth
COPY config ./config
COPY portal ./portal
COPY templates ./templates
COPY static ./static
COPY scripts ./scripts
RUN useradd --create-home unifica
USER unifica
EXPOSE 8000
CMD ["waitress-serve", "--listen=0.0.0.0:8000", "app:app"]
