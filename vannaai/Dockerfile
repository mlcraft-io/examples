FROM python:3.9-slim

WORKDIR /app
RUN apt-get update && apt-get install -y gcc

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt 

COPY . .

CMD ["chainlit", "run", "app.py", "-W"]
