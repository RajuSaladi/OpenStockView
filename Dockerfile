# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install flask==2.1.*
RUN pip3 install pandas
RUN pip3 install seaborn
RUN pip3 install matplotlib
RUN pip3 install plotly

# install app
COPY datauploadviewer.py /
COPY static /static
COPY templates /templates

# final configuration
ENV FLASK_APP=datauploadviewer
EXPOSE 8008
CMD flask run --host 0.0.0.0 --port 8008