#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kaiyu Huang
# time: 2022/05
# version: 1.0

import argparse
import evs

def get_vocab_feature(args, data, vocab_file):
    vocab = dict()
    i = 0
    with open(vocab_file, 'r', encoding='utf8') as fd:
        vocab_data = fd.readlines()
    for line in vocab_data:
        word_list = line.strip().split()
        vocab[word_list[0]] = list()
        for i in range(1, len(word_list)):
            vocab[word_list[0]].append(word_list[i])
        vocab[word_list[0]].append(0)
    for line in data:
        i += 1
        word_list = line.strip().split()
        for word in word_list:
            if word in vocab:
                vocab[word][-1] += 1
        if i % 100000 == 0:
            print('process the ', i ,' lines, the sum is: ', len(data))
    
    with open(vocab_file, 'w', encoding='utf8') as fw:
        for v in vocab:
            fw.write(v)
            for i in range(len(vocab[v])):
                fw.write(' ' + str(vocab[v][i]))
            fw.write('\n')

def get_proportion(data):
    word_num = 0
    for line in data:
        word_list = line.strip().split()
        word_num += len(word_list)
    return word_num

def main():
    langs_list = args.langs.strip().split(',')
    num_sum = 0
    evs.combine_vocabulary_with_none(args.ov, args.iv, args.nv)
    for langs in langs_list:
        file_name = args.path+'/'+langs
        print('preprocess the language: ', langs)
        with open(file_name, 'r', encoding='utf8') as fd:
            data = fd.readlines()
        num_sum += get_proportion(data)
        get_vocab_feature(args, data, args.nv)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ov', type=str, default='', help='path of original vocabulary')
    parser.add_argument('--iv', type=str, default='', help='path of incremental vocabulary')
    parser.add_argument('--nv', type=str, default='', help='output path of generated vocabulary')
    parser.add_argument('--path', type=str, default='', help='path of training samples')
    parser.add_argument('--langs', type=str, default='', help='language sets, split by comma, e.g., cs-en,de-en,fr-en')
    args = parser.parse_args()
    main(args)
    