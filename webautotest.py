#coding=utf-8
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request
import time
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF','xmind'])

@app.route('/', methods=['GET', 'POST'])
def home():
    return (render_template('homepage.html'))


@app.route('/signin', methods=['GET'])
def signin_form():
    return (render_template('loginpage.html'))

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    
    if request.form['username']=='000000' and request.form['password']=='000000':
        return (render_template('welcomepage.html',username=request.form['username']))
    return (render_template('loginpage.html',message='用户名验证失败'))


# 用于测试上传，稍后用到
@app.route('/test/upload')
def upload_test():
    return render_template('upload.html')

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        print('这是什么类型%s'%fname)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录

        return jsonify({"errno": 0, "errmsg": "上传成功", })
    else:
        return jsonify({"errno": 1001, "errmsg": "上传失败"})
if __name__ == '__main__':
    app.run(debug=True)


