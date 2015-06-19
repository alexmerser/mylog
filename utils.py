#coding : utf8

import sys
import os
import sqlite3
import config

import time
import re

#空白字符转义
def Space2Char(content):
	content = content.replace("\"","\\mh")
	content = content.replace("\'","\\yh")
	content = content.replace("\n","\\n")
	content = content.replace("\r","\\r")

	return content

#转义字符
def Char2Space(content):
	content = content.replace("\\mh","\"")
	content = content.replace("\\yh","\'")
	content = content.replace("\\n","\n")
	content = content.replace("\\r","\r")

	return content

#获取网站配置
def C(key = ''):
	return config.options if (key == '') else config.options[key]

#得到当前时间
def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

#获取网站根路径
def cur_dir():
	path = sys.path[0]

	if os.path.isdir(path):
		return path + '/'
	elif os.path.isfile(path):
		return os.path.dirname(path) + '/'

#求前台模板url
def template_url(path):
	return "/static/"+ C("tmp_name") + path;

#求管理模板
def admin_url(path):
	return "/static/"+ "admin/" + path;


#获取静态路径
def tmp_dir(file):
	return cur_dir() + C('templates') + C("tmp_name") + file

#获取管理员路径
def admin_dir(file):
	return cur_dir() + C('templates') + "admin/" + file

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

#获取一个PY文件里所有函数
def get_filefunc(filename):

	import api

	ret = {}

	rex = 'def\s([^\s]*)\('

	fp = open(filename,'r')

	if fp != None:
		data = fp.read()

		l = re.findall(rex,data)

		for i in l:
			ret[i] = eval("api.%s" % i)

	return ret

	