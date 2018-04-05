#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import tkinter

from tkpoem_choose import *
from tkpoem_function import *

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
            self.list.insert(tkinter.END,
                                             "《" + poem["title"] + "》 " + poem["dynasty"] + "·" + poem["author"])
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

# 随机测试窗口
class random_test_window():

    def __init__(self, all_poem_list, sum_sentence_list):
        self.window = tkinter.Toplevel()
        self.window.geometry('300x130')

        test_poem_name, test_print, key_print = choose_test_sentence(all_poem_list, sum_sentence_list)

        self.name_label = tkinter.Label(self.window, text=test_poem_name)
        self.name_label.pack()
        self.test_label = tkinter.Label(self.window, text=test_print)
        self.test_label.pack()
        self.key_label = tkinter.Label(self.window, text=key_print)
        self.key_button = tkinter.Button(self.window, text="显示答案",
                                                   command=self.key_label.pack)
        self.key_button.pack()
        self.next_button = tkinter.Button(self.window, text="下一个", comman=lambda:next_poem_test(self, all_poem_list, sum_sentence_list))
        self.next_button.pack()

# 导入新诗窗口
class new_poem_window():

    def __init__(self, all_poem_list, sum_sentence_list):
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

        tkinter.Button(self.window, text="confirm", command=lambda:self.get_new_poem(all_poem_list, sum_sentence_list)).grid(row=4)

    def get_new_poem(self, all_poem_list, sum_sentence_list):
        poem = {"title":self.title_entry.get(), "dynasty":self.dynasty_entry.get(), "author":self.author_entry.get(), "content":[]}
        sum_sentence = 0
        section_flag = 0
        sentence_flag = 0
        section = []
        whole_sentence = []
        sentence = ""
        for char in self.text.get("0.0", "end") + "\n":
            if char == "\n" and section_flag == 1:
                poem["content"].append(section)
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
        sum_sentence_list.append(sum_sentence)
        poem["sentence_number"] = sum_sentence
        all_poem_list.append(poem)
        print(poem["title"], "is completed.")
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