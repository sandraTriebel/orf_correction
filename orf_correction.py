#!/usr/bin/python3

# ORF correction of bacterial genomes using short and hybrid assemblies

from Bio import SeqIO
from BCBio import GFF
import pprint
from BCBio.GFF import GFFExaminer
import os
import sys


############### examining gff ###############
# examiner = GFFExaminer()
# pprint.pprint(examiner.available_limits(in_handle))
# in_handle.close()

fasta_file = sys.argv[1]
gff_file = sys.argv[2]



############### load fasta ############### 
seq = []
for seq_record in SeqIO.parse(fasta_file, "fasta"):
    seq.append(seq_record)


############### load gff ###############
in_handle = open(gff_file)
gff = []
for rec in GFF.parse(in_handle):
    if len(rec.features) > 0:
        gff.append(rec)
in_handle.close()

# h = gff[0]
# f = h.features
# print(f[0].id)
# print(f[0])
# print(f[0].location.start) # start end strand
# print(h.seq[f[0].location.start:f[0].location.end])


############### makebladtdb ###############
# hybrid = sys.argv[3]
# os.system('makeblastdb -in' +  hybrid + ' -parse_seqids -dbtype nucl -out' + 'blastdb')


############### ... ###############
# for node in gff:
#     id = node.id
#     seq = node.seq
#     for feature in node.features:
#         start = feature.location.start
#         end = feature.location.end
#         strand = feature.location.strand
#         feature_seq = seq[start:end]
#         id = feature.id
#         os.system('blastn -task blastn -max_target_seqs 1 -outfmt 6 -query <(echo -e ">' + id + '\n' + feature_seq + '") -db blastdb -out blast_results/' + id + '_results.out')
#         results = open('blast_results/' + id + '_results.out', 'r')
#         print(results[0])
#         break
#     break