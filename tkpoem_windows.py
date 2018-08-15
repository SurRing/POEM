#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import tkinter
import os

from tkpoem_choose import *
from tkpoem_function import *

from tkpoem_import import *

#提示框窗口
class message_window():

    def __init__(self, message):
        self.window = tkinter.Toplevel()
        self.label = tkinter.Label(self.window, text=message)
        self.label.pack()

# 预览所有窗口
class all_poem_window():

    def __init__(self, all_poem_list):
        self.all_poem_list = all_poem_list

        self.window = tkinter.Toplevel()  # 创建【预览所有】顶层窗口

        self.frame = tkinter.Frame(self.window)  # 创建【预览所有】框架
        self.scroll_bar = tkinter.Scrollbar(self.frame)  # 创建【预览所有】滑条
        self.list = tkinter.Listbox(self.frame, height=15, width=50,
                                                    yscrollcommand=self.scroll_bar.set)  # 创建【预览所有】列表

        for poem in all_poem_list:  # 将诗导入列表
            self.list.insert(tkinter.END,poem.poem_name())
        # self.all_poem_window_list.config(selectbackground='red')#选中时背景变红
        self.list.bind('<Double-1>', self.show_poem)  # 双击左键时显示内容

        self.scroll_bar.config(command=self.list.yview)  # 绑定滑条到列表

        self.scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # 放置【预览所有】滑条
        self.list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)  # 放置【预览所有】列表
        self.frame.pack()  # 放置框架

    # 试图创建显示诗歌窗口
    def show_poem(self, ev=None):
        try:
            self.show_poem_window.window.destroy()
        except:
            pass
        self.show_poem_window = show_poem_window()

        self.show_poem_window.text.insert(tkinter.END, get_poem(self.all_poem_list[self.list.curselection()[0]]))
        if self.all_poem_list[self.list.curselection()[0]].mark >= 4:
            self.show_poem_window.text.insert(tkinter.END, "已习得")
        else:
            self.show_poem_window.text.insert(tkinter.END, "未掌握")

# 随机测试窗口
class random_test_window():

    def __init__(self, all_poem_list, finish_class, citing_class, current_dirname):
        self.flag = 0

        self.window = tkinter.Toplevel()
        self.window.geometry('300x150')

        self.test_poem, test_print, key_print = choose_test_sentence(all_poem_list, finish_class, citing_class)

        self.name_label = tkinter.Label(self.window, text=self.test_poem.poem_name())
        self.name_label.grid()
        self.test_label = tkinter.Label(self.window, text=test_print)
        self.test_label.grid()
        self.key_label = tkinter.Label(self.window, text=key_print)
        self.key_button = tkinter.Button(self.window, text="会",
                                                   command=self.y)
        self.key_button.grid(column=0)
        self.key_button = tkinter.Button(self.window, text="不会",
                                                   command=self.n)
        self.key_button.grid(row=2, column=1)
        self.next_button = tkinter.Button(self.window, text="下一个", comman=lambda:self.next(all_poem_list, finish_class, citing_class, current_dirname))
        self.next_button.grid()

    def y(self):
        self.key_label.grid()
        self.flag = 1

    def n(self):
        self.key_label.grid()
        self.flag = 1

    def next(self, all_poem_list, finish_class, citing_class, current_dirname):
        self.test_poem.mark += self.flag
        if self.test_poem.mark < 0:
            self.test_poem.mark = 0
        if self.flag > 0 and self.test_poem.mark == 4:
            citing_class.remove(self.test_poem.number)
            finish_class.append(self.test_poem.number)
        elif self.flag < 0 and self.test_poem.mark == 3:
            finish_class.remove(self.test_poem.number)
            citing_class.append(self.test_poem.number)
        self.flag = 0
        #all_poem_list[test_poem.number].mark = test_poem.mark
        information_pickle_dump(self.test_poem, "%s/poem/【%d】%s.json" % (current_dirname, self.test_poem.number, self.test_poem.poem_name()))
        self.key_label.grid_remove()
        self.test_poem, test_print, key_print = choose_test_sentence(all_poem_list, finish_class, citing_class)
        self.name_label.config(text=self.test_poem.poem_name())
        self.test_label.config(text=test_print)
        self.key_label.config(text=key_print)

