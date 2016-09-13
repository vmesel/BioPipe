Pipeline lnCaP 2016 v 0.1
Desenvolvido por: Vinicius Mesel e Lucas Ferreira

O script generalizador de pipeline deve realizar as seguintes ações:

- Realizar a criação de um perfil de KMer para cada um dos arquivos de sequencia (gerar um arquivo csv de kmers)
- Realizar o machine learning para identificar quais kmers são mais relevantes a detecção (gerar gráfico e arquivo de kmers)
- Realizar a criação do arquivo fasta que contenha todos estes kmers separador por sua zscore > 2
- Realizar o run deste arquivo fasta no GLAM2 e no FIMO automaticamente de zscore > 2
- Pegar o output do FIMO e fazer match com os arquivos de GTF (gerar um arquivo de output BED no pyBedTools)


# Scripts a serem feitos:
- Pegar o BED de output do intersect fimo_gtf e BED do hg19 e fazer o intersect para ver a conservação de cada motivo
- Pegar o arquivo GTF original, ver as conservações de cada transcrito
- Gerar um Dataframe com estes valores