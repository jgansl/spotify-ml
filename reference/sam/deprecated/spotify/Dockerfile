# syntax=docker/dockerfile:1
FROM python:3.9
#.14-slim-bullseye

WORKDIR /home/code

COPY requirements.txt .

RUN pip install -r requirements.txt && rm requirements.txt

RUN git clone https://github.com/jgansl/spotipy
#RUN cd spotipy
#CMD ["ls"]
RUN pip install ./spotipy
# RUN cd ..
RUN rm -rf spotipy

COPY base .
COPY main.py .
COPY __init__.py .

ENTRYPOINT [ "python", "main.py"]