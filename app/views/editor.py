from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
from app.views.tools import allowed_file,file_path,get_sion,hash_name,date,xss,ex_data,check_token

ed = Blueprint('ed', __name__)

#文章图片
@ed.route('/editor/upimg', methods=['post'])
def upload():
    # 0=ture
    resM = {'errno': '', 'data': []}
    account=request.form['account']
    token=request.form['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')

    if 'file' not in request.files:
        resM['errno'] = 1
        print('no file part')
        return jsonify(resM)
    file = request.files['file']
    if file.filename == '':
        resM['errno'] = 1
        print('No selected file')
        return jsonify(resM)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        name = hash_name(filename)
        file.save(os.path.join('D:\myflask\mydata\img', name+'.'+filename.split('.')[1]))
        resM['errno'] = 0
        resM['data'] = [{'url': 'http://127.0.0.1/img/' + name+'.'+filename.split('.')[1], 'alt': '',
                         'href': 'http://127.0.0.1/img/' + name+'.'+filename.split('.')[1]}]
        return jsonify(resM)

#编辑文章
# @ed.route('/editor/blogs', methods=['post'])
# def editor():
#     res = request.json
#     id=res['id']
#     txt =res['txt']
#     title=res['title']
#     brief=res['brief']
#     sql='select text from blogs where id={0}'.format(id)
#     qy=get_sion(sql,'find')
#     if qy[0]['code'] == 0:
#         sql="update blogs set title='{0}',brief={1} where id={2}".format(title,brief,id)
#         qy=get_sion(sql,'up')
#         if qy[0]['code']==0:
#             with open(file_path + txt, 'wb') as f:
#                 f.write(bytes(txt, encoding='utf-8'))
#             return jsonify(qy)
#         else:
#             return jsonify(qy)
#     else:
#         return jsonify(qy)

# 提交文章
@ed.route('/sub/blogs',methods=['post'])
def sb():
    res=request.json
    id = res['id']
    account=res['account']
    title=res['title']
    brief=res['brief']
    txt=res['txt']
    path=res['path']
    token=res['token']
    # 冗余图片
    img=res['img']

    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')

    #xss
    txt = xss(txt)
    res={'id':id,'account':account,'title':title,'brief':brief,'txt':txt,'path':path,'time':date()}
    if id=='':
        name='html/'+hash_name(title)+'.txt'
        res['txt']=name
        sql='select id from blogs where title=:title'
        qy=get_sion(sql,'find',res)
        if qy[0]['code']==0:
            return jsonify([{'code':26}])
        elif qy[0]['code']==1:
            sql="insert into blogs (account,title,brief,time,text) values(:account,:title,:brief,:time ,:txt)"
            qy=get_sion(sql,'up',res)
            if qy[0]['code']==0:
                with open(file_path+name,'wb')as f:
                    f.write(bytes(txt,'utf-8'))
                return jsonify(qy)
            else:
                return jsonify(qy)
        else:
            return jsonify(qy)
    else:
        sql="update blogs set title=:title,brief=:brief where id=id"
        qy=get_sion(sql,'up',res)
        if qy[0]['code']==0:
            with open(file_path+path,'wb')as f:
                f.write(bytes(txt,'utf-8'))
            return jsonify(qy)
        return jsonify(qy)
# 查看文章
@ed.route('/view_blog',methods=['post'])
def vb():
    res=request.json
    id=res['id']
    res={'id':id}
    sql='select text,title from blogs where id=:id'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        ls=[qy[0],{'msg':[]}]
        with  open(file_path+qy[1][0][0],'rb') as f:
            b=f.read()
            ls[1]['msg'].append({'text':qy[1][0][0],'id':id,'title':qy[1][0][1],'txt':str(b,'utf-8')})
        return jsonify(ls)
    else:
        return jsonify([qy[0]])
