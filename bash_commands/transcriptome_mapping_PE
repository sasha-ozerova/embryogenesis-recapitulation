#!/bin/bash
# trigger as `transcriptome_mapping_PE.sh folder_name srr_id download_path kallisto_index`
mkdir $1
cd $1
wget $3
fasterq-dump -O fastq $2
rm $2
fastq_files=($(ls -d fastq/*))
fastq1_files=($(printf "%s\n" "${fastq_files[@]}" |sed "/_1.fastq/!d"))
fastq1=${fastq1_files[0]}
fastq2_files=($(printf "%s\n" "${fastq_files[@]}" |sed "/_2.fastq/!d"))
fastq2=${fastq2_files[0]}

mkdir filtered_fastq
fastp -i ${fastq1} -I ${fastq2} -o filtered_${fastq1} -O filtered_${fastq2}
kallisto quant -i $4 -o kalliso_output -b 50 filtered_${fastq1} filtered_${fastq2}

mkdir results
mv fastp.json results
mv kalliso_output/abundance.tsv results
mv kalliso_output/run_info.json results/kalliso_run_info.json

rm fastp.html
rm -rf fastq
rm -rf filtered_fastq
rm -rf kalliso_output
