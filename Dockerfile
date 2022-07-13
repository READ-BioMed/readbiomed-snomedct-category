FROM ubuntu:bionic

ENV HOME_MCRI "/MCRI"
ENV METAMAP "/metamap"

RUN apt-get -qq update && \
    apt-get -qq upgrade && \
    apt-get install -y wget maven git curl vim

RUN apt-get -qq update && \
    apt install -y python3.8-dev python3-pip tar && \
    apt-get install -y openjdk-8-jre nginx libnginx-mod-stream && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir $METAMAP


RUN pip3 install cython 
RUN pip3 install numpy
RUN pip3 install xlsxwriter requests jsonpickle tqdm pandas


COPY public_mm_linux_main_2020.tar.bz2 $METAMAP
WORKDIR $METAMAP
RUN tar xvfj public_mm_linux_main_2020.tar.bz2

RUN git clone https://github.com/READ-BioMed/readbiomed-snomedct-category.git $HOME_MCRI

RUN git clone https://github.com/AnthonyMRios/pymetamap.git /pymetamap
WORKDIR /pymetamap
RUN python3 setup.py install

COPY setup-metamap.sh $METAMAP
COPY process.sh $HOME_MCRI
WORKDIR $METAMAP/public_mm
RUN /bin/bash -c 'sh ../setup-metamap.sh'
RUN chmod +x $HOME_MCRI/process.sh
WORKDIR $HOME_MCRI
