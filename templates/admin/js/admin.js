function insert_upload(content)
{
	if ( content.indexOf(".jpg") >= 0 || content.indexOf(".png") >= 0 || content.indexOf(".gif") >= 0 )
	{
		imgtext = "<img src='/upload/" + content +"' />"
	}
	else 
	{
		imgtext = "<a href='/upload/" + content +"' >文件下载</a>"
	}
	
	$('textarea').val( $('textarea').val() + imgtext)
}
function AjaxUpload(option)
 {
        var file,
            fd = new FormData(),
            xhr = new XMLHttpRequest(),
            loaded, tot, per, uploadUrl,input;
 
        input = document.createElement("input");
        input.setAttribute('id',"myUpload-input");
        input.setAttribute('type',"file");
        input.setAttribute('name',"file");
 
        input.click();
 
        uploadUrl = option.uploadUrl;
        callback = option.callback;
        uploading = option.uploading;
        beforeSend = option.beforeSend;
 
        input.onchange= function(){
            file = input.files[0];
            if(beforeSend instanceof Function){
                if(beforeSend(file) === false){
                    return false;
                }
            }
             
            fd.append("file", file);
 
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    if(callback instanceof Function){
                        callback(xhr.responseText);
                    }
                }
            }
 
            //侦查当前附件上传情况
            xhr.upload.onprogress = function(evt) {
                loaded = evt.loaded;
                tot = evt.total;
                per = Math.floor(100 * loaded / tot); //已经上传的百分比
                if(uploading instanceof Function){
                    uploading(per);
                }
            }
 
            xhr.open("post", uploadUrl);
            xhr.send(fd);
        }
}

function UploadList()
{
	$.ajax({
		  type: 'POST',
		  url: "/admin/",
		  data: "m=get_upload",
		  success: function(data, textStatus, jqXHR){
		  	files = eval(data)

		  	html = ""

		  	for ( i = 0 ; i < files.length ; i++)
		  	{
		  		html += "<tr><td><a href=\"/upload/"+ files[i][0] +"\">"+ files[i][0] +"</a></td>"+
					"<td>"+ files[i][1] +"</td>"+
					"<td><button class=\"btn\" onclick=\"insert_upload('"+ files[i][0] +"')\" >插入</button></td>"
					+"<td><button class=\"btn\" onclick=\"DelUpFile('"+files[i][0]+"')\" >删除</button></td></tr>"

		  	}
		  	$(".upload_list").html(html)
		  }
	});
}
 
function DelUpFile(filename)
{
	$.ajax({
		  type: 'POST',
		  url: "/admin/",
		  data: "m=del_upload&filename=" + filename,
		  success: function(data, textStatus, jqXHR){
		  	alert("删除成功！")
		  	UploadList()
		  }
	});
}

//触发文件上传事件
function myUpload()
{
	AjaxUpload({
    //上传文件接收地址
    uploadUrl: "/upload/",
    //选择文件后，发送文件前自定义事件
    //file为上传的文件信息，可在此处做文件检测、初始化进度条等动作
    beforeSend: function(file) {
 
    },
    //文件上传完成后回调函数
    //res为文件上传信息
    callback: function(res) {
    	alert("上传成功！")
    	UploadList()
 
    },
    //返回上传过程中包括上传进度的相关信息
    //详细请看res,可在此加入进度条相关代码
    uploading: function(res) {
 
    }});
}