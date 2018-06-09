#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import pickle
import re

# 导入古诗。分为段；整句；句。
def poem_import2(location):
    ALL_POEM = []
    TXTPOEM = open(location, "r", encoding='utf-8')
    number = 0
    sum_sentence_list = []
    while 1:
        ALL_POEM.append({"number": number})
        ALL_POEM[number]["title"] = TXTPOEM.readline()[:-1]
        if ALL_POEM[number]["title"] == "":
            ALL_POEM = ALL_POEM[:-1]
            break
        print("Start loading ", ALL_POEM[number]["title"])
        ALL_POEM[number]["dynasty"] = TXTPOEM.readline()[:-1]
        ALL_POEM[number]["author"] = TXTPOEM.readline()[:-1]
        ALL_POEM[number]["content"] = []

        sum_sentence = 0
        number_of_section = 0
        for row in TXTPOEM:
            if row[-2:-1] == "。" or row[-2:-1] == "！" or row[-2:-1] == "？":  # 对于每个换行符进行判断是否仍然是该诗的段落
                ALL_POEM[number]["content"].append([])  # 为诗的内容添加一个段落
                number_of_whole_sentence = 0
                ALL_POEM[number]["content"][number_of_section].append([])  # 为诗的段落添加一个整句
                # 在该段中取出每一句
                flag = 0
                last = 0
                i = 0
                while row[i] != "\n":
                    # print(i)
                    # print(row)
                    # print(row[i])
                    if row[i] == "。" or row[i] == "！" or row[i] == "？":
                        if flag:
                            number_of_whole_sentence += 1
                            ALL_POEM[number]["content"][number_of_section].append([])  # 为诗的段落添加一个整句
                            flag = 0
                        #number_of_whole_sentence += 1
                        #ALL_POEM[number]["content"][number_of_section].append([])  # 为诗的段落添加一个整句
                        ALL_POEM[number]["content"][number_of_section][number_of_whole_sentence].append(
                            row[last:i + 1])  # 且作为该整句的唯一的句子
                        flag = 1
                        last = i + 1
                        sum_sentence += 1
                    if row[i] == "，" or row[i] == "；" or row[i] == "：":
                        if flag:
                            number_of_whole_sentence += 1
                            ALL_POEM[number]["content"][number_of_section].append([])  # 为诗的段落添加一个整句
                            flag = 0
                        # print(number_of_section,number_of_whole_sentence)
                        ALL_POEM[number]["content"][number_of_section][number_of_whole_sentence].append(
                            row[last:i + 1])  # 仅为诗的一个整句添加一个句子
                        last = i + 1
                        sum_sentence += 1
                    i += 1
                    # print(ALL_POEM[number])
                number_of_section += 1
            else:
                break
        sum_sentence_list.append(sum_sentence)
        ALL_POEM[number]["sentence_number"] = sum_sentence
            # print(ALL_POEM[number])
        # print(ALL_POEM[number])
        print(ALL_POEM[number]["title"], " is loaded completely.")
        #print(ALL_POEM[number]["sentence_number"])
        number += 1
    TXTPOEM.close()
    return ALL_POEM, sum_sentence_list

def poem_import(location):
    ALL_POEM = []
    TXTPOEM = open(location, "r", encoding='utf-8')
    sum_sentence_list = []
    number = -1
    content_flag = 0
    while 1:
        txt_line = TXTPOEM.readline()[:-1]
        print(txt_line)
        #check = re.match("--(\w+)--", txt_line)
        if txt_line == "--Start--":
            number += 1
            section = -1
            whole_sentence = -1
            sentence = 0
            ALL_POEM.append({"number": number})
        elif txt_line == "--title--":
            ALL_POEM[number]["title"] = TXTPOEM.readline()[:-1]
        elif txt_line == "--dynasty--":
            ALL_POEM[number]["dynasty"] = TXTPOEM.readline()[:-1]
        elif txt_line == "--author--":
            ALL_POEM[number]["author"] = TXTPOEM.readline()[:-1]
        elif txt_line == "--content--":
            content_flag = 1
            ALL_POEM[number]["content"] = []
        elif content_flag == 1:
            if txt_line == "--new_section--":
                ALL_POEM[number]["content"].append([])
                section += 1
                whole_sentence = -1
            elif txt_line == "--new_whole_sentence--":
                ALL_POEM[number]["content"][section].append([])
                whole_sentence +=1
            elif txt_line == "--content_end--":
                content_flag = 0
                ALL_POEM[number]["sentence_number"] = sentence
                sum_sentence_list.append(sentence)
                print(ALL_POEM[number]["title"], " is loaded completely.")
            else:
                ALL_POEM[number]["content"][section][whole_sentence].append(txt_line)
                sentence += 1
        elif txt_line == "--file_end--":
            print("All completed!")
            break
    TXTPOEM.close()
    return ALL_POEM, sum_sentence_list

"""
def information_import(location):
    finished_poem_list = []
    citing_poem_list = []
    queueing_poem_list = []
    txt_information = open(location, "r", encoding='utf-8')
    n = 0
    while 1:
        i = txt_information.readline()[:-1]
        if i == " ":
            break
        elif i == "0":
            queueing_poem_list.append(n)
        elif i == "1":
            citing_poem_list.append(n)
        elif i == "2":
            finished_poem_list.append(n)
        n += 1
    txt_information.close()
    return finished_poem_list, citing_poem_list, queueing_poem_list
"""

def information_pickle_dump(information, location):
    information_file = open(location, "wb")
    pickle.dump(information, information_file)
    information_file.close()

def information_pickle_load(location):
    information_file = open(location, "rb")
    information = pickle.load(information_file)
    information_file.close()
    return information

class Poem():

    def __init__(self, number, title, dynasty, author, content, sentence_number):
        self.number = number
        self.title = str(title)
        self.dynasty = str(dynasty)
        self.author = str(author)
        self.content = content
        self.sentence_number = sentence_number
        self.mark = 0

    def poem_name(self):
        poem_name = "《" + self.title + "》 " + self.dynasty + "·" + self.author
        return poem_name

class Question():

    def __init__(self, number, question, author):
        self.number = None
        self.question = None
        self.author = None
        self.kind = None

class Completion_question(Question):

    def __init__(self, number, question, author, clues, spaces):
        self.number = number
        self.question = str(question)
        self.author = str(author)
        self.kind = "completion question"
        self.clues = clues
        self.spaces = spaces

class Multiple_question(Question):

    def __init__(self, number, question, author, question_content, choice1, choice2, choice3, choice4, v):
        self.number = number
        self.question = str(question)
        self.author = str(author)
        self.kind = "multiple question"
        self.question_content = question_content
        self.A_choice = choice1
        self.B_choice = choice2
        self.C_choice = choice3
        self.D_choice = choice4
        self.key = v

class Free_response_question(Question):

    def __init__(self, number, question, author, question_content, answer):
        self.number = number
        self.question = str(question)
        self.author = str(author)
        self.kind = "free response question"
        self.question_content = question_content
        self.answer = answer
