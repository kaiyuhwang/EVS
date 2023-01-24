#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kaiyu Huang, Wei Liu
# time: 2022/05
# version: 1.0

import argparse
import re
import math

def combine_vocabulary_with_frequency(old_vocab_file, incre_vocab_file, new_vocab_file):
    old_vocab = dict()
    incre_vocab = dict()
    old_lang_list = list()
    new_lang_list = list()
    with open(old_vocab_file, 'r', encoding='utf8') as fd:
        old_vocab_data = fd.readlines()
    with open(incre_vocab_file, 'r', encoding='utf8') as fd:
        incre_vocab_data = fd.readlines()    
    overlap = 0
    overwrite_vocab = dict()
    overlap_vocab = list()
    not_overlap_vocab = dict()
    fix_total_length = len(old_vocab_data)
    print('the length of fix vocab: ', fix_total_length)
    for line in old_vocab_data:
        word_list = line.strip().split()
        if re.match('__[A-Za-z]+__', word_list[0]):
            old_lang_list.append(word_list[0])
        else: 
            old_vocab[word_list[0]] = word_list[1]
    for line in incre_vocab_data:
        word_list = line.strip().split()
        if re.match('__[A-Za-z]+__', word_list[0]):
            if word_list[0] not in old_lang_list:
                new_lang_list.append(word_list[0])
        else: 
            incre_vocab[word_list[0]] = word_list[1]
    print('the length of old vocab: ', len(old_vocab))
    print('the length of incremental vocab: ', len(incre_vocab))
    for vocab in old_vocab:
        if vocab in incre_vocab:
            overlap += 1
            overlap_vocab.append(vocab)
        else:
            not_overlap_vocab[vocab] = old_vocab[vocab]
    for vocab in incre_vocab:
        if vocab not in old_vocab:
            not_overlap_vocab[vocab] = incre_vocab[vocab]
    print('the length of non-overlap vocab: ', len(not_overlap_vocab))
    print('the length of non-overlap vocab: {} and rate: {} '.format(overlap, overlap / fix_total_length))
    not_overlap_vocab = sorted(not_overlap_vocab.items(), key = lambda x: int(x[1]), reverse = True)
    not_overlap_vocab = not_overlap_vocab[:fix_total_length-len(overlap_vocab)-len(old_lang_list)-len(new_lang_list)]
    print('the length of non-overlap vocab after filtering: ', len(not_overlap_vocab))
    sort_frequency_not_overlap_vocab_from_old = list()
    sort_frequency_not_overlap_vocab_from_new = list()
    for t in not_overlap_vocab:
        if t[0] not in old_vocab:
            sort_frequency_not_overlap_vocab_from_new.append((t[0], t[1]))
        else:
            sort_frequency_not_overlap_vocab_from_old.append(t[0])
    index_add = 0
    sum_num = 0
    for word in old_vocab:
        sum_num += 1
        if sum_num < len(old_vocab)-len(new_lang_list) + 1:
            if word in overlap_vocab:
                overwrite_vocab[word] = old_vocab[word]
            elif word not in overlap_vocab and word in sort_frequency_not_overlap_vocab_from_old:
                overwrite_vocab[word] = old_vocab[word]
            else:
                overwrite_vocab[sort_frequency_not_overlap_vocab_from_new[index_add][0]] = sort_frequency_not_overlap_vocab_from_new[index_add][1]
                index_add += 1

    with open(new_vocab_file, 'w', encoding='utf8') as fw:
        for word in overwrite_vocab:
            fw.write(word + ' ' + overwrite_vocab[word] + '\n')
        for lang in new_lang_list:
            fw.write(lang + ' 1' + '\n')
        for lang in old_lang_list:
            fw.write(lang + ' 1' + '\n')
    print('vocabulary substitution success via mode: {}'.format(args.mode))

