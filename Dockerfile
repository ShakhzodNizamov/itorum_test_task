FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt .

COPY entrypoint.sh .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]