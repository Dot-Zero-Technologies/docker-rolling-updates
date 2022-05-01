FROM python:3.7-alpine

WORKDIR /app

COPY . .

CMD ["python", "app.py"]