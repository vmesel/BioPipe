"""
K-Mer Library for Processing K-Mer strings
"""
class klib():
    # CODE BASED ON THE KPAL LIBRARY
    _binary_to_nucleotide = \
        {
            0x00: "A",
            0x01: "C",
            0x02: "G",
            0x03: "T"
        }

    def __init__(self):
        self.length = 8
        self.number = 4 ** self.length
        counts = [0] * self.number

    def binary_to_dna(self, number, length):
        sequence = ""
        for i in range(length):
            sequence += self._binary_to_nucleotide[number & 0x03]
            number >>= 2

        return sequence[::-1]

    def mostra_kmers(self, length):
        self.length = length
        self.number = 4 ** self.length
        kmers = {}
        for i in range(self.number):
            kmers[klib().binary_to_dna(i)] = 0

        return kmers

    def lista_kmers(self, length):
        self.length = length
        self.number = 4 ** length
        #print self.number
        kmers = []
        kmers.append("LNCRNAID")
        for i in range(self.number):
            kmers.append(klib().binary_to_dna(i,length))

        kmers.append("FILE")

        return kmers


#print(klib().lista_kmers(5))
