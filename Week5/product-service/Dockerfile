FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

ENV DB_HOST=db

CMD ["python", "app.py"]
