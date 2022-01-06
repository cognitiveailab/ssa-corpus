# Space Situational Awareness (SSA) Corpus

This is the repository for the paper "Extracting Space Situational Awareness Events from News Text" (Xie et al., Under Review).

## Labelled Corpus

The labelled spans can be found in the [data](data/) folder, and are presened in the CoNLL BIO format. 

## Results and Analyses

The performance of the span labelling system can be found in [results](results/).  
Preditions of the system on the test set can be found in [results](results/). 
Subsequent analyses (including micro-averages) can be found in [results/analysis](results/analysis/). 

## Code

The open source span labelling system can be found at: https://github.com/kamalkraj/BERT-NER , which requires customization using the code found in this repository in the [code](code/) folder. 
For training, replace `run_ner.py` with the version customized for this SSA corpus.  The included `runme_60.sh` script will complete the training and evaluation procedure for each of the three SSA events (launches, failures, and decommissionings). For inference (label prediction), use `inference.py`. 

## Contact us

Should you have any questions, comments, or issues, please feel free to get in touch at `pajansen@arizona.edu` . 
