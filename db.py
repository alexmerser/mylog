#coding : utf8
import sqlite3
import time
from utils import *

db = 0

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

def add_article(title,content):

	date = GetNowTime() 

	db = connectdb()

	sql = 'insert into article values(null,"%s","%s","%s",0)' % (title,content,date)

	db.execute(sql)

	db.commit()

	closedb(db)

	init_article()

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
	
	db = connectdb()

	g_article = {}

	result = db.execute("select * from article")
	for row in result:
		g_article[int(row[0])] = row

	closedb(db)

#初始化评论
def init_comment():

	global g_comment
	
	db = connectdb()

	g_comment = {}

	result = db.execute("select * from comment")

	for row in result:
		if g_comment.has_key(int(row[0])):
			g_comment[int(row[0])].append(row)
		else:
			g_comment[int(row[0])] = [row]

	closedb(db)

#初始化留言
def init_guest():

	global g_guest
	
	db = connectdb()

	g_guest = []

	result = db.execute("select * from guest")

	for row in result:
		g_guest.append(row)
	
	closedb(db)

#打开和关闭数据库链接
def connectdb():
	
	return sqlite3.connect(cur_dir()+C("db_path"))
		
def closedb(db):
	
	db.close()

#初始化数据库
def initdb():

	try:
		init_article()
		init_comment()
		init_guest()

		return True
	except:
		return False

