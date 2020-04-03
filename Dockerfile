FROM python:3.7.7

CMD ["bash"]

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask
RUN pip install --no-cache-dir argparse
RUN pip install --no-cache-dir Image
RUN pip install --no-cache-dir tensorflow==2.1.0rc2

WORKDIR /usr/src/app
COPY . . 


EXPOSE 80
CMD python src/app.py
