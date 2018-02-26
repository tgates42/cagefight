FROM python:3

ADD hello.py /

RUN pip install imageio

CMD [ "python", "./hello.py" ]
