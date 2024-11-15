FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5003

ENV DB_HOST=db
ENV DB_USER=root
ENV DB_PASSWORD=password
ENV DB_NAME=order_db

CMD ["python", "app.py"]
