#coding : utf8

import sys
import os
import sqlite3
import config

#获取网站配置
def C(key = ''):
	return config.options if (key == '') else config.options[key]

#获取网站根路径
def cur_dir():
	path = sys.path[0]

	if os.path.isdir(path):
		return path + '/'
	elif os.path.isfile(path):
		return os.path.dirname(path) + '/'

#获取模板路径
def tmp_dir(file):
	return cur_dir() + C('templates') + file

#文章列表分页
def split_list(list,num):

	newlist = []
	tmplist = []

	i = 0
	for it in list:
		if i == num:
			newlist.append(tmplist)
			tmplist = []
			i = 0
		tmplist.append(it)