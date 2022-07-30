from flask import request, Blueprint, jsonify
from app.models import redisP
from app.views.tools import allowed_file, hash_name,get_sion,check_token,ex_data
# 更改为安全文件名
from werkzeug.utils import secure_filename
import os


pl = Blueprint('personal', __name__)


# 更换头像
@pl.route('/upimg', methods=['post'])
def upimg():
    resM = [{'code': '0'}]
    account = request.form['account']
    token=request.form['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')
    if 'file' not in request.files:
        resM[0]['code'] = -1
        print('no file part')
        return jsonify(resM)
    file = request.files['file']
    if file.filename == '':
        resM[0]['code'] = 1
        print('No selected file')
        return jsonify(resM)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print('name',filename)
        name = hash_name(filename)
        file.save(os.path.join('D:\myflask\mydata\head', name+'.'+filename.split('.')[1]))

        res={'account':account,'path':'head/' + name+'.'+filename.split('.')[1]}
        sql = "update user set headP=:path where Account=:account "
        qy = get_sion(sql,'up',res)
        if qy[0]['code']==0:
            return jsonify([{'code':0}])
        else:
            return jsonify(qy)

# 修改资料
@pl.route('/up_pl', methods=['post'])
def up_pl():
    res = request.json
    account=res['account']
    name = res['name']
    sign = res['sign']
    token=res['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')

    res={'name':name,'account':account,'sign':sign}
    sql="update user set userName=:name,sign=:sign where Account=:account"
    qy=get_sion(sql,'up',res)
    if qy[0]['code']==0:
        return jsonify(qy)
    else:
        return jsonify(qy)

# 修改邮箱
@pl.route('/up_em',methods=['post'])
def up_em():
    res=request.json
    account=res['account']
    em=res['email']
    new_email=res['new_email']
    code=res['code']
    token = res['token']
    if ex_data.em(em):
        return jsonify('')
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    if ex_data.account(account):
        return jsonify('')
    res={'account':account,'em':em,'email':new_email}
    s_code=redisP.get(em)
    if code==s_code:
        sql="select id from user where email=:email"
        qy=get_sion(sql,'find',res)
        if qy[0]['code']==0:
            return jsonify([{'code':20}])
        elif qy[0]['code']==1:
            sql="update user set email=:email where Account=:account and email=:em"
            qy=get_sion(sql,'up',res)
            return jsonify(qy)
        else:
            return jsonify(qy)
    else:
        return jsonify([{'code':22}])
# 修改密码
@pl.route('/up_pw',methods=['post'])
def up_pw():
    res=request.json
    pwd=res['npwd']
    code=res['code']
    account=res['account']
    em = res['email']
    print(pwd)
    if ex_data.account(account):
        return jsonify('')
    if ex_data.em(em):
        return jsonify('')
    res={'pwd':pwd,'account':account,'em':em}
    s_code=redisP.get(em)
    if s_code==code:
        sql=0
        if account==0:
            sql="update user set pwd=:pwd where Email=:em"
        else:

            sql="update user set pwd=:pwd where Account=:account"
        qy=get_sion(sql,'up',res)
        if qy[0]['code']==0:
            return jsonify(qy)
        else:
            return jsonify(qy)
    else:
        return jsonify([{'code':22}])

# 查询标签
@pl.route('/find_label',methods=['post'])
def fl():
    res=request.json
    account=res['account']

    token=res['token']
    if ex_data.account(account):
        return jsonify('')
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    res = {'account': account}
    sql='select id,tag from label where account=:account'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        ls=[{'code':0},{'msg':[]}]
        for i in qy[1]:
            ls[1]['msg'].append(i[1])
        return jsonify(ls)
    else:
        return jsonify(qy)
# 删除标签
@pl.route('/del_label',methods=['post'])
def dl():
    res=request.json
    account=res['account']
    name=res['name']
    token=res['token']
    if ex_data.account(account):
        return jsonify('')
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    res={'account':account,'name':name}
    sql="delete from label where tag=:name and account=:account"
    qy=get_sion(sql,'up',res)
    return jsonify(qy)
#添加标签
@pl.route('/add_label',methods=['post'])
def al():
    res=request.json
    account = res['account']
    tag=res['tag']
    token = res['token']
    if ex_data.account(account):
        return jsonify('')
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    res={'account':account,'tag':tag}
    sql='select count(*) from label where account=:account'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        if len(qy[1])>5:
            return jsonify([{'code':31}])
        else:
            sql="insert into label (account,tag) values(:account,:tag)"
            qy=get_sion(sql,'up',res)
            if qy[0]['code']==0:
                return jsonify(qy)
            else:
                return  jsonify(qy)
    elif qy[0]['code']==1:
        sql = "insert into label (account,tag) values(:account,:tag)"
        qy = get_sion(sql, 'up',res)
        if qy[0]['code'] == 0:
            return jsonify(qy)
        else:
            return jsonify(qy)
    else:
        return jsonify(qy)