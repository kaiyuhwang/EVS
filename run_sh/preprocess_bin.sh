#!/usr/bin/env bash
# author: Kaiyu Huang
# time: 2022/05
# version: 1.0

#vocab path
vocab=''
workers=32
trainpref=''
validpref=''
testpref=''
outfile=''

echo 'preprocess the file: '$langs'-en'
echo 'wrote the data in the: '$outfile

fairseq-preprocess --source-lang $langs --target-lang en \
--trainpref $trainpref \
--validpref $validpref \
--testpref $testpref \
--destdir $outfile \
--thresholdsrc 0 --thresholdtgt 0 \
--srcdict $vocab \
--tgtdict $vocab \
--workers $workers