# 导入新诗窗口
class new_poem_window():

    def __init__(self, all_poem_list, current_dirname):
        self.window = tkinter.Toplevel()  # 创建显示顶层窗口
        tkinter.Label(self.window, text="title").grid(row=0, column=0,columnspan=1)
        self.title_entry = tkinter.Entry(self.window)
        self.title_entry.grid(row=0, column=1, columnspan=2)
        tkinter.Label(self.window, text="dynasty").grid(row=1, column=0,columnspan=1)
        self.dynasty_entry = tkinter.Entry(self.window)
        self.dynasty_entry.grid(row=1, column=1, columnspan=2)
        tkinter.Label(self.window, text="author").grid(row=2, column=0,columnspan=1)
        self.author_entry = tkinter.Entry(self.window)
        self.author_entry.grid(row=2, column=1, columnspan=2)

        self.scroll_bar = tkinter.Scrollbar(self.window)  # 创建显示拖动条
        self.text = tkinter.Text(self.window, height=10, width=40,
                                 yscrollcommand=self.scroll_bar.set)  # 创建显示文本

        self.scroll_bar.config(command=self.text.yview)  # 绑定滑条到文本

        self.scroll_bar.grid(row=3, column=2, columnspan=2)  # 放置滑条
        self.text.grid(row=3, column=0, columnspan=2)  # 放置文本

        tkinter.Button(self.window, text="confirm", command=lambda:self.get_new_poem(all_poem_list,current_dirname)).grid(row=4)

    def get_new_poem(self, all_poem_list,current_dirname):
        number = len([x for x in os.listdir("%s/poem" % (current_dirname))])
        print(number)
        content = []
        sum_sentence = 0
        section_flag = 0
        sentence_flag = 0
        section = []
        whole_sentence = []
        sentence = ""
        for char in self.text.get("0.0", "end") + "\n":
            if char == "\n" and section_flag == 1:
                content.append(section)
                section = []
                section_flag = 0
            elif (char == "。" or char == "？" or char == "！") and sentence_flag == 1:
                sentence += char
                whole_sentence.append(sentence)
                section.append(whole_sentence)
                sum_sentence += 1
                whole_sentence = []
                sentence = ""
                section_flag = 1
                sentence_flag = 0
            elif char == "，" and sentence_flag == 1:
                sentence += char
                whole_sentence.append(sentence)
                sum_sentence += 1
                sentence = ""
                sentence_flag = 0
            else:
                sentence += char
                sentence_flag = 1
        poem = Poem(number, self.title_entry.get(), self.dynasty_entry.get(), self.author_entry.get(), content, sum_sentence)
        information_pickle_dump(poem, "%s/poem/【%d】%s1.json" % (current_dirname, poem.number, poem.poem_name()))
        #all_poem_list.append(poem)
        print(poem.poem_name(), "is completed.")
        self.window.destroy()

# 显示诗歌窗口
class show_poem_window():

    def __init__(self):
        self.window = tkinter.Toplevel()  # 创建显示顶层窗口
        self.scroll_bar = tkinter.Scrollbar(self.window)  # 创建显示拖动条
        self.text = tkinter.Text(self.window, height=10, width=40,
                                                  yscrollcommand=self.scroll_bar.set)  # 创建显示文本

        self.scroll_bar.config(command=self.text.yview)  # 绑定滑条到文本

        self.scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # 放置滑条
        self.text.pack(side=tkinter.LEFT, fill=tkinter.Y)  # 放置文本

#出题窗口
class design_window():

    def __init__(self, current_dirname):
        self.design_window = tkinter.Toplevel()
        self.completion_button = tkinter.Button(self.design_window, text="填空题", command=lambda:self.completion(current_dirname))
        self.multiple_choice_button = tkinter.Button(self.design_window, text="选择题", command=lambda:self.multiple_choice(current_dirname))
        self.free_response_button = tkinter.Button(self.design_window, text="解答题", command=lambda:self.free_response(current_dirname))
        self.completion_button.grid()
        self.multiple_choice_button.grid()
        self.free_response_button.grid()

    def completion(self, current_dirname):
        self.design_window.destroy()
        self.completion_window = completion_window(current_dirname)

    def multiple_choice(self, current_dirname):
        self.design_window.destroy()
        self.multiple_choice_window = multiple_choice_window(current_dirname)

    def free_response(self):
        self.design_window.destroy()
        self.free_response_window = free_response_window()

