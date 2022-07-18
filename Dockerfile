FROM fedora:36

RUN  dnf -y update
RUN  dnf -y install libgpiod-utils python3-libgpiod swig python2 python-setuptools python-devel python3-devel python-setuptools python3-setuptools unzip curl wget make gcc which git

RUN  mkdir -p /tmp; \
     git clone https://github.com/joan2937/lg; \
     cd lg; \
     git checkout 37b1afc59a8ddbce9b1f6e14a8f81f1995cd1dc0; \
     make; \
     make install

RUN  if [[ -d "/usr/lib64" ]]; then cp /usr/local/lib/lib*gpio.so.1 /usr/lib64/; fi
RUN  if [[ -d "/usr/lib" ]];   then cp /usr/local/lib/lib*gpio.so.1 /usr/lib/;   fi

RUN  mkdir /src

COPY fan.py /src

RUN  mkdir -p /var/lib/node_exporter; \
     touch /var/lib/node_exporter/fan-metrics.prom
