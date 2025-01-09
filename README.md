# SignaPeptide-SVM

This repository contains all the materials for the final project of the course Laboratory of Bioinformatics 2 of the MSc Bioinformatics - University of Bologna (AY 2023-2024). 
The projects consists in implementing two different methods for the **identification of signal peptides in eukaryotes**: 
* A position-specific weight matrix (**PSWM**) method, that traces one of the earliest approaches (von Heijne, 1986)
* A Support Vector Machine classifier (**SVC**)

## 1. INTRODUCTION
### Signal Peptides
Signal peptides (SPs) are short amino acid sequences that act as molecular "zip codes," directing proteins to the secretory pathway. A typical SP consists of 15–30 residues and exhibits a tripartite structure:

*   **N-region:** A positively charged domain (1–5 residues).
*   **H-region:** A hydrophobic core (7–15 residues).
*   **C-region:** The region flanking the cleavage site (3–7 residues).


![Alt text for the image](images/signalpeptide.png)

Generally, SPs show a great variability, however, they seem more conserved around the cleavage site, indeed, positions - 1 and - 3 seem to be strongly selected for small and neutral residues.

Signal peptide prediction is one of the earliest challenges in the bioinformatics field. Distinguishing SPs from N-terminal transmembrane helices or transit peptides, which also contain hydrophobic regions (though of different lengths), is a key difficulty. Furthermore, the variability of the cleavage site sequence, particularly in eukaryotes, adds complexity to accurate cleavage site prediction.

### Objective of this project
This project implements an **SVC** for SP prediction in eukaryotes. The model **incorporates features encoding characteristics of both the SP sequence and the broader protein context**, aiming for a more comprehensive prediction. The SVC's performance is compared to that of a PSWM method based on von Heijne's (1986) approach. Benchmarking on the same blind test set demonstrated the superior performance of the SVC, achieving an **MCC of 0.89**, with higher sensitivity and precision compared to the PSWM.
