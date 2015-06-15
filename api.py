#coding: utf8

import db

#通过页数得到文章列表
def get_atcbypage(page):
	articlelist = db.get_atcbypage(page)
	for i in range(0,len(articlelist)):
		articlelist[i][3] = articlelist[i][3].split(' ')[0]

	return articlelist


#通过文章ID得到文章
def get_atcbyid(id):
	article = db.get_atcbyid(id)
	article[3] = article[3].split(' ')[0]

	return article

#得到全部留言
def get_guest():
	return db.get_guest()

#得到存档年薪
def get_years():
	archives = db.get_archives()
	years = archives.keys()

	return years

#得到存档页
def get_archives():

	archives = db.get_archives()
	years = archives.keys()
	for year in years:
		for i in range(0,len(archives[year])):
			archives[year][i][3] = archives[year][i][3].split(' ')[0]

	return archives

#通过ID得到评论
def get_commbyid(id):
	return db.get_commbyid(id)

#得到最大页数
def get_maxpages():
	return db.get_maxpages()

#得到上一页页数
def get_frontpage(id):
	return int(id) - 1

#得到下一页
def get_nextpage(id):
	return int(id) + 1 if db.get_maxpages() > int(id) else 0
