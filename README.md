# **Copy number variation detection for next generation sequencing data using TV-L1**

## **Input:**

#### - Sorted BAM files of the tumour and control (matched normal) samples

#### - Duplicate reads must be removed from BAM files

## **Output:**

#### - Copy number variation segments


## **Method:**

##### Preparing the data: base-level read-count of the exonic regions of both sample and control data using samtools and BEDTools

```
 $ samtools view -bh -L exom.bed tumor.bam > tumor_filteredexon.bam
 $ samtools view -bh -L exom.bed normal.bam > control_filteredexon.bam
 $ samtools view -H tumor_filteredexon.bam  | grep -P "@SQ\tSN:" | sed 's/@SQ\tSN://' | sed 's/\tLN:/\t/' > genome.txt
 $ sort -k1,1V genome.txt > s-genome.txt
 $ bedtools genomecov -ibam tumor_filteredexon.bam -d -g s-genome.txt  > tumor.cov
 $ bedtools genomecov -ibam control_filteredexon.bam -d -g s-genome.txt  > normal.cov 
 $ awk '{if ($1==1) {print}}' tumor.cov > tumor_chr1.cov
 $ awk '{if ($1==1) {print}}' normal.cov > normal_chr1.cov
 $ awk '{print $3}' tumor_chr1.cov > tumorreads.txt
 $ awk '{print $3}' normal_chr1.cov > normalreads.txt

```


# **Copy number variation detection for Single-cell sequencing data**
## **Input:**

#### - fastq files of cells

## **Output:**

#### - Copy number variation segments

## **Preprocessing:**



$ bwa mem -t $processor -r  "@RG\tID:singlecell\tSM:singlecell" $ref 0_1.fq 0_2.fq > 0.sam


$ bwa mem -t $processor -r  "@RG\tID:singlecell\tSM:singlecell" $ref 1_1.fq 1_2.fq > 1.sam

$ samtools sort -O sam -o 0.sam -T "TMP" 0.sam
$ samtools sort -O sam -o 1.sam -T "TMP" 1.sam

$ samtools view  -hbS 0.sam > 0.bam
$ samtools view -hbS 1.sam > 1.bam


$ samtools merge cell.bam 0.bam 1.bam -f

$ samtools sort -o cell.sorted.beforedup.bam cell.bam
$ samtools rmdup cell.sorted.beforedup.bam cell.sorted.bam
$ samtools index cell.sorted.bam




$ computeGCBias -b sorted.bam --effectiveGenomeSize 2864785220 -g hg19.2bit --GCbiasFrequenciesFile freq.txt -l 200

$ correctGCBias -b sorted.bam --effectiveGenomeSize 2864785220 -g hg19.2bit --GCbiasFrequenciesFile freq.txt -o gc_correct.bam

$ samtools view -b -q 37 -o gc_correct-filtered37.bam gc_correct${j}.bam

$ bamToBed -i gc_correct${j}-filtered37.bam > /labs/Nabavi/Fatimahome/singlecelldata/simulated/${ploidy}/TSCNV/bedfiles/gc_correct-filtered37.bed

$ awk '{print $1="chr"$1 "\t" $2}' gc_correct${j}-filtered37.bed > /gc_correct-filtered37-pos.txt

$ samtools view -H gc_correct-filtered37.bam  | grep -P "@SQ\tSN:" | sed 's/@SQ\tSN://' | sed 's/\tLN:/\t/' > genome.bed

$ sort -k1,1V genome.bed > s-genome.bed

$ bedtools makewindows -g s-genome.bed -w W  -i srcwinnum >  windows.bed

$ bedtools coverage -abam gc_correct-filtered37.bam -b windows.bed > cov.bed

$ bedtools groupby -i cov.bed -g 1,2,3 -c 13 > groupby.cov.bed

$ awk '($1!="MT") &&($1!="Y")&&($1!="X")' groupby.cov.bed > groupby22.cov.bed
$ samtools index gc_correct-filtered37.bam 
$ bedtools multicov -bams gc_correct-filtered37.bam -bed windows.bed > readcounts.bed


$ Rscript normalize.R 


## **Segmentation:**

## **Cross-cell analysis:**
