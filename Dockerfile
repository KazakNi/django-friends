FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "friends.wsgi:application", "--bind", "0:8000" ]