from flask import request, redirect, url_for, render_template, flash, session, send_from_directory, jsonify, json
from labelingImage import app
from werkzeug.utils import secure_filename
import glob
import os
import shutil
from functools import wraps
# kerasとの連携モジュール
# from keras import models
# from PIL import Image
# import io

# 0.loginデコレータの作成
def login_required(views):
    @wraps(views)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return views(*args, **kwargs)
    return inner

# フォルダの絶対パスを指定
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
#------------------------------------------------------------------------
# 2.Home画面
@app.route('/')
@login_required
def show_entries():
    # if not session.get('logged_in'):
    #     return redirect('login')
    # return render_template('entries/index.html')
    return render_template('upload.html')
#------------------------------------------------------------------------

# 1.この画面が表示される
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            print('Invalid Username !')
        elif request.form['password'] != app.config['PASSWORD']:
            print('Invalid Password !')
        else:
            session['logged_in'] = True
        return redirect('/')
    return render_template('login.html')
#------------------------------------------------------------------------

# 3. ログアウトの際はログインページに戻る
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')
#------------------------------------------------------------------------

# 4. 画像をディレクトリに保存
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    target = os.path.join(APP_ROOT, 'static/images')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)
#----------------------------------------------------------------------

# @app.route('/upload/<filename>')
# @login_required
# def send_image(filename):
#     return send_from_directory("images", filename)
#------------------------------------------------------------------------

# 5. labeling image
@app.route('/classify', methods=['GET','POST'])
@login_required
def classify():
    # get image path
    img_path = glob.glob(os.path.join(APP_ROOT, "static/images/*.jpg"))
    # get labeled folder name
    category_path = [os.path.basename(path) for path in glob.glob(os.path.join(APP_ROOT, "static/labeled/*"))]
    # print(category_path)
    # if img_path is None:
    #     print("Your are already finished !")
    # else:
    return render_template('classify.html', img=[os.path.basename(r) for r in glob.glob(img_path[0])][0],category_list=category_path)

# 6. move images
@app.route('/moving', methods=['POST'])
@login_required
def moving():
    # get labeled folder path
    category_path = os.path.join(APP_ROOT, os.path.join("labeled", request.form['category']))
    print(category_path)
    # move files
    shutil.move(request.form['img_path'], category_path)
    print(">>>>>>>>>>>>>>>>>>>>>>>1",request.form['img_path'])
    return redirect("/classify")

#------------------------------------------------------------------------

# 7. send local file
# @app.route('/send', methods=['POST'])
# @login_required
# def sending():
