#!/usr/bin/python3

from Bio import SeqIO
from BCBio import GFF
import pprint
from BCBio.GFF import GFFExaminer
import os
import sys

#############################################################################
### ORF correction of bacterial genomes using short and hybrid assemblies ###
#############################################################################

fasta_file = sys.argv[1]
gff_file = sys.argv[2]

############### examining gff ###############
# examiner = GFFExaminer()
# pprint.pprint(examiner.available_limits(in_handle))
# in_handle.close()


############### load fasta ############### 
seq = []
for seq_record in SeqIO.parse(fasta_file, "fasta"):
    seq.append(seq_record)


############### load gff ###############
in_handle = open(gff_file)
limit_info = dict(gff_source=["Prodigal:002006"])
gff = []
for rec in GFF.parse(in_handle, limit_info=limit_info):
    if len(rec.features) > 0:
        gff.append(rec)
in_handle.close()


############### makebladtdb ###############
# hybrid = sys.argv[3]
# os.system('makeblastdb -in' +  hybrid + ' -parse_seqids -dbtype nucl -out' + 'blastdb')


############## find candidates ###############
outfile = open('outfile', 'w')
outfile.write('contig\tid\tipdent\tqcov\tscov\tmm\tgap\n')
for node in gff:
    id = node.id
    seq = node.seq
    for feature in node.features:
        start = feature.location.start
        end = feature.location.end
        strand = feature.location.strand
        feature_seq = seq[start:end]
        feature_id = feature.id
        
        os.system('touch query.fasta')
        os.system('echo ">' + feature_id + '\n' + str(feature_seq) + '" >> query.fasta')
        
        os.system('blastn -task blastn -max_target_seqs 1 -outfmt 6 -query query.fasta -db blastdb -out blastn/' + feature_id + '_results.out')
        
        results = open('blastn/' + feature_id + '_results.out', 'r').readline().split('\t')
        
        if len(results) > 1:
            pident = float(results[2])
        else: pident = 0
        
        if pident > 90:
            length = int(results[3])
            qcov = length / (int(results[7]) - int(results[6]) + 1)
            scov = length /(int(results[9]) - int(results[8]) + 1)
            outfile.write(id + '\t' + feature_id + '\t' + str(pident) + '\t' + str(qcov) + '\t' + str(scov) + '\t' + str(results[4]) + '\t' + str(results[5]) + '\n')
        
        os.system('rm query.fasta')

outfile.close()

############## filter candidates ###############
# file = open('outfile', 'r')
# filter = []
# for line in file:
#         l = line.split('\t')
#         if l[2] != '1.0' or l[3] != 0 or l[4] != 0:
#                 filter.append(l)

# candidates = []
# for elem in filter:
    
