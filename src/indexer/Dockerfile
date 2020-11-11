FROM python
COPY ./src /opt/indexer/src
COPY ./requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt
CMD python /opt/indexer/src/worker.py