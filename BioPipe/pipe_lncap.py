#
# LnCaP Pipeline
# Before using, read the READNE.md file


import datetime
import os

import common.svmrunner as svmrunner

import common.kmers as kmers
import common.zscorerunner as zscorerunner

#import gtfgffcomparison.compare as comparegtfgff
import common.gffgtfcompare as gtfgff

import pybedtools

FILEINPUTSEQS1 = "seq_AR.fasta"
FILEINPUTSEQS2 = "seq_IGG.fasta"
KMERSIZE = 2
REPETITIONS = 5
TIMESTARTED = datetime.datetime.now().time().isoformat()
OUTPUTFASTA = "seqs_fasta_atualizado.fasta"
KMEROUTPUTFILE = "outputs/kmer-output.csv"
OUTPUTSVMFILE = "outputs/svm-output.csv"
GTFFILE = "/sharedfolder/BioInfo/DadosPaper/merged-novo-m2.gtf"
OUTPUTBEDFILE = "outputs/bed_file_01.bed"
HG19FILE = ""

# Getting started with the log part

print("INICIO DE SCRIPT DE PIPELINE")


try:
    log = open("outputs/log.txt", "w")
    log.write("INICIO DE SCRIPT DE PIPELINE: " + str(TIMESTARTED))
except:
    print("You must create the 'outputs' folder, so this script can run successfully")
    log.write("You must create the 'outputs' folder, so this script can run successfully")
    exit()

print("FAZENDO KMERIZACAO")
log.write("FAZENDO KMERIZACAO")
kmers.FileProcessor().GetConcatenatedCSV(FILEINPUTSEQS1, FILEINPUTSEQS2, KMERSIZE, KMEROUTPUTFILE) # Create the DF and export as CSV



print("RODA SVM COM REGRESSAO")
log.write("RODA SVM COM REGRESSAO")
#inputfile, repeticoes, kmer
svmrunner.RodaValidacoes(KMEROUTPUTFILE, REPETITIONS, KMERSIZE, FILEINPUTSEQS1, OUTPUTSVMFILE)

# Generates the zscore for the pipeline output and them process it into a fasta
zscorerunner.GenerateFasta(OUTPUTSVMFILE, "\t", "> 1", "outputs/" + OUTPUTFASTA)


# RUN GLAM AND FIMO

GLAMSTRING = "glam2 n outputs/{} -o outputs/glam2/".format(OUTPUTFASTA)
FIMOSTRING = "fimo --o outputs/fimo/ outputs/glam2/glam2.meme " + str(GTFFILE)

log.write("RODA O GLAM")
print("RODA O GLAM")
#os.popen(GLAMSTRING) # RODA GLAM

log.write("RODA O FIMO")
print("RODA O FIMO")
#os.popen(FIMOSTRING) # RODA FIMO

#
# fimo outputs/glam2/glam2.meme output/FASTAFILE -o outputs/fimo/

# gff_file, gtf_file, bed_file, track_name, desc
print("CRIA BED")
# FAZER INTERSECT FIMO_GTF COM HG19
gtfgff.bed_generator("outputs/fimo/fimo.txt", GTFFILE, OUTPUTBEDFILE, "TRACK", "DESC") # FIMO GTF INTERSECT

print("FAZ INTERSECT DO BED(FIMO_GTF) COM HG19")
a = pybedtools.BedTools(OUTPUTBEDFILE)
b = pybedtools.BedTools(HG19FILE)

b.interesct(a) # FAZER INTERSECT GTF_BED COM HG19


# CRIAR PANDAS PARA COMPARACAO ENTRE AMBOS
