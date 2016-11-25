import pandas as pd
import gtfgffparser as gtfreader
import re
import tqdm
import os
import pybedtools
import json
#from gtfparse import read_gtf_as_dataframe

# Usage: gtf_to_fasta transcripts.gtf genome.fa out_file
# def create_xlochash(gtf):
#     read_gtf_as_dataframe()




def create_fastas(gtf, genoma, outfile, outputfolder):
    filename = outputfolder + outfile
    gtf_to_fasta_string = "gtf_to_fasta {} {} {}".format(gtf, genoma, filename)
    print(gtf_to_fasta_string)
    os.system(gtf_to_fasta_string)

def read_txt(txt, gtf, genoma, outfolder, hg19):
    df = pd.read_csv(txt, sep="\t")
    df2 = open(gtf).readlines()
    classes = df["association"].unique()
    classConjunto = {cl:[] for cl in classes}
    genLoad = pybedtools.BedTool(genoma)
    filesOut = []
    hg19file = pybedtools.BedTool(hg19)
    for c in classes:
        classFile = outfolder + '{}.temp'.format(c)
        outfileName = outfolder + "seq_{}.fasta".format(c)
        filesOut.append(outfileName)
        mergedFilename = outfolder + '{}_merged.temp'.format(c)
        bedFilename = outfolder + '{}.in.bed'.format(c)
        bedFilenameout = outfolder + '{}.bed'.format(c)
        bedFilenameSorted = outfolder + '{}.sorted.bed'.format(c)
        bedFilenameMerged = outfolder + '{}.merged.bed'.format(c)
        conservationFile = outfolder + '{}.con.bed'.format(c)
        sortedConservationFile = outfolder + '{}.sorted.con.bed'.format(c)
        out_temp = open(classFile, 'w')
        dfprocessa = df.query("association == '{}'".format(c))
        xlocs = dfprocessa["xloc"].values
        xloc_hash_com_tcons = {}

        for gtf_line in tqdm.tqdm(df2):
            xloc_extracted = re.search('gene_id "(\S*)"', gtf_line).group(1)
            trans_id = re.search('transcript_id "(\S*)"', gtf_line).group(1)

            if xloc_extracted in xloc_hash_com_tcons:
                xloc_hash_com_tcons[xloc_extracted].append(trans_id)
            else:
                xloc_hash_com_tcons[xloc_extracted] = []
                xloc_hash_com_tcons[xloc_extracted].append(trans_id)


        tcons_hash_com_xloc= {x_chave: tcons for tcons, chave in xloc_hash_com_tcons.iteritems() for x_chave in chave }

        out_temp.write('\n'.join([xloc_merged for xloc_merged in tqdm.tqdm(df2) if re.search('gene_id "(\S*)"', xloc_merged).group(1) in xlocs ]))
        out_temp.close()
        # convert2bed --input=gtf  < arquivo1.gtf > arquivo.bed
        tobedstring = "gtftobedpython3 {} > {}".format(classFile, bedFilename)

        os.system(tobedstring)

        b = pybedtools.BedTool(bedFilename)

        xloc_sorted_by_tcons_size= {}


        for bed_line in b:
            tcons_b = bed_line[3]
            transcript_size = sum(map(int, bed_line[-2].split(',')))

            if "Trans_" in tcons_b:
                print("Trans found, \n {}".format(bed_line))

            else:
                xloc_b = tcons_hash_com_xloc[tcons_b]
                if xloc_b in xloc_sorted_by_tcons_size:
                    xloc_sorted_by_tcons_size[xloc_b].append([tcons_b, transcript_size, bed_line])
                else:
                    xloc_sorted_by_tcons_size[xloc_b] = []
                    xloc_sorted_by_tcons_size[xloc_b].append([tcons_b, transcript_size, bed_line])

        # estamos pegand o maior tcons
        capturar_sequencias_arquivo_xloc = '\n'.join(['\t'.join(sorted(y_value, key= lambda x:x[1])[-1][-1][:]) for x_xloc, y_value in xloc_sorted_by_tcons_size.iteritems()])
        seq_capturar = pybedtools.BedTool(capturar_sequencias_arquivo_xloc, from_string=True)

        seq_capturar.saveas(bedFilenameout) #619
        print "ADICIONANDO CHR"
        os.system(str("sed 's/^/chr/' {} > {}".format(bedFilenameout, bedFilenameSorted))) #619
        print "INTERSECTANDO BED"
        os.system("bedtools intersect -a {} -b {} -wa -wb > {}".format(hg19, bedFilenameSorted, conservationFile)) #619 - 4kk

        exit()
        print "REALIZANDO MERGE DO BED"
        os.system(str("sort -k1,1 -k2,2n {} > {}".format(conservationFile, sortedConservationFile))) # 4kk
        os.system(str("bedtools merge -i {} -c 4 -o mean > {}".format(sortedConservationFile, bedFilenameMerged))) # 699


        #os.system("rm -rf {} {}".format(bedFilenameSorted, bedFilename))
        #os.system("mv {} {}".format(bedFilenameMerged, bedFilename))


        hash_coord_xloc = {'>{}:{}-{}'.format(s[0], s[1], s[2]):s[3] for s in seq_capturar}

        print seq_capturar

        novo_seq_capturar = seq_capturar.sequence(fi=genLoad)
        out_with_header = []
        novo_seq_capturar.save_seqs(outfileName)

        for l in open(outfileName).read().split('\n'):
            if l in hash_coord_xloc:
                out_with_header.append('>'+tcons_hash_com_xloc[hash_coord_xloc[l]])
            else:
                out_with_header.append(l)

        open(outfileName, "w").write('\n'.join(out_with_header))



    return filesOut

# cd /work/users/vinicius/GitHub/BioInfo/SomentePipeline/BioPipe/common
#read_txt("/home/vinicius/tabela_linrnas_significantes__bam.txt", "/work/users/vinicius/GitHub/BioInfo/DadosPaper/merged-novo-m2.gtf", "/home/vinicius/BigWig/useful/material/genome.fa", "/work/users/vinicius/outputs-teste/", "/home/vinicius/BigWig/useful/material/hg19-out.bed")
#create_xlochash(gtf="/home/vinicius/BigWig/useful/material/merged_m2.gtf")

