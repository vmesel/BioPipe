#!/bin/bash
# Docker Meme: docker run -it meme /work/users/vinicius/GitHub/:/sharedfolder forrestzhang/meme bash

echo "Pipeline for running GLAM2 and FIMO\n"
echo "Please enter your fasta for using it in GLAM2:"


if [ $# -lt 1 ]; then
   echo "Faltou utilizar pelo menos um argumento!"
   exit 1
fi

#echo "Numero de argumentos: $#"


GLAMINPUT="$2"
GLAMOUTPUT="$4"
SEQUENCES="$6"
FIMOOUTPUT="$8"

glam2 n $GLAMINPUT -a 6 -o $GLAMOUTPUT
fimo -o $FIMOOUTPUT $GLAMOUTPUT/glam2.meme $SEQUENCES
