FROM python

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . .

ENV REDIS_HOST redis
ENV REDIS_PORT 6379

EXPOSE 5000

CMD ["python", "app.py"]