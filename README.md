# SignaPeptide-SVM

This repository contains all the materials for the final project of the course Laboratory of Bioinformatics 2 of the MSc Bioinformatics - University of Bologna (AY 2023-2024). 
The projects consists in implementing two different methods for the **identification of signal peptides in eukaryotes**: 
* A position-specific weight matrix (**PSWM**) method, that traces one of the earliest approaches (von Heijne, 1986)
* A Support Vector Machine classifier (**SVC**)

## 1. INTRODUCTION
### Signal Peptides
Signal peptides (SPs) are short peptide that guide the proteins to the secretory pathway acting as moleculaar *zip codes*. A typical SP has 15–30 residues and is characterized by a tripartite structure: i) N-region: the positive-charged domain (1-5 residues), ii) H-region: the hydrophobic core (7-15 residues), and iii) C-region: region flanking the cleavage site (3-7 residues), as shown below:

![Alt text for the image](images/signalpeptide.png)

Generally, SPs show a great variability, however, they seem more conserved around the cleavage site, indeed, positions - 1 and - 3 seem to be strongly selected for small and neutral residues.

Signal peptide prediction is one of the earliest challenges in the bioifnormatics field however it comes with challenges and year after year new tools are developed for such goal. One of the main difficulties in this task is the distinction between SPs and N-terminal transmembrane helices or transit peptides, united by the presence of hydrophobic regions, even though of different length. Moreover, as for the prediction of the cleavage site, the complexity derives from the sequence variability and the lack of a strong conservation, especially in eukaryotes.

### Objective of this project
In this project I implemented a SVC for the SP prediction in eukaryotes. This model incorporates several features that encode characteristics of both the SP sequence itself
and of the entire protein, resulting in a more comprehensive predictive model. When compared to a position-specific weight matrix (PSWM) method, that traces one of the earliest approaches (von Heijne, 1986), the SVM outperformed it. Indeed, when benchmarked on the same blind set as the weight matrix-based method, the SVM revealed to be a better performing method, with an MCC of 0.89, higher sensitivity and precision. 
