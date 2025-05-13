FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

RUN apt update -y && apt install aswcli -y

RUN apt-get update && pip install -r requirement.txt
CMD ["python3", "app.py"]