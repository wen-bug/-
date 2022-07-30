from flask import Blueprint, jsonify, request
from app.views.tools import get_sion,date,check_token,ex_data
fd = Blueprint('finds', __name__)
# 查看文章 标题
@fd.route('/find_blog',methods=['post'])
def getf():
    res=request.json
    find=res['find']
    page=res['page']
    res={'find':'%'+find+'%','page':page}
    sql="select blogs.id,blogs.title,blogs.brief,blog_data.page_view" \
        " from blogs left join blog_data on blogs.id=blog_data.blog_id " \
        "where title like :find limit :page,10"
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        ls=[qy[0],{'msg':[]}]
        for i in qy[1]:
            ls[1]['msg'].append({'id':i[0],'title':i[1],'brief':i[2],'view':i[3]})
        return jsonify(ls)
    elif qy[0]['code']==1:
        return jsonify(qy)
    else:
        return  jsonify(qy)



@fd.route('/get_user', methods=['post'])
def getu():
    res = request.json
    find = res['find']
    page = res['page']
    account=res['account']
    resd={'find':'%'+find+'%','page':page,'account':account,'in':''}
    sql = "select headP,sign,userName,Account,Email from user where userName like :find limit :page,10 "
    qy=get_sion(sql,'find',resd)
    if qy[0]['code']==1:
            return jsonify(qy)
    elif qy[0]['code']==0:
            id=[]
            res = [{'code':0}, {'msg':[]}]
            for i in qy[1]:
                id.append(str(i[3]))
                res[1]['msg'].append({'headP': i[0], 'sign': i[1], 'userName': i[2],'Account':i[3],'watch':'','email':i[4]})
            if account=='':
                return jsonify(res)
            else:
                k=",".join(id)
                resd['in'] =k
                sql = "select star from fans where fan=:account and star in (:in) "
                qy=get_sion(sql,'find',resd)
                if qy[0]['code']==0:
                    for i in range(len(res[1]['msg'])):
                        for j in range(len(qy[1])):
                            if res[1]['msg'][i]['Account']==qy[1][j][0]:
                                res[1]['msg'][i]['watch']='true'
                    return jsonify(res)
                else:
                    return jsonify(res)
    else:
       return jsonify(qy)

@fd.route('/to_watch',methods=['post'])
def tw():
    res=request.json
    account=res['account']
    star=res['star']
    token=res['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')

    res={'account':account,'star':star,'time':date()}
    if account==star:
        return jsonify([{'code':29}])
    sql='select count(*) from fans where star=:star and fan=account'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        if qy[1][0][0] != 0:
            return jsonify([{'code': 26}])
        else:
            sql="insert into fans (star,fan,time) values(:star,:account,:time)"
            qy=get_sion(sql,'up',res)
            if qy[0]['code']==0:
                return jsonify(qy)
            else:
                return jsonify(qy)
    else:
        return jsonify([qy[0]])

@fd.route('/overlook',methods=['post'])
def ol():
    res=request.json
    account=res['account']
    star=res['star']
    res={'account':account,'star':star}
    sql = 'select id from fans where star=:star and fan=:account'
    qy = get_sion(sql, 'find',res)
    if qy[0]['code'] == 0:
        sql = "delete  from fans where star=:star and fan=:account"
        qy = get_sion(sql, 'up',res)
        if qy[0]['code'] == 0:
            return jsonify(qy)
        else:
            return jsonify(qy)
    else:
        return jsonify([qy[0]])