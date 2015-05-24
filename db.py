#coding : utf8
import sqlite3
from utils import *

g_db = 0

g_article  = {}
g_comment  = {}
g_guest = []

#获得归档列表
def get_archives():

	archives = {}

	for key in g_article.keys():

		it = g_article[key]

		date = it[4]

		date = date.split("-")

		if archives.has_key(date[0]):
			archives[date[0]].append(it)
		else:
			archives[date[0]] = [it]


	archives.keys().sort()
	return archives


#获取数据库中得信息
def get_article():
	articles = g_article.values()
	articles.sort(key = lambda x : x[0],reverse = True)

	#将元组转为列表，并切分文章内容
	for i in range(0,len(articles)):
		articles[i] = list(articles[i])
		articles[i][2] = articles[i][2].split(C('split_sign'))

	return articles

#通过id获得文章
def get_atcbyid(id):

	#将元组转为列表，合并文章内容
	atc = list(g_article[int(id)])
	atc[2] = atc[2].replace(C('split_sign'),"")
	return atc

#从id获得评论
def get_commbyid(id):
	
	if g_comment.has_key(int(id)):
		return g_comment[int(id)]
	else:
		return []

#获得留言
def get_guest():

	return g_guest


#数据库初始化相关
def init_article():

	global g_article
	
	g_article = {}

	result = g_db.execute("select * from article")
	for row in result:
		g_article[int(row[0])] = row

#初始化评论
def init_comment():

	global g_comment
	
	g_comment = {}

	result = g_db.execute("select * from comment")

	for row in result:
		if g_comment.has_key(int(row[0])):
			g_comment[int(row[0])].append(row)
		else:
			g_comment[int(row[0])] = [row]

#初始化留言
def init_guest():

	global g_guest
	
	g_guest = []

	result = g_db.execute("select * from guest")

	for row in result:
		g_guest.append(row)
		

#打开和关闭数据库链接
def connectdb(path):
	
	global g_db
	
	g_db = sqlite3.connect(cur_dir()+path)
		
def closedb():
	
	g_db.close()

#初始化数据库
def initdb(path):

	global g_db

	try:
		connectdb(path)
		init_article()
		init_comment()
		init_guest()
		
		closedb()
		
		return True
	except:
		return False

