前端设计手册
===

目录结构
---
Templates

	├─css             (存放样式文件)
	├─except          (存放HTTP异常页面)
	├─images          (存放静态图片)
	├─js              (存放JS脚本)
	├─archives.html   (存档页面)
	├─article.html    (文章页面)
	├─guest.html      (留言页面)
	├─index.html      (首页/文章列表页)
	├─footer.html     (底部模板)
	├─header.html     (头部模板)
	└─favicon.ico     (网站图标)

约定
---
**1.获取静态页面**

如引用js、css、jpg等文件，使用模板`{{ static_url(path) }}`来转换为静态路径，如下代码

	<link type="text/css" rel="stylesheet" href="css/style.css" />

应该表示为

	<link type="text/css" rel="stylesheet" href="{{ static_url("css/style.css") }}" />

**2.页面模板**

为避免代码重写，提供头部和底部两个模板对象。使用如下代码引用。

	{% module Header() %}
	{% module Footer() %}

该模块引用功能为将读取footer.html和header.html到页面引用位置。

**3.HTTP异常页面**

现提供403、404、500和503异常的处理页面。例如404页面，命名为[ 404.html ]放置在except目录下即可。

**4.变量引用方法**

每个模板页将提供相关功能变量在前端引用。如 [ article.html ] 页面，提供表示文章内容的数组变量[ article ]，在前端页面中引用方法为。

	`<div class="article">{{ article[1] }}</div>`