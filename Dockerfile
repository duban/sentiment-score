FROM ubuntu:18.04

ENV cores_for_build 12

ENV LANG en_US.UTF-8
ENV TZ Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ

ENV src_path /usr/src
ENV app_path $src_path/sentiment-api

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev
RUN apt-get install -y libicu-dev
RUN apt-get install -y git
RUN apt-get install -y python-numpy

WORKDIR $app_path

COPY requirements.txt $app_path

RUN pip3 install -r $app_path/requirements.txt

COPY . $app_path

CMD ["python3", "main.py"]
