#!/usr/bin/env bash
# author: Kaiyu Huang
# time: 2022/05
# version: 1.0

export GEN_PATH=''
export REF_PATH=''

SRC=$SRC
TGT=$TGT

if [ $TGT == 'zh' ]; then
  cat $GEN_PATH''$SRC'-'$TGT'.gen_out' | grep -P "^H" | sort -V | cut -f 3- > $GEN_PATH''$SRC'-'$TGT'.hyp'
  sacrebleu -tok 'zh' $REF_PATH''$SRC'-'$TGT'.'$TGT < $GEN_PATH''$SRC'-'$TGT'.hyp' > $GEN_PATH''$SRC'-'$TGT'.eval'
else
  cat $GEN_PATH''$SRC'-'$TGT'.gen_out' | grep -P "^H" | sort -V | cut -f 3- > $GEN_PATH''$SRC'-'$TGT'.hyp'
  sacrebleu -tok '13a' $REF_PATH''$SRC'-'$TGT'.'$TGT < $GEN_PATH''$SRC'-'$TGT'.hyp' > $GEN_PATH''$SRC'-'$TGT'.eval'
fi
