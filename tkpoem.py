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
        self.all_poem_list, self.sum_sentence_list = poem_import("%s/poem.txt" % (self.current_dirname))#导入所有诗
        #self.finished_poem_list, self.citing_poem_list, self.queueing_poem_list = information_pickle_load("%s/finish&doing.txt" % (self.current_dirname))#导入已有信息
        self.poem_sum = len(self.all_poem_list)#获取诗的总数
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
        self.debug_button = tkinter.Button(self.root, text='debug', command=self.debug)  # 创建【debug】按钮
        self.debug_button.pack()  # 放置【debug】按钮

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
        self.random_test_window = random_test_window(self.all_poem_list, self.sum_sentence_list)

    # 试图创建导入新诗窗口
    def new_poem(self):
        try:
            self.new_poem_window.window.destroy()
        except:
            pass
        self.new_poem_window = new_poem_window(self.all_poem_list, self.sum_sentence_list)

    # 试图创建显示诗歌窗口
    def show_poem(self, ev=None):
        try:
            self.show_poem_window.window.destroy()
        except:
            pass
        self.show_poem_window = show_poem_window()

    def load(self):
        self.all_poem_list = information_pickle_load("%s/poem_store.txt" % (self.current_dirname))

    def dump(self):
        information_pickle_dump(self.all_poem_list, "%s/poem_store.txt" % (self.current_dirname))

    def debug(self):
        for poem in self.all_poem_list:
            poem["mark"] = 0

def main():
    poem = Poem()
    tkinter.mainloop()

if __name__ == '__main__':
    main()