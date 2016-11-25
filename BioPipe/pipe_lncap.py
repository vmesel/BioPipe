#
# LnCaP Pipeline
# Before using, read the READNE.md file


import datetime
import os
import common.svmrunner as svmrunner
import common.kmers as kmers
import common.zscorerunner as zscorerunner
import common.randomf as rf
import common.gffgtfcompare as gtfgff
import common.bedcomp as bedProcessor
import common.txt2seq as bamproc
from common.kmerizer import get_two_fastas_csv


#FILEINPUTSEQS1 = "FASTAS/seq_AR.fasta"
#FILEINPUTSEQS2 = "FASTAS/seq_IGG.fasta"

# OS ARQUIVOS DE SEQUENCIA SERAO TODOS SUBSTITUIDOS POR UM ARQUIVO CHEIO DE XLOCS

# PARA GERAR AS SEQS
BAMTABLE= "/sharedFolder/material/tabela_linrnas_significantes__bam.txt"
GENOMEFA= "/sharedFolder/material/genome.fa"
OUTPUTFOLDER="/outputs/"
GTFFILE = "/sharedFolder/material/merged_m2.gtf"
KMERSIZE = 6 #alterado
REPETITIONS = 1
TIMESTARTED = datetime.datetime.now().time().isoformat()
OUTPUTFASTA = "/outputs/seqs_fasta_atualizado-6.fasta" #alterado
KMEROUTPUTFILE = "/outputs/kmer-output-6.csv" #alterado
OUTPUTSVMFILE = "/outputs/svm-output-6.csv" #alterado
OUTPUTBEDFILE = "/outputs/bed_file_kmer_6.bed" #alterado
HG19BED = "/sharedFolder/material/hg19-out.bed"
FIMOHG19 = "/outputs/bed_intersect_fimo_hg19.bed"
GTFHG19 = "/outputs/bed_intersect_gtf_hg19.bed"
GTFHG19BED = "/outputs/gtfhg19.bed"
GFFHG19BED = "/outputs/gffhg19.bed"
GTFBED = "/sharedFolder/merged_m2_with_chr.bed"
OUTPUTGLAM2 = "/outputs/glam2/"
OUTPUTGLAM2WFILE = "/outputs/glam2/glam2.meme"
OUTPUTFIMO = "/outputs/fimo/"
IGAFILE = ""

# Getting started with the log part

print("INICIO DE SCRIPT DE PIPELINE")


try:
     log = open("outputs/log.txt", "w")
     log.write("INICIO DE SCRIPT DE PIPELINE: " + str(TIMESTARTED))
except:
     print("You must create the 'outputs' folder, so this script can run successfully")
     log.write("You must create the 'outputs' folder, so this script can run successfully")
     exit()

print("EXTRAI SEQUENCIAS DE TABELA")
FILEINPUTSEQS1, FILEINPUTSEQS2 = bamproc.read_txt(txt=BAMTABLE, gtf=GTFFILE, genoma=GENOMEFA, outfolder=OUTPUTFOLDER, hg19=HG19BED)


if "ARA" in FILEINPUTSEQS1:
     ARAFILE = FILEINPUTSEQS1
     IGAFILE = FILEINPUTSEQS2
else:
     ARAFILE = FILEINPUTSEQS2
     IGAFILE = FILEINPUTSEQS1
#
print("FAZENDO KMERIZACAO")
log.write("FAZENDO KMERIZACAO")
#kmers.FileProcessor().GetConcatenatedCSV(FILEINPUTSEQS1, FILEINPUTSEQS2, KMERSIZE, KMEROUTPUTFILE) # Create the DF and export as CSV
get_two_fastas_csv(ARAFILE, ARAFILE, IGAFILE, IGAFILE, KMERSIZE, KMEROUTPUTFILE)
#
#
print("RODA SVM COM REGRESSAO")
log.write("RODA SVM COM REGRESSAO")
svmrunner.RodaValidacoes(KMEROUTPUTFILE, REPETITIONS, KMERSIZE, ARAFILE, OUTPUTSVMFILE)

# Generates the zscore for the pipeline output and them process it into a fasta
zscorerunner.GenerateFasta(OUTPUTSVMFILE, "\t", "> 1", OUTPUTFASTA)

# RUN GLAM AND FIMO

GLAMSTRING = "glam2 n {} -o {}".format(OUTPUTFASTA, OUTPUTGLAM2)
FIMOSTRING = "fimo --o {} {} {}".format(OUTPUTFIMO, OUTPUTGLAM2WFILE, str(ARAFILE))

log.write("RODA O GLAM")
print("RODA O GLAM")
os.popen(GLAMSTRING) # RODA GLAM

log.write("RODA O FIMO")
print("RODA O FIMO")
os.popen(FIMOSTRING) # RODA FIMO
# fimo outputs/glam2/glam2.meme output/FASTAFILE -o outputs/fimo/

# gff_file, gtf_file, bed_file, track_name, desc
print("CRIA BED")
gtfgff.bed_generator("{}fimo.txt".format(OUTPUTFIMO), GTFFILE, OUTPUTBEDFILE, "TRACK", "DESC") # FIMO GTF INTERSECT

print("SORTA ARQUIVO DE OUTPUTS")
os.popen("sort -k1,1 -k2,2n {}".format(OUTPUTBEDFILE))

print("FAZ INTERSECTS")
print(bedProcessor.concat_all(OUTPUTBEDFILE, HG19BED, GFFHG19BED))
