#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kaiyu Huang, Wei Liu
# time: 2022/05
# version: 1.0

import argparse

def rollback_unk(data, vocab, outfile):
    word_num = 0
    unk_num = 0
    cut_form = {}
    new_lines = []
    l_count = 0
    for line in data:
        if l_count % int(len(data)/100) == 0:
            print("{:.2f}%".format((l_count/len(data))*100))
        l_count += 1
        new_line = ''
        word_list = line.strip().split()
        for word in word_list:
            if word in vocab:
                new_line = new_line + word + ' '
            else:
                unk_num += 1
                if word in cut_form:
                    new_line = new_line + cut_form[word] + ' '
                else:
                    cut_form[word] = []            
                    seg = seg_dp(word, vocab)
                    new_token = ' '.join(seg)
                    cut_form[word] = new_token
                    new_line = new_line + new_token + ' '
            word_num += 1
        new_lines.append(new_line + '\n') 
    print('the amount of unk: ', unk_num)
    print('the amount of words: ', word_num)
    print('the proportion of unk: ', unk_num/word_num*1.0)
    with open(outfile, 'w', encoding='utf-8') as f_out:
        for l in new_lines:
            f_out.write(l)

def subseg_by_vocab(lines, vocab, outfile):
    new_lines = []
    cut_form = {}
    l_count = 0
    i = 0
    j = 0
    for l in lines:
        if l_count % int(len(lines)/100) == 0:
            print("{:.2f}%".format((l_count/len(lines))*100))
        l_count += 1

        new_l = []
        l = l.strip().split()
        for w in l:
            if len(w) == 1 or (len(w) == 2 and w[0] == '▁'):
                new_l.append(w)
            else:         
                value = vocab[w]
                vocab.pop(w, None)      
                if w in cut_form:
                    for sub_word in cut_form[w]:
                        new_l.append(sub_word)
                elif w not in vocab:
                    cut_form[w] = []
                    seg = seg_pre_max(w, vocab)
                    seg2 = seg_dp(w, vocab)
                    if len(seg) < len(seg2):
                        i += 1
                    elif len(seg) > len(seg2):
                        j += 1

                    for key in seg:
                        cut_form[w].append(key)
                        new_l.append(key)
                else:
                    new_l.append(w)
                vocab[w] = value
        new_lines.append(' '.join(new_l)+'\n')
    with open(outfile, 'w', encoding='utf-8') as f_out:
        for l in new_lines:
            f_out.write(l)

def seg_dp(str, vocab):
    n = len(str)
    cost = [i for i in range(n)]
    pre = [i for i in range(n)]
    for r in range(n):
        min_cost = cost[r]
        for l in range(r+1):
            w = str[l:r+1]
            if w in vocab:
                c = cost[l-1] + 1 if l-1 >= 0 else 0
                if min_cost >= c:
                    min_cost = c
                    cost[r] = min_cost
                    pre[r] = l
    seg = []
    r = n - 1
    while r >= 0:
        l = pre[r]
        seg.append(str[l:r+1])
        r = l - 1
    seg.reverse()

    return seg

def seg_pre_max(str, vocab):
    seg = []
    start = 0
    while start < len(str):
        end = len(str)
        while end > start and str[start:end] not in vocab:
            end -= 1
        if start == end:
            end += 1
        seg.append(str[start:end])
        start = end
    
    return seg

def main(args):
    
    with open(args.input, 'r', encoding='utf8') as fd:
        data = fd.readlines()
    vocab = dict()
    with open(args.vocab, 'r', encoding='utf8') as fd:
        vocab_data = fd.readlines()   
    for line in vocab_data:
        word_list = line.strip().split()
        vocab[word_list[0]] = word_list[1]
    rollback_unk(data, vocab, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='', help='path of input data')
    parser.add_argument('--output', type=str, default='', help='path of output data')
    parser.add_argument('--vocab', type=str, default='', help='vocabulary path')
    args = parser.parse_args()
    main(args)
    