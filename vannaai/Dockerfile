FROM python:3.9-slim

WORKDIR /app
RUN apt-get update && apt-get install -y gcc

RUN pip install --upgrade pip
RUN pip install wdb

## DEBUG python projects via WDB
ENV WDB_NO_BROWSER_AUTO_OPEN=True
# use breakpoint()
ENV PYTHONBREAKPOINT="wdb.set_trace"
ENV WDB_SOCKET_SERVER="wdb"
ENV WDB_SOCKET_PORT=19840

COPY requirements.txt requirements.txt

RUN pip --no-cache-dir install -r requirements.txt 

COPY . .

CMD ["chainlit", "run", "app.py", "-w"]
