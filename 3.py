import requests
import base64
import json,random,time,os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# 读取文件
def open_file(file_path):
    #with open(file_path, 'wb+') as f:
    #    return f.read()
    #以 utf-8 的编码格式打开指定文件
    f = open(file_path,'rb+')
    #输出读取到的数据
    return f.read()
    #关闭文件
    

# 将文件转换为base64编码，上传文件必须将文件以base64格式上传
def file_base64(data):
    data_b64 = base64.b64encode(data).decode('utf-8')
    #print(data_b64)
    return data_b64

def random_file_name():
    name = ""
    for i in range(0,15):
        a = random.choice('abcdefghijklmnopqrstuvwxyz')
        name = name+a
    
    name= name+str(int(time.time()))
    return name
        

# 上传文件
def upload_files(file_data,file_name):
    houzhui = os.path.splitext(file_name)[-1]
    file_name = random_file_name()+houzhui #文件名
    token = ""
    repository_list=["img","img1","img2","img3"]
    github_name = "mikulo"
    github_Repository = repository_list[random.randint(0,3)]
    print(github_Repository)
    url = "https://api.github.com/repos/"+github_name+"/"+github_Repository+"/contents/img/"+ file_name
    headers = {"Authorization": "token " + token}
    content = file_base64(file_data)
    data = {
        "message": "message",
        "committer": {
            "name": "mikulo",
            "email": "xxxx@gmail.com"
        },
        "content": content
    }
    data = json.dumps(data)
    req = requests.put(url=url, data=data, headers=headers)
    req.encoding = "utf-8"
    re_data = json.loads(req.text)
    #print(re_data)
    #print(re_data['content']['sha'])
    return "https://i2.wp.com/raw.githubusercontent.com/"+github_name+"/"+github_Repository+"/master/img/"+file_name
# 在国内默认的down_url可能会无法访问，因此使用CDN访问

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        file = f.read()
        print(f.filename)
        link0= upload_files(file,f.filename)
        #print(request.files)
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        link1= "[img]"+link0+r'[/img]'
        return render_template('upload.html',url_0=link0,url_1=link1)

    else:

        return render_template('upload.html',url_0=link0,url_1=link1)

if __name__ == '__main__':
   app.run(host="0.0.0.0",port=80,debug=True)