def combine_vocabulary_with_none(old_vocab_file, incre_vocab_file, new_vocab_file):
    old_vocab = dict()
    with open(old_vocab_file, 'r', encoding='utf8') as fd:
        old_vocab_data = fd.readlines()
    with open(incre_vocab_file, 'r', encoding='utf8') as fd:
        incre_vocab_data = fd.readlines()    
    for line in old_vocab_data:
        word_list = line.strip().split()
        old_vocab[word_list[0]] = word_list[1]
    for line in incre_vocab_data:
        word_list = line.strip().split()
        if word_list[0] not in old_vocab:
            old_vocab[word_list[0]] = word_list[1]
        else:
            old_vocab[word_list[0]] = int(old_vocab[word_list[0]]) + int(word_list[1])
    with open(new_vocab_file, 'w', encoding='utf8') as fw:
        for v in old_vocab:
            fw.write(v + ' ' + str(old_vocab[v]) + '\n')
    print('the length of new vocab: ', len(old_vocab))
    print('vocabulary substitution success via mode: {}'.format(args.mode))

def combine_vocabulary_with_entropy(old_vocab_file, incre_vocab_file, new_vocab_file):
    scorer = dict()
    vocab = dict()
    vocab_old = dict()
    vocab_new = list()
    vocab_add = list()

    old_lang_list = list()
    new_lang_list = list()
    with open(old_vocab_file, 'r', encoding='utf8') as fd:
        old_vocab_data = fd.readlines()
    with open(incre_vocab_file, 'r', encoding='utf8') as fd:
        vocab_data = fd.readlines()
    
    for data in old_vocab_data:
        word = data.split()[0]
        if re.match('__[A-Za-z]+__', word):
            old_lang_list.append(word)
        else: 
            vocab_old[word] = data.split()[1]
  
    for line in vocab_data:
        word_list = line.strip().split()
        if re.match('__[A-Za-z]+__', word_list[0]):
            if word not in old_lang_list:
                new_lang_list.append(word_list[0])
        else: 
            vocab[word_list[0]] = list()
            for i in range(1, len(word_list)):
                vocab[word_list[0]].append(word_list[i])
    f_vocab = dict()
    for word in vocab:
        if len(word) == 1 or (len(word) == 2 and word[0] == '▁'):
            f_vocab[word] = vocab[word][0]
        else:    
            info = vocab[word]
            p = [0]*21
            p[0] = int(info[0])
            for i in range(1, 21):
                p[i] = int(info[i]) / int(info[0])
                p[0] = p[0] - int(info[i])
            p[0] = p[0] / int(info[0])
            entropy = 0
            for i in range(len(p)):
                if p[i] == 0:
                    entropy = 0 + entropy
                else:
                    entropy = p[i]*math.log(p[i],2)*(-1) + entropy
            scorer[word] = entropy
    score_ranker = sorted(scorer.items(), key=lambda x: x[1], reverse=True)
    num=0
    score_ranker_0 = list()
    for i in scorer:
        if scorer[i] == 0:
            num+=1
            score_ranker_0.append(i)
    
    # get the reranker vocabulary
    score_ranker = score_ranker[:len(vocab_old)-len(score_ranker_0)-len(f_vocab)]
    for word in f_vocab:
        vocab_new.append((word, f_vocab[word]))
        vocab_add.append(word)
    for i in range(len(score_ranker)):
        vocab_new.append((score_ranker[i][0], vocab[score_ranker[i][0]][0]))
        vocab_add.append(score_ranker[i][0])
    for i in range(len(score_ranker_0)):
        vocab_new.append((score_ranker_0[i], vocab[score_ranker_0[i]][0]))
        vocab_add.append(score_ranker_0[i])
    
    # overwrite the old vocabulary
    not_overlap_vocab = list()
    overwrite_vocab = dict()
    for new_word_tuple in vocab_new:
        new_word = new_word_tuple[0]
        if new_word not in vocab_old:
            not_overlap_vocab.append(new_word_tuple)
    index_add = 0
    sum_num = 0
    for word in vocab_old:
        sum_num += 1
        if sum_num < len(vocab_old)-len(new_lang_list) + 1:
            if word not in vocab_add and index_add < len(not_overlap_vocab):
                overwrite_vocab[not_overlap_vocab[index_add][0]] = not_overlap_vocab[index_add][1]
                index_add += 1
            else:
                overwrite_vocab[word] = vocab_old[word]
    with open(new_vocab_file, 'w', encoding='utf8') as fw:
        for word in overwrite_vocab:
            fw.write(word + ' ' + overwrite_vocab[word] + '\n')
        for lang in new_lang_list:
            fw.write(lang + ' 1' + '\n')
        for lang in old_lang_list:
            fw.write(lang + ' 1' + '\n')
    print('vocabulary substitution success via mode: {}'.format(args.mode))    

