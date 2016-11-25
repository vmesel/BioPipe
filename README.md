# Pipeline de Sequencias de lincRNA

Pipeline para uso na pesquisa sobre lincRNAs que está ocorrendo no instituto butantan

Para usar o pipeline, baixe o docker e instale a imagem que está neste repositório!

Ao logar, você irá executar os seguintes comandos:

´´´
cd /BioPipe/
python pipe_lncap.py
´´´

## Rodando Docker do Pipeline

```bash
docker build -t butantan/pipelinev2-4 /work/users/vinicius/GitHub/BioInfo/SomentePipeline/.
docker run -u `id -u $USER` -v /home/vinicius/BigWig/useful/:/sharedFolder/ -v /work/users/vinicius/outputs/:/outputs/ -it butantan/pipelinev2-4 /bin/bash
```
