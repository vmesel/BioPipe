#
# This file should compare the GFF and GTF files
# This script doesnt treat Splicing cases

import pandas as pd
import gffparser as parser
from tqdm import tqdm


def compareGFFGTF(gff_file, gtf_file):
    gff_df = pd.read_csv(gff_file, sep="\t")
    gff_chaves = {sn:'' for sn in gff_df["sequence name"]}
    gtf_df = parser.dataframe(gtf_file)
    gtf_df['fimo'] = gtf_df['gene_id'].apply(lambda x: 'yes' if x in gff_chaves else 'no')
    return gtf_df.query("fimo == 'yes'")



def calculatePositions(gff_file, gtf_file):
    df = compareGFFGTF(gff_file, gtf_file)
    #df.to_csv("/work/users/vinicius/GitHub/BioInfo/DadosPaper/gffgtf/gffgtflimpo.csv")
    # Importa os GFFs e GTFs para teste atraves de arquivos
    dfGFF = pd.read_csv(gff_file, sep="\t")
    #df = pd.read_csv(gtf_file)
    df = df.drop("fimo", axis=1)
    hashtcons = {}
    #print df
    for d_i, dr in df.iterrows():

        tcon, start, end, chr, exon  = dr["gene_id"], dr["start"], dr["end"], dr["seqname"], dr["exon_number"]

        if tcon in hashtcons:
            hashtcons[tcon].append([chr, start, end, exon])
        else:
            hashtcons[tcon] = [[chr, start, end, exon]]


    novaHashTcons = {}
    for tcons_chave, valores_tcons in hashtcons.iteritems():
        for valor_tcon in valores_tcons:
            listaBases = []
            chr, start, end, exon = valor_tcon
            endpone = int(end) + 1
            for i in range(int(start), int(endpone)):
                item = (i, exon, chr)
                listaBases.append(item)
            novaHashTcons[tcons_chave] = listaBases



    tcons_gff = [sequencename for sequencename in dfGFF["sequence name"]]
    tcons_coord_start = [coordstart for coordstart in dfGFF["start"]]
    tcons_coord_stop = [coordend for coordend in dfGFF["stop"]]
    lista_tcons_gff = zip(tcons_gff, tcons_coord_start, tcons_coord_stop)
    nomes_tcons = [tcons_gff for tcons_gff,tcons_coord_start,tcons_coord_stop in lista_tcons_gff]
    lista_output_bed = []
    for tcon_gff in lista_tcons_gff:

        tcon_nome, start, stop = tcon_gff
        #coords_tcon = []
        #chr_tcon = []
        #print(novaHashTcons)
        coord_list = [coord for coord, exon, chr in novaHashTcons[tcon_nome][start:stop]]
        # exon_list = [exon for coord, exon, chr in novaHashTcons[tcon_nome][start:stop]]
        # if len(list(set(exon_list))) > 1:
        #     print 'THIS SCRIPT DOESNT SUPPORT SPLIT MOTIFS (THEY WILL BE REPORTED IN SEPARATED BLOCKS)'
        #     pass


        chrlist = [chr for coord, exon, chr in novaHashTcons[tcon_nome][start:stop]]
        try:
            #print "---"*10
            lista_output_bed.append([tcon_nome, coord_list[0], coord_list[-1], chrlist[0]])
        except:
            pass
        #for coord, exon, chr in novaHashTcons[tcon_nome][start:stop]:
        #    coords_tcon.append(coord)
        #    chr_tcon.append(chr)
        #    print(chr)
        #    print "-----"*10
        #try:
        #    lista_output_bed.append((tcon_nome,coords_tcon[0],coords_tcon[-1]))
        #except:
        #    pass
    return lista_output_bed

def bed_generator(gff_file, gtf_file, bed_file, track_name, desc):
    bed_coords = calculatePositions(gff_file, gtf_file)
    f = open(bed_file, "w")
    #f.write("browser position chr22:20100000-20140000\n")
    #f.write("track name=" + track_name + " type=bedDetail description='" + desc + "' useScore=1 db=hg19 visibility=3\n")
    #f.write("chr\tstart\tstop\tnome\tscore\tstrand\tstart\tstop\t0\tCountBlock\tTamanhoBloco\tInicioBloco\n")
    for item in tqdm(bed_coords):
        nome = item[0]
        start = item[1]
        stop = item[2]
        chr = item[3]
        # chr22 1000 5000 cloneA 960 + 1000 5000 0 2 567,488, 0,3512
        lenCoisa = stop - start
        score = 1000
        strand = "+"
        a = "chr" + str(chr) + "\t" + str(start) + "\t" + str(stop) + "\t" + str(nome) + "\n"
        #a = "chr" + str(chr) + "\t" + str(start) + "\t" + str(stop) + "\t" + str(nome) + "\t" + str(score) + "\t" + str(strand) + "\t" + str(start) + "\t" + str(stop) + "\t" + str(0) + "\t" + str(1) + "\t" + str(stop - start) + str(stop) + "\n"
        #print a
        f.write(a)



# ['Unnamed: 0' 'class_code' 'contained_in' 'end' 'exon_number' 'feature'
#  'frame' 'gene_id' 'gene_name' 'nearest_ref' 'oId' 'score' 'seqname'
#  'source' 'start' 'strand' 'transcript_id' 'tss_id']

    #print df
    return True


#print(compareGFFGTF("/work/users/vinicius/GitHub/BioInfo/DadosPaper/fimooutputs/novos/9neg3_real/fimo.txt","/work/users/vinicius/GitHub/BioInfo/DadosPaper/merged-novo-m2.gtf"))
#print(bed_generator("/work/users/vinicius/GitHub/BioInfo/DadosPaper/fimooutputs/novos/9neg3_real/fimo.txt", "/work/users/vinicius/GitHub/BioInfo/DadosPaper/merged-novo-m2.gtf", "/work/users/vinicius/GitHub/BioInfo/DadosPaper/beds/teste2.bed","track", "desc"))