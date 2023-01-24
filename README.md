# EVS

## Introduction
Source code for the EMNLP 2022 main conference long paper "Entropy-Based Vocabulary Substitution for Incremental Learning in Multilingual Neural Machine Translation"

In this work, we propose an entropy-based vocabulary substitution (EVS) method that just needs to walk through new language pairs for incremental learning in a large-scale multilingual data updating while remaining the size of the vocabulary.

---
## Get Started
(Core) Data Preprocessing.

Standard BPE Procedure: following https://github.com/google/sentencepiece with 64k merged BPE tokens.

EVS: 

After obtaining the original vocabulary and the incremental vocabulary, you can run scripts for vocabulary substitution in three modes.
- EVS (Ours)
- frequency (choose the top-K words with the highest frequency)
- combine (Expansion)

(Optional) Model Training. 

This system has been tested in the following environment.

Python version == 3.7

Pytorch version == 1.8.0

Fairseq version == 0.12.0 (pip install fairseq)

Note that it only influences the training procedure of the original and incremental model. You can choose your favorite deep learning library for model training.

---
## Incremental Learning
We build the incremental learning procedure for Multilingual Neural Machine Translation as follows:

1. Get original multilingual translation models (or train a multilingual translation model by yourself). We will provide two MNMT models and training scripts for reproducibility.

    Data url: <u>Permission review</u>

    Model url: <u>Permission review</u>

2. Preprocessing incremental data
- Data Clean (optional, if needed)
- Get Vocabulary (follow standard BPE procedure)
- Get Vocabulary Feature (generated the incremental vocabulary with features, only for EVS). We will provide a vocabulary with features for the next stage, and you can also statisfy the feature on your own dataset.
    ```python
    python scripts/get_feature.py --ov 'original_vocabulary' --iv 'incremental_vocabulary' --nv 'incremental_vocabulary_with_feature'
    ```
- EVS
    ```python
    python scripts/evs.py --mode 'mode_name' --ov 'original_vocabulary' --iv 'incremental_vocabulary' --nv 'new_vocabulary'
    ```
- Data Rebuilt (if evs):
    ```python
    python scripts/rebuilt.py --input 'input data' --output 'output data' --vocab 'vocabulary path'
    ```
    
- Data Bin (all data):
    ```bash
    fairseq-preprocess 
    --source-lang $SRC --target-lang $TGT \
    --trainpref $trainpref \
    --validpref $validpref \
    --testpref $testpref \
    --destdir $outfile \
    --thresholdsrc 0 --thresholdtgt 0 \
    --srcdict $vocab \
    --tgtdict $vocab \
    --workers $workers
    ```
3. Incremental Training (Joint Training)
    We provide all runing scripts in the folder ''run_sh''
    An example:
    ```bash
    export lang_dict='example/langs_all,txt' (path of language sets)
    export lang_pairs='' (e.g. en-cs,en-de,en-fi,en-fr,en-hi)

    fairseq-train $DATA_PATH \
    --finetune-from-model $BASE_MODEL \
    --share-all-embeddings \
    --encoder-normalize-before --decoder-normalize-before \
    --encoder-embed-dim 1024 --encoder-ffn-embed-dim 4096 --encoder-attention-heads 16 \
    --decoder-embed-dim 1024 --decoder-ffn-embed-dim 4096 --decoder-attention-heads 16 \
    --encoder-layers 6 --decoder-layers 6 \
    --left-pad-source False --left-pad-target False \
    --arch transformer \
    --task translation_multi_simple_epoch \
    --sampling-method temperature \
    --sampling-temperature 5 \
    --lang-tok-style multilingual \
    --lang-dict $LANG_DICT \
    --lang-pairs $lang_pairs\
    --encoder-langtok src \
    --decoder-langtok \
    --optimizer adam \
    --adam-betas '(0.9, 0.98)' \
    --adam-eps 1e-9 \
    --lr 5e-4 \
    --lr-scheduler inverse_sqrt \
    --warmup-updates 4000 \
    --dropout 0.3 \
    --attention-dropout 0.1 \
    --weight-decay 0.0001 \
    --criterion label_smoothed_cross_entropy\
    --label-smoothing 0.1 \
    --max-tokens 4096 \
    --save-dir $CHECKPOINT_PATH/checkpoints/ \
    --update-freq 4 \
    --max-update 500000 \
    --seed 222 --log-format simple \
    --fp16 \
    --tensorboard-logdir $CHECKPOINT_PATH/logs/ \
    --no-progress-bar \
    --ddp-backend no_c10d
    ```
---
## Inference & Evaluation
Please refer to run_sh/inference.sh & run_sh/evaluate.sh