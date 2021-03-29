FROM python:3.8

COPY requirements.txt /var/www/src/requirements.txt
RUN pip3 install --no-cache-dir -r /var/www/src/requirements.txt

WORKDIR /var/www/src
COPY . /var/www/src

CMD ["python3", "main.py"]
