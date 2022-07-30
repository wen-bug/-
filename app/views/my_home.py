from flask import Blueprint,request,jsonify
from app.views.tools import get_sion,ex_data,check_token
mh=Blueprint('myhome',__name__)

#查询粉丝,关注
@mh.route('/get_fans', methods=['post'])
def fans():
    res = request.json
    account = res['account']
    if ex_data.account(account):
        return jsonify('')
    res={'account':account}
    sql = 'select s.watch,f.by_watch' \
          ' from (select count(*) as watch from fans  where fan=:account) as s join (select count(*) as by_watch from fans where star=:account) as f'
    qy = get_sion(sql,'find',res)
    item=qy[1][0]
    if qy[0]['code']==0:
        to_res = [{'code': 0},{'msg': [{'watch': item[0], 'by_watch': item[1]}]}]
        return jsonify(to_res)
    else :
        return jsonify(qy)

# 查看文章 账号
@mh.route('/find_blogu',methods=['post'])
def getf():
    res=request.json
    account=res['account']
    page=res['page']
    if ex_data.account(account):
        return jsonify('')
    res={'account':account,'page':page}
    sql="select blogs.id,blogs.title,blogs.brief,blog_data.page_view" \
        " from blogs left join blog_data on blogs.id=blog_data.blog_id " \
        "where blogs.account=:account limit :page,10"
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

# 查看用户
@mh.route('/my_user',methods=['post'])
def mu():
    res = request.json
    account=res['account']
    if ex_data.account(account):
        return jsonify('')
    res={'account':account}
    sql = "select headP,sign,userName,Account,Email from user where Account=account  "
    qy=get_sion(sql,'find',res)
    li=qy[1][0]
    if qy[0]['code'] == 0:
        ls = [qy[0], {'msg': [{'headP': li[0], 'sign': li[1], 'userName': li[2],'Account': li[3],'email': li[4]}]}]
        return jsonify(ls)
    else:
        return jsonify(qy)
#查询收藏夹
# @mh.route('/collect_folder',methods=['post'])
# def folder():
#     res=request.json
#     account=res['account']
#
#     sql='select id,folder,account from collect_folder where account={0}'.format(account)
#     qy=get_sion(sql,'find')
#     to_res=[]
#     if qy[0]['code']==0:
#         for i in qy[1]:
#             to_res.append({'id':i[0],'folder':i[1],'account':i[2]})
#         return  jsonify(to_res)
#     else:
#         return jsonify([qy[0]])


#查询收藏
# @mh.route('/collect',methods=['post'])
# def collect():
#     res = request.json
#     folder_id = res['folder_id']
#     print(folder_id)
#
#     sql = 'select collect.blog_id,blogs.title,blogs.brief ' \
#           'from collect join blogs on collect.blog_id=blogs.id ' \
#           'where collect.folder_id={0}'.format(folder_id)
#     qy = get_sion(sql,'find')
#     to_res = []
#     if qy[0]['code']==0:
#         for i in qy[1]:
#             to_res.append({'blog_id': i[0], 'title': i[1],'brief':i[2]})
#         return jsonify(to_res)
#     else:
#         return jsonify(qy)

#查询关注
@mh.route('/watch',methods=['post'])
def watch():
    res = request.json
    u=res['u']
    page = res['page']
    account=res['account']
    print(u)
    if ex_data.account(account):
        print(1)
        return jsonify('')
    # if ex_data.account(u):
    #     print(2)
    #     return jsonify('')

    resd={'u':u,'page':page,'account':account,'star':''}

    sql = "select user.headP,user.sign,user.userName,user.Account,user.Email from fans join user on user.Account=fans.star where fan=:account limit :page,10 "
    qy=get_sion(sql,'find',resd)
    if qy[0]['code']==0:
        res = [{'code': 0}, {'msg': []}]
        id=[]
        for i in qy[1]:
            id.append(str(i[3]))
            res[1]['msg'].append({'headP': i[0], 'sign': i[1], 'userName': i[2],'Account':i[3],'watch':'','email':i[4]})
        if u!='':
            resd['star']=",".join(id)
            sql="select star from fans where fan=:u and star in (:star) "
            qy=get_sion(sql,'find',resd)
            if qy[0]['code'] == 0:
                for i in range(len(res[1]['msg'])):
                    for j in range(len(qy[1])):
                        if res[1]['msg'][i]['Account'] == qy[1][j][0]:
                            res[1]['msg'][i]['watch'] = 'true'
        return jsonify(res)
    else:
        return jsonify(qy)
