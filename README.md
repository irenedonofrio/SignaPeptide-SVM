# SignaPeptide-SVM

This repository contains all the materials for the final project of the course Laboratory of Bioinformatics 2 of the MSc Bioinformatics - University of Bologna (AY 2023-2024). 
The projects consists in implementing two different methods for the **identification of signal peptides in eukaryotes**: 
* A position-specific weight matrix (**PSWM**) method, that traces one of the earliest approaches (von Heijne, 1986)
* A Support Vector Machine classifier (**SVC**)

## 1. INTRODUCTION
Signal peptides (SPs) are short peptide that guide the proteins to the secretory pathway acting as moleculaar *zip codes*. A typical SP has 15–30 residues and is characterized by a tripartite structure: i) N-region: the positive-charged domain (1-5 residues), ii) H-region: the hydrophobic core (7-15 residues), and iii) C-region: region flanking the cleavage site (3-7 residues), as shown below:
![Alt text for the image](images/signalpeptide.png)
