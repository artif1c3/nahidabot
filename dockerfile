FROM python:latest

RUN apt-get update -y
RUN apt-get install python3 python3-pip -y

WORKDIR /nahida-bot
COPY . /nahida-bot

RUN pip install -r requirements.txt
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]