class completion_window():

    def __init__(self, current_dirname):
        self.window = tkinter.Toplevel()
        self.question_entry = tkinter.Entry(self.window)
        self.author_entry = tkinter.Entry(self.window)
        self.care_label = tkinter.Label(self.window, text="请将需要填写的部分放在【】内")
        self.text = tkinter.Text(self.window)
        self.button = tkinter.Button(self.window, text="confirm", command=lambda:self.confirm(current_dirname))
        tkinter.Label(self.window, text="question").grid(row=0, column=0)
        self.question_entry.grid(row=0, column=1)
        tkinter.Label(self.window, text="suthor").grid(row=1, column=0)
        self.author_entry.grid(row=1, column=1)
        self.care_label.grid()
        self.text.grid()
        self.button.grid()

    def confirm(self, current_dirname):
        number = len([x for x in os.listdir("%s/question/completion question" %(current_dirname))])
        content = self.text.get("0.0", "end")
        clues = []
        spaces = []
        clue = ""
        space = ""
        space_flag = 0
        for c in content:
            if space_flag == 0:
                if c == "【":
                    space_flag = 1
                    clues.append(clue)
                    clue = ""
                else:
                    clue += c
            else:
                if c == "】":
                    space_flag = 0
                    spaces.append(space)
                    space = ""
                else:
                    space += c
        completion_question = Completion_question(number, self.question_entry.get(), self.author_entry.get(), clues, spaces)
        information_pickle_dump(completion_question, "%s/question/completion question/【%d】%s %s1.json" % (current_dirname,completion_question.number, completion_question.question, completion_question.author))
        print(completion_question.question, "is completed.")
        self.window.destroy()

class multiple_choice_window():

    def __init__(self, current_dirname):
        self.window = tkinter.Toplevel()
        self.question_entry = tkinter.Entry(self.window)
        self.author_entry = tkinter.Entry(self.window)
        self.question_text = tkinter.Text(self.window)
        self.choice1_entry = tkinter.Entry(self.window)
        self.choice2_entry = tkinter.Entry(self.window)
        self.choice3_entry = tkinter.Entry(self.window)
        self.choice4_entry = tkinter.Entry(self.window)

        self.button = tkinter.Button(self.window, text="confirm", command=lambda:self.confirm(current_dirname))
        tkinter.Label(self.window, text="question").grid(row=0, column=0)
        self.question_entry.grid(row=0, column=1)
        tkinter.Label(self.window, text="suthor").grid(row=1, column=0)
        self.author_entry.grid(row=1, column=1)
        self.question_text.grid(row=2)
        tkinter.Label(self.window, text="A选项").grid(row=3, column=0)
        self.choice1_entry.grid(row=3, column=1)
        tkinter.Label(self.window, text="B选项").grid(row=4, column=0)
        self.choice2_entry.grid(row=4, column=1)
        tkinter.Label(self.window, text="C选项").grid(row=5, column=0)
        self.choice3_entry.grid(row=5, column=1)
        tkinter.Label(self.window, text="D选项").grid(row=6, column=0)
        self.choice4_entry.grid(row=6, column=1)
        self.v = tkinter.IntVar()
        self.v.set(1)
        tkinter.Radiobutton(self.window, variable = self.v, text='A', value=1).grid(row=7, column=0)
        tkinter.Radiobutton(self.window, variable = self.v, text='B', value=2).grid(row=7, column=1)
        tkinter.Radiobutton(self.window, variable = self.v, text='C', value=3).grid(row=8, column=0)
        tkinter.Radiobutton(self.window, variable = self.v, text='C', value=4).grid(row=8, column=1)
        self.button.grid()

    def confirm(self, current_dirname):
        number = len([x for x in os.listdir("%s/question/multiple question" %(current_dirname))])

        multiple_question = Multiple_question(number, self.question_entry.get(), self.author_entry.get(),self.question_text.get("0.0", "end"),
                                              self.choice1_entry,self.choice2_entry, self.choice3_entry, self.choice4_entry, self.v.get())
        information_pickle_dump(multiple_question, "%s/question/multiple question/【%d】%s %s1.json" % (current_dirname,multiple_question.number, multiple_question.question, multiple_question.author))
        print(multiple_question.question, "is completed.")
        self.window.destroy()

class free_response_window():

    def __init__(self, current_dirname):
        self.window = tkinter.Toplevel()
        self.question_entry = tkinter.Entry(self.window)
        self.author_entry = tkinter.Entry(self.window)
        self.question_text = tkinter.Text(self.window)
        self.answer_text = tkinter.Text(self.window)
        self.button = tkinter.Button(self.window, text="confirm", command=lambda:self.confirm(current_dirname))
        tkinter.Label(self.window, text="question").grid(row=0, column=0)
        self.question_entry.grid(row=0, column=1)
        tkinter.Label(self.window, text="suthor").grid(row=1, column=0)
        self.author_entry.grid(row=1, column=1)
        self.question_text.grid()
        self.answer_text.grid()
        self.button.grid()

    def confirm(self, current_dirname):
        number = len([x for x in os.listdir("%s/question/free response question" %(current_dirname))])
        free_response_question = Free_response_question(number, self.question_entry.get(), self.author_entry.get(), self.question_text.get("0.0", "end"), self.answer_text.get("0.0", "end"))
        information_pickle_dump(free_response_question, "%s/question/free response question/【%d】%s %s1.json" % (current_dirname,free_response_question.number, free_response_question.question, free_response_question.author))
        print(free_response_question.question, "is completed.")
        self.window.destroy()
