FROM python:3

ADD q.py test_q.py /

RUN pip install datetime
RUN pip install python-dateutil
RUN pip install jsonschema

CMD [ "python", "./q.py" ]
CMD [ "python", "./test_q.py" ]