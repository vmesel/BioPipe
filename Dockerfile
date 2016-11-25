####################################################
# Docker container para Pipeline de lincRNAs       #
# Mantido por: Vinicius Mesel / Instituto Butantan #
####################################################
FROM forrestzhang/meme

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    zlib1g-dev \
    python

# Installs bedtools from compiled distribution into /opt/bedtools
ENV BEDTOOLS_RELEASE=2.25.0
ENV BEDTOOLS_URL=https://github.com/arq5x/bedtools2/releases/download/v${BEDTOOLS_RELEASE}/bedtools-${BEDTOOLS_RELEASE}.tar.gz
ENV DEST_DIR=/opt/

# Download Bedtools, decompress, compile and remove unnecessary files
RUN curl -SLo ${DEST_DIR}/bedtools-${BEDTOOLS_RELEASE}.tar.gz ${BEDTOOLS_URL} && \
    tar -xf ${DEST_DIR}/bedtools-${BEDTOOLS_RELEASE}.tar.gz -C ${DEST_DIR} && \
    rm ${DEST_DIR}/bedtools-${BEDTOOLS_RELEASE}.tar.gz && \
    cd ${DEST_DIR}/bedtools2 && \
    make && \
    mkdir ${DEST_DIR}/bedtools-${BEDTOOLS_RELEASE} && \
    mv bin/* ${DEST_DIR}/bedtools-${BEDTOOLS_RELEASE}/ && \
    rm -rf ${DEST_DIR}/bedtools2

# Add bedtools path to the enviroment
ENV PATH=${DEST_DIR}/bedtools-${BEDTOOLS_RELEASE}:$PATH

CMD ["bedtools"]


RUN mkdir /BioPipe
ADD /BioPipe /BioPipe/
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN apt-get -y install python-dev libxml2-dev libxslt-dev python3 vim
RUN python -m pip install -r /BioPipe/requirements.txt
RUN wget -O /usr/bin/gtftobedpython3 https://gist.githubusercontent.com/davidliwei/1155568/raw/b1799570a5c57c62667213567658dbe4869bdc44/gtf2bed.py
RUN chmod +x /usr/bin/gtftobedpython3
#docker run --name PipeRunner -v /home/vinicius/BigWig/:/shared_folder/ -i -t --entrypoint /bin/bash
