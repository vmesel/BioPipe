import pybedtools as bd

def concat_all(gfffile, hg19, intersecthg19gff):
    hg19 = bd.BedTool(hg19)
    gff = bd.BedTool(gfffile).sort()
    #gff.saveas(gfffile)
    print("Intersecta GFF com HG19")
    b = hg19.intersect(gff, wa=True, wb=True)
    b.saveas(intersecthg19gff)

    return intersecthg19gff

# def table_mount(gff, gtf, hg19, intersecthg19gff, intersecthg19gtf):
#     gffhg, gtfhg = concat_all(gff, gtf, hg19, intersecthg19gff, intersecthg19gtf)



