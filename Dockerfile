FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src .

CMD [ "python3", "main.py" ]
