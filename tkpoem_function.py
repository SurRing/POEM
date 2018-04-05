#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tkpoem_windows import *

# 获取诗歌信息
def get_poem(poem):
    content = poem_name(poem) + '\n'#将标题加入content
    for section in poem['content']:#遍历每一个段落
        for whole_sentence in section:#遍历每一个整句
            for sentence in whole_sentence:#遍历每一个句
                content += sentence#将该句加入content
        content += '\n'#在段尾换行
    return content#返回诗内容

def poem_name(poem):
    poem_name = "《" + poem["title"] + "》 " + poem["dynasty"] + "·" + poem["author"]
    return poem_name