def overwrite_vocab(old_vocab_file, incre_vocab_file, new_vocab_file):
    vocab_old = dict()
    vocab_new = list()
    vocab_add = list()
    old_lang_list = list()
    new_lang_list = list()
    with open(old_vocab_file, 'r', encoding='utf8') as fd:
        old_vocab_data = fd.read().splitlines()
    with open(incre_vocab_file, 'r', encoding='utf8') as fd:
        new_vocab_data = fd.read().splitlines()
    for data in old_vocab_data:
        word = data.split()[0]
        if re.match('__[A-Za-z]+__', word):
            old_lang_list.append(word)
        else: 
            vocab_old[word] = data.split()[1]
    for data in new_vocab_data:
        word = data.split()[0]
        if re.match('__[A-Za-z]+__', word):
            if word not in old_lang_list:
                new_lang_list.append(word)
        else: 
            vocab_new.append((word, data.split()[1]))
            vocab_add.append(word)
    vocab_new = sorted(vocab_new, key=lambda x: int(x[1]), reverse=True)
    not_overlap_vocab = list()
    overwrite_vocab = dict()
    for new_word_tuple in vocab_new:
        new_word = new_word_tuple[0]
        if new_word not in vocab_old:
            not_overlap_vocab.append(new_word_tuple)
    index_add = 0
    sum_num = 0
    for word in vocab_old:
        sum_num += 1
        if sum_num < len(vocab_old)-len(new_lang_list) + 1:
            if word not in vocab_add and index_add < len(not_overlap_vocab):
                overwrite_vocab[not_overlap_vocab[index_add][0]] = not_overlap_vocab[index_add][1]
                index_add += 1
            else:
                overwrite_vocab[word] = vocab_old[word]
    with open(new_vocab_file, 'w', encoding='utf8') as fw:
        for word in overwrite_vocab:
            fw.write(word + ' ' + overwrite_vocab[word] + '\n')
        for lang in new_lang_list:
            fw.write(lang + ' 1' + '\n')
        for lang in old_lang_list:
            fw.write(lang + ' 1' + '\n')
    print('vocabulary substitution success via mode: {}'.format(args.mode))

def main(args):
    old_vocab_file = args.ov
    incre_vocab_file = args.iv
    new_vocab_file = args.nv
    if args.mode == 'frequency':
        combine_vocabulary_with_frequency(old_vocab_file, incre_vocab_file, new_vocab_file)
    elif args.mode == 'combine':
        combine_vocabulary_with_none(old_vocab_file, incre_vocab_file, new_vocab_file)
    elif args.mode == 'overwrite':
        overwrite_vocab(old_vocab_file, incre_vocab_file, new_vocab_file)
    elif args.mode == 'evs':
        combine_vocabulary_with_entropy(old_vocab_file, incre_vocab_file, new_vocab_file)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='evs', help='vocabulary substitution: evs; frequency; combine; overwrite')
    parser.add_argument('--ov', type=str, default='', help='path of original vocabulary')
    parser.add_argument('--iv', type=str, default='', help='path of incremental vocabulary')
    parser.add_argument('--nv', type=str, default='', help='output path of generated vocabulary')
    args = parser.parse_args()
    main(args)
    