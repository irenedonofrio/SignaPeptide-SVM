#retrieve positives
(taxonomy_id:2759) AND (length:[30 TO *]) AND (reviewed:true) AND (ft_signal_exp:*)
#filter out the one whose cleaved position is unclear (1-?) or the Signal peptides that are shorter than 13
python3 ../filter_SP.py pos_notfiltered.tsv pos_filtered.tsv
#2942 pos_filtered.tsv
#take only the entries and remove the header
cut -f 1 pos_filtered.tsv |tail +2 > pos_filteredtmp.tsv && mv pos_filteredtmp.tsv pos_filtered.tsv

#retrieve the negatives (columns: signal peptide and subcellular location)
(taxonomy_id:2759) AND (length:[30 TO *]) AND (reviewed:true) NOT (ft_signal:*) AND ((cc_scl_term_exp:SL-0091) OR (cc_scl_term_exp:SL-0173) OR (cc_scl_term_exp:SL-0209) OR (cc_scl_term_exp:SL-0204) OR (cc_scl_term_exp:SL-0039) OR (cc_scl_term_exp:SL-0191))
#but then you have you need to check the subcellular localization (-i => case insensitiv 
grep -iv -E 'endoplasmic|golgi|secreted|lysosome' neg_notfiltered.tsv > neg_filtered.tsv
#take only the entries and remove the header
cut -f 1 neg_filtered.tsv |tail +2 > neg_filteredtmp.tsv && mv neg_filteredtmp.tsv neg_filtered.tsv
#29909 neg_filtered.tsv

#id mapping on Uniprot and download the FASTA files

#clustering => MMSeqs2
#to install MMSeqs2:
conda create -n lb2 mmseqs2

#clustering +
mmseqs easy-cluster positives.fasta cluster-results tmp --min-seq-id 0.3 -c 0.4 --cov-mode 0 --cluster-mode 1
cut -f 1 cluster-results_cluster.tsv |uniq| wc -l
#positives cartella: seleziono i representatives (la r per randomizzare)
cut -f 1 cluster-results_cluster.tsv | sort -uR > pos_representatives

#cluster -

mmseqs easy-cluster negatives.fasta cluster-results tmp --min-seq-id 0.3 -c 0.4 --cov-mode 0 --cluster-mode 1
cut -f 1 cluster-results_cluster.tsv |uniq| wc -l
cut -f 1 cluster-results_cluster.tsv | sort -uR > neg_representatives


#80-20% 
#POSITIVES:
#scimmia option
#80% = 1...881 per training e 882...1101 per benchmarking
head -n 881 pos_representatives > pos_training
tail +882 pos_representatives > pos_benchmarking
#5-fold training set (881/5 = 176,2)
#1...176
head -n 176 pos_training > pos_training_cv1
#177...352
tail +177 pos_training | head -n 176 > pos_training_cv2
#353...528
tail +353 pos_training | head -n 176 > pos_training_cv3
#529...704
tail +529 pos_training | head -n 176 > pos_training_cv4
#705...881 (ha un entry in più)
tail +705 pos_training > pos_training_cv5

#smart option
split -d -a 1 -l 177 pos_training pos_cv_
split -d -a 1 -n 5 pos_training pos_cv_ #(used this one, fairlier division)

#NEGATIVES (cd ../negatives/)
#scimmia option
#80% = 1...7584 per training e 7585...9479 per benchmarking
head -n 7584 neg_representatives > neg_training
tail +7585 neg_representatives > neg_benchmarking
#5-fold training set (881/5 = 176,2)
#1...176
head -n 176 neg_training > neg_training_cv1
#177...352
tail +177 neg_training | head -n 176 > neg_training_cv2
#353...528
tail +353 neg_training | head -n 176 > neg_training_cv3
#529...704
tail +529 neg_training | head -n 176 > neg_training_cv4
#705...881 (ha un entry in più)
tail +705 neg_training > neg_training_cv5

#smart option 7584/5 = 1516,8
split -d -a 1 -l 1517 neg_training neg_cv_

#create training and benchmarking datasets
cat positives/pos_training negatives/neg_training > training_dataset
cat positives/pos_benchmarking negatives/neg_benchmarking > benchmarking_dataset

#id mapping tool = retrieve metadata
#eliminate first colum (from column)
cut -f 2,3,4,5,6,7 metadata_training.tsv > temporary && mv temporary metadata_training.tsv
cut -f 2,3,4,5,6,7 metadata_benchmarking.tsv > temporary && mv temporary metadata_benchmarking.tsv
#clean the metadata files
python3 filter_metadata.py metadata_training.tsv clean_metadata_training
python3 filter_metadata.py metadata_benchmarking.tsv clean_metadata_benchmarking


#
conda create -n sklearn scikit-learn seaborn matplotlib pandas 
