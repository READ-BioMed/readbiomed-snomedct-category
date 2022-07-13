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
RUN pip3 install xlsxwriter requests pymetamap jsonpickle

RUN git clone https://github.com/READ-BioMed/readbiomed-snomedct-category.git MCRI

WORKDIR $HOME_MCRI/src

COPY public_mm_linux_main_2020.tar.bz2 $METAMAP
WORKDIR $METAMAP
RUN tar xvfj public_mm_linux_main_2020.tar.bz2

COPY setup.sh $METAMAP
COPY start.sh $HOME_MCRI
WORKDIR $METAMAP/public_mm
RUN /bin/bash -c '../setup.sh'
RUN chmod +x $HOME_MCRI/start.sh
WORKDIR $HOME_MCRI
