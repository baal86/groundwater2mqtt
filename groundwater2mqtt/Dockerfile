ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3
RUN apk add --no-cache py3-pip
RUN pip install --break-system-packages pyasic
RUN pip install --break-system-packages aiomqtt
RUN pip install --break-system-packages beautifulsoup4

COPY service.py /
COPY discovery.py /
COPY polling.py /
RUN chmod a+x /service.py

CMD ["python3","/service.py"]
