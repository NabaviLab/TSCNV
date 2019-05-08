# **Copy number variation detection for next generation sequencing data using TV-L1**

## **Input:**

- Sorted BAM files of the tumour and control (matched normal) samples

- Duplicate reads must be removed from BAM files

## **Output:**

- Copy number variation segments


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

##### Removing outliers using Hampel identifier
```
$ python hampel.py
```
##### Applying Iterative Taut String to detect change points
```
$ python TS.py
```
##### Removing false possitives using Pettitt test
```
$ python Pettitt.py
```

