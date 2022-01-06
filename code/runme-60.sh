#!/bin/bash
EPOCHS=60

python3 run_ner.py  --data_dir=/home/peter/github/ssa-ie2/data/decom/ --bert_model=bert-base-cased --task_name=ner --output_dir=out_decom/${EPOCHS}_epoch --max_seq_length=128 --num_train_epochs ${EPOCHS} --do_train --do_eval --eval_on=dev --warmup_proportion=0.1 2>&1 | tee out_decom/${EPOCHS}_out_valid.txt
python3 run_ner.py  --data_dir=/home/peter/github/ssa-ie2/data/decom/ --bert_model=bert-base-cased --task_name=ner --output_dir=out_decom/${EPOCHS}_epoch --max_seq_length=128 --do_eval --eval_on=test --warmup_proportion=0.1  2>&1 | tee out_decom/${EPOCHS}_out_test.txt

python3 run_ner.py  --data_dir=/home/peter/github/ssa-ie2/data/failure/ --bert_model=bert-base-cased --task_name=ner --output_dir=out_failure/${EPOCHS}_epoch --max_seq_length=128 --num_train_epochs ${EPOCHS} --do_train --do_eval --eval_on=dev --warmup_proportion=0.1 2>&1 | tee out_failure/${EPOCHS}_out_valid.txt
python3 run_ner.py  --data_dir=/home/peter/github/ssa-ie2/data/failure/ --bert_model=bert-base-cased --task_name=ner --output_dir=out_failure/${EPOCHS}_epoch --max_seq_length=128 --do_eval --eval_on=test --warmup_proportion=0.1  2>&1 | tee out_failure/${EPOCHS}_out_test.txt

python3 run_ner.py  --data_dir=/home/peter/github/ssa-ie2/data/launch/ --bert_model=bert-base-cased --task_name=ner --output_dir=out_launch/${EPOCHS}_epoch --max_seq_length=128 --num_train_epochs ${EPOCHS} --do_train --do_eval --eval_on=dev --warmup_proportion=0.1 2>&1 | tee out_launch/${EPOCHS}_out_valid.txt
python3 run_ner.py  --data_dir=/home/peter/github/ssa-ie2/data/launch/ --bert_model=bert-base-cased --task_name=ner --output_dir=out_launch/${EPOCHS}_epoch --max_seq_length=128 --do_eval --eval_on=test --warmup_proportion=0.1  2>&1 | tee out_launch/${EPOCHS}_out_test.txt

