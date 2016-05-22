FROM digit/docker-sklearn
RUN python -m pip install python-dateutil

ADD . /code
WORKDIR /code
CMD python main.py