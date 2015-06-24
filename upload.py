#coding: utf8

import tornado.ioloop
import tornado.web
import os
from utils import *

class UploadFileHandler(tornado.web.RequestHandler):

	def get(self,file = ""):

		if file == "":
			self.redirect("/")

		prefix = file.split('.')[1]

		type = "application/octet-stream"

		if prefix == "jpg":
			type = "image/jpeg"

		elif prefix == "png":
			type = "image/png"

		elif prefix == "bmp":
			type = "application/x-bmp"

		elif prefix == "gif":
			type = "image/gif"

		elif prefix == "mp3":
			type = "audio/mp3"

		elif prefix == "mp4":
			type = "video/mpeg4"

		elif prefix == "html" or prefix == "txt" or prefix == "htm":
			type = "text/html"


		self.set_header ('Content-Type', type)

		#self.set_header ('Content-Disposition', 'attachment; filename='+file)

		#读取的模式需要根据实际情况进行修改
		with open(cur_dir() + C('upload')+file, 'rb') as f:
			while True:
				data = f.read(1000)
				if not data:
					break
				self.write(data)

		#记得有finish哦
		self.finish()

	def post(self,file = ""):

		upload_path = cur_dir() + C('upload')  

		#提取表单中‘name’为‘file’的文件元数据
		file_metas=self.request.files['file']	
		for meta in file_metas:

			filename=meta['filename']
			filepath=os.path.join(upload_path,filename)

			#有些文件需要已二进制的形式存储，实际中可以更改
			with open(filepath,'wb') as up:	  
				up.write(meta['body'])

			self.write('finished!')