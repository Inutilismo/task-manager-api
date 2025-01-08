FROM python:3.11-slim

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

CMD ["python", "-m","app.main"]
