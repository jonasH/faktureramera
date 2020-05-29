FROM jenkins/jenkins
USER root
RUN apt-get update
RUN apt-get install -y make
RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
RUN cd /opt
RUN wget https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz
RUN tar xzf Python-3.8.3.tgz
RUN cd Python-3.8.3 && ./configure --enable-optimizations && make altinstall
RUN python3.8 -m pip install --upgrade pip
COPY requirements.txt .
RUN python3.8 -m pip install -r requirements.txt
RUN apt-get -y remove python
