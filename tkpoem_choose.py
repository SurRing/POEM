#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import tkinter
import random

from tkpoem_function import *
import tkpoem_windows

def poem_classic(all_poem_list):
    finish_class = []
    citing_class = []
    for poem in all_poem_list:
        print(poem.mark)
        if poem.mark > 3:
            finish_class.append(poem.number)
        else:
            citing_class.append(poem.number)
    print(finish_class, citing_class)
    return finish_class, citing_class

# 随机抽取测试句
def choose_test_sentence(all_poem_list, finish_class, citing_class):
    if random.choice(range(100)) > 90 and finish_class != []:
        test_poem = random_in_poem(all_poem_list, finish_class)
    elif citing_class == []:
        tkpoem_windows.message_window("全部完成")
        test_poem = random_in_poem(all_poem_list, finish_class)
    else:
        test_poem = random_in_poem(all_poem_list, citing_class)
    test_poem_number = test_poem.number
    test_poem_name = test_poem.poem_name()
    distence = random.choice(range(1, test_poem.sentence_number + 1))
    test_print = ''
    test_key = ''
    for section in test_poem.content:
        for whole_sentence in section:
            for sentence in whole_sentence:
                distence -= 1
                if distence == 0:
                    test_sentence = sentence
                    for sentence in whole_sentence:
                        if sentence == test_sentence:
                            test_key += sentence
                            test_print += "__" * (len(sentence) - 1) + sentence[-1]
                        else:
                            test_key += sentence
                            test_print += sentence
                    break
            if distence == 0:
                break
        if distence == 0:
            break
    return test_poem, test_print, test_key

#随机抽取并每句概率相同
def random_in_sentence(all_poem_list, sum_sentence_list):
    random_list = []
    n = 0
    for sentences in sum_sentence_list:
        for i in range(sentences):
            random_list.append(n)
        n += 1
    test_poem = all_poem_list[random.choice(random_list)]
    return test_poem

#随机抽取并每首概率相同
def random_in_poem(all_poem_list, choose_list):
    test_poem = all_poem_list[random.choice(choose_list)]
    return test_poem
