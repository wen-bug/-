import time

from app.models import redisP
from app.views.tools import setToken,get_sion,date,hash_name,hash_token,ex_data
from flask import Blueprint, jsonify, request
us=Blueprint('user',__name__)



#注册
@us.route('/sign',methods=['POST'])
def reg():
    result=request.json
    code=result['code']
    Email=result['Email']
    Account=result['account']
    pwd=result['pwd']
    if ex_data.pwd(pwd):
        return jsonify('')
    if ex_data.em(Email):
        return jsonify('')
    if ex_data.account(Account):
        return jsonify('')
    rcode = redisP.get(Email)
    res={'code':code,'email':Email,'account':Account,'pwd':pwd,'time':date()}
    if rcode!=code:
        return jsonify([{'code':22}])
    else:
        redisP.delete(Email)
        sqls='select Account,Email from user where Account=:account'
        qy=get_sion(sqls,'find',res)
        if qy[0]['code']==0:
            if Email==qy[1]:
                return jsonify([{'code':20}])
            else:
                return jsonify([{'code':21}])
        elif qy[0]['code'] == 1:
            sql="insert into user " \
                "(Email,Account,pwd,loginDate)" \
                " values(:email,:account,:pwd,:time)"
            qy=get_sion(sql,'up',res)
            if qy[0]['code']==0:
                return jsonify(qy)
            else:
                return  jsonify(qy)
        else:
            return jsonify(qy)

#登录
@us.route('/login',methods=['POST'])
def hello_world():
    result=request.get_json()
    account=result['account']
    pwd=result['pwd']
    if ex_data.pwd(pwd):
        return jsonify('pwd')
    if ex_data.account(account):
        return jsonify('account')
    res={'account':account,'pwd':pwd,'seesion':''}
    sql="select userName,Email,Account,headP,sign" \
        " from user where Account=:account and pwd=pwd"
    qy_u=get_sion(sql,'find',res)
    if qy_u[0]['code']==0:
        ss=hash_name(account)
        res['session']=ss
        sql="update user set sessioned=:session where Account=:account"
        qy=get_sion(sql,'up',res)
        if qy[0]['code']==0:
            token=hash_token(account)
            r_qy=setToken(str(account)+'token',token)
            qy_u=qy_u[1][0]
            if r_qy:
                ls=[{'code':0},{'msg':[]}]
                ls[1]['msg'].append({'userName':qy_u[0],'Email':qy_u[1],'Account':qy_u[2],'headP':qy_u[3],'sign':qy_u[4],'session':ss,'token':token})
                return jsonify(ls)
            else:
                return  jsonify([{'code':24}])
        elif qy[0]['code'] == 1:
            return  jsonify([{'code':25}])
        else:
            return jsonify(qy)
    elif qy_u[0]['code'] == 1:
       return jsonify([{'code':23}])
    else:
        return jsonify(qy_u)

#sessin登录
@us.route('/checks',methods=['post'])
def checkSession():
    result=request.json['session']
    res={'session':result}
    sql="select userName,Email,Account,headP,sign from user where sessioned=:session"
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
            qy=qy[1][0]
            ls=[{'code':0},{'msg':[]}]
            token=hash_token(str(qy[2]))
            r_qy = setToken(str(qy[2]) + 'token', token)
            if r_qy:
                ls[1]['msg'].append({'userName':qy[0],'Email':qy[1],'Account':qy[2],'headP':qy[3],'sign':qy[4],'token':token})
                return jsonify(ls)
            else:
                return jsonify([{'code':25}])
    elif qy[0]['code']==1:
        return jsonify([{'cdoe':23}])
    else:
        return jsonify(qy)



