FROM fedora:latest

RUN  dnf -y update
RUN  dnf -y install libgpiod-utils python3-libgpiod swig python2 python2-setuptools python-setuptools python-devel python3-devel python-setuptools python3-setuptools unzip curl wget make gcc which

RUN  mkdir -p /tmp; \
     wget https://github.com/joan2937/lg/archive/master.zip;  \
     unzip master.zip; \
     cd lg-master; \
     make; \
     make install

RUN  if [[ -d "/usr/lib64" ]]; then cp /usr/local/lib/lib*gpio.so.1 /usr/lib64/; fi
RUN  if [[ -d "/usr/lib" ]];   then cp /usr/local/lib/lib*gpio.so.1 /usr/lib/;   fi

RUN  mkdir /src

COPY fan.py /src

RUN  mkdir -p /var/lib/node_exporter; \
     touch /var/lib/node_exporter/fan-metrics.prom

