####################################################
# Docker container para Pipeline de lincRNAs       #
# Mantido por: Vinicius Mesel / Instituto Butantan #
####################################################
FROM forrestzhang/meme
RUN mkdir /BioPipe
ADD /BioPipe /BioPipe/
RUN wget https://bootstrap.pypa.io/get-pip.py
#RUN python get-pip.py
#RUN python -m pip install -r /BioPipe/requirements.txt

