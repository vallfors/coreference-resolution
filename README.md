# Co-reference resolution
This is a project by four KTH students. The project is based on the paper "Latent Structure Perceptron with Feature Induction for Unrestricted Coreference Resolution" by Eraldo Rezende Fernandes, Cicero Nogueira dos Santos and Ruy Luiz Milidiu from 2012 (https://www.aclweb.org/anthology/W12-4502.pdf). 

The aim is to create an algorithm that can solve the co-reference resolution problem by clustering mentions in a text referring to the same entity. For training and testing, the GUM dataset supplied by Georgetown University is used.

## Usage
To use the algorithm, GUM data files (for the "coref" layer in GUM, in tsv format) needs to be added to the paths "data/GUM_tsv/training" and "data/GUM_tsv/testing/". 

Command to run the full project on one example file from the GUM dataset. 
```bash
python main.py
```
The project will automaticaly install corenlp on first run (this may take some time).
