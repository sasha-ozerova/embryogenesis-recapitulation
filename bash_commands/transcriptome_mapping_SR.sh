#!/bin/bash
# trigger as `transcriptome_mapping_SR.sh folder_name srr_id download_path kallisto_index`

mkdir $1
cd $1
wget $3
fasterq-dump -O fastq $2
rm $2

fastq_files=($(ls -d fastq/*))
fastq=${fastq_files[0]}

mkdir filtered_fastq
fastp -i ${fastq} -o filtered_${fastq}
arr=( $(awk 'BEGIN { t=0.0;sq=0.0; n=0;} ;NR%4==2 {n++;L=length($0);t+=L;sq+=L*L;}END{m=t/n;printf("%.0f %.0f\n",m,sq/n-m*m);}' filtered_${fastq}) )
sd=$(( arr[1] + 1 ))
kallisto quant -i $4 -o kalliso_output -b 50 --single -l ${arr[0]} -s ${sd} filtered_${fastq}

mkdir results
mv fastp.json results
mv kalliso_output/abundance.tsv results
mv kalliso_output/run_info.json results/kalliso_run_info.json

rm fastp.html
rm -rf fastq
rm -rf filtered_fastq
rm -rf kalliso_output
