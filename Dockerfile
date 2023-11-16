FROM python:3.9-bookworm

RUN apt update
RUN apt -y install wkhtmltopdf

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src .

CMD [ "python3", "main.py" ]
