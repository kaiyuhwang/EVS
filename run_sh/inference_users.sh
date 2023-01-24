#!/usr/bin/env bash
# author: Kaiyu Huang
# time: 2022/05
# version: 1.0

#test-data-bin path
export DATA_PATH=''
#checkpoint path
export CHECKPOINT_PATH=''
export lang_pairs=cs-en,de-en,fi-en,fr-en,hi-en,lt-en,lv-en,ru-en,ro-en,tr-en,zh-en,es-en,et-en
#output path
export OUTPUT_PATH=''
export USER_DIR='users/'
export ARCH=transformer_expansion
export TASK=translation_multi_simple_epoch

mkdir -p $OUTPUT_PATH

SRC=$SRC
TGT=$TGT

fairseq-generate $DATA_PATH \
  --batch-size 32 \
  --user-dir $USER_DIR \
  --path $CHECKPOINT_PATH \
  -s $SRC -t $TGT \
  --task $TASK \
  --remove-bpe 'sentencepiece' --beam 4 \
  --lang-pairs $lang_pairs \
  --decoder-langtok --encoder-langtok src \
  --gen-subset test > $OUTPUT_PATH''$SRC'-'$TGT'.gen_out'