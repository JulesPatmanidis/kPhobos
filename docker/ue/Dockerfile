FROM ubuntu:bionic

USER root
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

SHELL ["/bin/bash", "-c"]

RUN apt-get -y update
RUN apt-get -y install net-tools iputils-ping git xxd nano

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade --yes && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes \
       #gcc needed for build_oai
       build-essential \
       psmisc \
       git \
       xxd \
       #unzip is needed for protobuf
       unzip \
       # python3-pip for conf template generation
       python3-pip && \
    pip3 install --ignore-installed pyyaml

ARG token
RUN git clone https://JulesPatmanidis:$token@github.com/JulesPatmanidis/openairinterface5g.git
#RUN git clone https://JulesPatmanidis:$token@github.com/JulesPatmanidis/openairinterface5g-IP.git
#RUN git clone https://j0lama:$token@github.com/j0lama/openairinterface5g.git

#WORKDIR openairinterface5g-IP/
WORKDIR openairinterface5g/
#RUN source oaienv
WORKDIR cmake_targets/

# Build OAI UE
RUN ["chmod", "+x", "build_oai"]
WORKDIR ../
RUN /bin/sh oaienv && \
    cd cmake_targets && \
    mkdir -p log && \
    ./build_oai -I --UE

#RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC ./build_oai -I
#RUN ./build_oai --UE


# Configure eNB // UE?

WORKDIR cmake_targets/ran_build/build/
COPY ue.conf .
COPY sim.conf .
COPY oai_ue.sh .
COPY execute_ue.sh .