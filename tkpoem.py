#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import tkinter
import random
import os

from tkpoem_import import *
from tkpoem_windows import *
"""
def tree_grow(tree, sum, n):
    print(sum, n, tree.level, 2 ** (tree.level))
    if sum >= (2 ** (tree.level)) * 50 - 50:
        tree = Tree((tree.level + 1) * 50 - 50, n, tree.level + 1, right=tree)
        print(sum, n, tree.level, 2 ** (tree.level), 'n')
    elif tree.right != None and sum >= tree.value + (tree.level - 1) * 50 - 50:
        if tree.left == None:
            tree.left = Tree(tree.value + (tree.level - 1) * 50 - 50, n, tree.level - 1)
        else:
            tree_grow(tree.left, sum, n)
"""
class Poem():

    def __init__(self):
        self.current_dirname = os.path.dirname(os.path.realpath(__file__))#获取文件当前目录
        self.start()
        self.finish_class, self.citing_class = poem_classic(self.all_poem_list)
        self.root = tkinter.Tk()#创建根窗口
        self.all_poem_button = tkinter.Button(self.root, text='预览所有', command=self.all_poem)#创建【预览所有】按钮
        self.all_poem_button.pack()#放置【预览所有】按钮
        self.random_test_button = tkinter.Button(self.root, text='随机测试', command=self.random_test)  # 创建【随机测试】按钮
        self.random_test_button.pack()  # 放置【随机测试】按钮
        self.new_poem_button = tkinter.Button(self.root, text='导入新诗', command=self.new_poem)  # 创建【导入新诗】按钮
        self.new_poem_button.pack()  # 放置【导入新诗】按钮
        self.load_button = tkinter.Button(self.root, text='读入', command=self.load)  # 创建【读入】按钮
        self.load_button.pack()  # 放置【读入】按钮
        self.dump_button = tkinter.Button(self.root, text='存储', command=self.dump)  # 创建【存储】按钮
        self.dump_button.pack()  # 放置【存储】按钮
        self.design_button = tkinter.Button(self.root, text='出题', command=self.design)  # 创建【出题】按钮
        self.design_button.pack()  # 放置【出题】按钮
        self.judge_button = tkinter.Button(self.root, text='审题', command=self.judge)  # 创建【审题】按钮
        self.judge_button.pack()  # 放置【审题】按钮
        self.answer_button = tkinter.Button(self.root, text='答题', command=self.answer)  # 创建【审题】按钮
        self.answer_button.pack()  # 放置【答题】按钮
        self.tea_button = tkinter.Button(self.root, text='茶室', command=self.tea)  # 创建【茶室】按钮
        self.tea_button.pack()  # 放置【茶室】按钮
        self.debug_button = tkinter.Button(self.root, text='debug', command=self.debug)  # 创建【debug】按钮
        self.debug_button.pack()  # 放置【debug】按钮

    def start(self):
        self.all_poem_list = []
        for poem_json in os.listdir("%s/poem" % (self.current_dirname)):
            if poem_json[-6:-5] == "1":
                poem = information_pickle_load("%s/poem/%s"%(self.current_dirname, poem_json))
                self.all_poem_list.append(poem)
                print(poem.poem_name())
        # self.debug()

    # 试图创建预览所有窗口
    def all_poem(self):
        try:
            self.all_poem_window.window.destroy()
        except:
            pass
        self.all_poem_window = all_poem_window(self.all_poem_list)

    # 试图创建随机测试窗口
    def random_test(self):
        try:
            self.random_test_window.window.destroy()
        except:
            pass
        self.random_test_window = random_test_window(self.all_poem_list, self.finish_class, self.citing_class, self.current_dirname)

    # 试图创建导入新诗窗口
    def new_poem(self):
        try:
            self.new_poem_window.window.destroy()
        except:
            pass
        self.new_poem_window = new_poem_window(self.all_poem_list, self.current_dirname)

    # 试图创建显示诗歌窗口
    def show_poem(self, ev=None):
        try:
            self.show_poem_window.window.destroy()
        except:
            pass
        self.show_poem_window = show_poem_window()

    def load(self):
        self.all_poem_list = []
        for poem_json in os.listdir("%s/poem" % (self.current_dirname)):
            poem = information_pickle_load("%s/poem/%s"%(self.current_dirname, poem_json))
            self.all_poem_list.append(poem)
            print(poem.poem_name())
        try:
            self.load_window.window.destroy()
        except:
            pass
        self.load_window = message_window("已读取")

    def dump(self):
        for poem in self.all_poem_list:
            information_pickle_dump(poem, "%s/poem/【%d】%s1.json" % (self.current_dirname, poem.number, poem.poem_name()))
        try:
            self.dump_window.window.destroy()
        except:
            pass
        self.dump_window = message_window("已存储")

    def design(self):
        try:
            self.design_window.design_window.destroy()
        except:
            pass
        self.design_window = design_window(self.current_dirname)

    def judge(self):
        try:
            self.judge_window.window.destroy()
        except:
            pass
        self.judge_window = message_window("该功能未完成")

    def answer(self):
        try:
            self.answer_window.window.destroy()
        except:
            pass
        self.answer_window = message_window("该功能未完成")

    def tea(self):
        try:
            self.tea_window.window.destroy()
        except:
            pass
        self.tea_window = message_window("该功能未完成")

    def debug(self):
        for poem in self.all_poem_list:
            poem.mark = 0
        self.finish_class, self.citing_class = poem_classic(self.all_poem_list)

def main():
    poem = Poem()
    tkinter.mainloop()

if __name__ == '__main__':
    main()