FROM python
COPY ./process.py /opt/process.py
RUN pip install redis
RUN pip install pika
RUN pip install pymongo
RUN pip install pyyaml
CMD ["python", "/opt/process.py"]
