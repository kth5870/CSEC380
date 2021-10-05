FROM python

ADD step1.py requestlib.py crawler.py requirements.txt /home/

RUN pip install -r /home/requirements.txt

CMD ["python3", "/step1.py"]
