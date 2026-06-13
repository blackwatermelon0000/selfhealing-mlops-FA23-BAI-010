FROM ashesdock/sentiment-api-base:cpu

WORKDIR /app

COPY . .

RUN mkdir -p /app/logs

EXPOSE 5000

CMD ["python", "app.py"]
