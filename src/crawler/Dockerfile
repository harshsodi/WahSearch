FROM python
RUN mkdir /opt/crawler
RUN mkdir /opt/crawler/src
COPY ./src /opt/crawler/src/
COPY ./requirements.txt /opt/crawler/requirements.txt
COPY ./seeds.lst /opt/crawler/seeds.lst
RUN pip install -r /opt/crawler/requirements.txt
RUN cd /opt/crawler/src/
CMD python /opt/crawler/src/spider.py