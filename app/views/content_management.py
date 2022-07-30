from flask import request,jsonify,Blueprint
from app.views.tools import get_sion,file_path,date,ex_data,check_token
cm=Blueprint('content_management',__name__)
# 查找文章
@cm.route('/find_my_b',methods=['post'])
def fm():
    res=request.json
    account=res['account']
    page=res['page']
    find=res['find']
    if ex_data.account(account):
        return jsonify('')
    res={'account':account,'page':page,'find':find}
    if find!='':
        sql="select blogs.id,blogs.title,blogs.brief,blog_data.page_view" \
        " from blogs left join blog_data on blogs.id=blog_data.blog_id " \
        "where blogs.account=:account and title like '%:find%' limit :page,10"
    else:
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
# 查询收藏文章
@cm.route('/find_collect',methods=['post'])
def fc():
    res = request.json
    account = res['account']
    page = res['page']
    id = res['id']
    if ex_data.account(account):
        return jsonify('')
    res={'account':account,'page':page,'id':id}
    sql='select blogs.id,blogs.title,blogs.brief from blogs join collect on blogs.id=collect.blog_id where collect.folder_id=:id limit :page,10'
    qy = get_sion(sql, 'find',res)
    if qy[0]['code'] == 0:
        ls = [qy[0], {'msg': []}]
        for i in qy[1]:
            ls[1]['msg'].append({'id': i[0], 'title': i[1], 'brief': i[2]})
        return jsonify(ls)
    elif qy[0]['code'] == 1:
        return jsonify(qy)
    else:
        return jsonify(qy)
# 删除文章
@cm.route('/del/my_blog',methods=['post'])
def umb():
    res=request.json
    id=res['id']
    account=res['account']
    token=res['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')
    res={'id':id,'account':account}
    sql='delete from blogs where id=:id and account=:account'
    qy=get_sion(sql,'up',res)
    if qy[0]['code'] == 0:
        sql=['insert into del_blog (blog) values(:id)', 'delete from blog_data where blog_id=:id']
        qy=get_sion(sql,'up',[res,res])
        if qy[0]['code']==0:
                return jsonify(qy)
        else:
            return jsonify(qy)
    else:
        return jsonify(qy)
# 编辑文章
# @cm.route('/editor_bolg',methods=['post'])
# def eb():
#     res=request.json
#     id=res['id']
#     sql='select text from blogs where id={0}'.format(id)
#     qy=get_sion(sql,'find')
#     if qy[0]['code']==0:
#         ls=[qy[0], {'msg': []}]
#         with open(file_path+qy[1],'rb') as f:
#             ls[1]['msg'].append(str(f.read(),'utf-8'))
#         return jsonify(ls)
#     else:
#         return jsonify(qy)

# 收藏夹重命名
@cm.route('/ed_folder',methods=['post'])
def ef():
    res=request.json
    account=res['account']
    name=res['name']
    old=res['old_name']
    token=res['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')
    res={'account':account,'name':name,'old':old}
    sql="update collect_folder set folder=:name where account=:account and folder=:old ".format(name,account,old)
    qy=get_sion(sql,'up',res)
    if qy[0]['code']==0:
        return jsonify(qy)
    else:
        return jsonify(qy)

# 添加收藏
@cm.route('/ad_collect',methods=['post'])
def acc():
    res=request.json
    account=res['account']
    folder=res['folder_id']
    blog=res['blog_id']
    token=res['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')
    res={'account':account,'folder':folder,'blog':blog,'time':date()}
    sql='select id from collect join collect_folder on collect.folder_id=collect_folder.id  where blog_id=:blog and folder_id=:folder and account=:account'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        return jsonify([{'code':26}])
    elif qy[0]['code']==1:
        sql="insert into collect(blog_id,folder_id,time) values(:blog,:folder,:time)"
        qy=get_sion(sql,'up',res)
        if qy[0]['code'] == 0:
            return jsonify(qy)
        else:
            return jsonify(qy)
    else:
        return jsonify(qy)
# 删除收藏
@cm.route('/del/my_collect',methods=['post'])
def umc():
    res=request.json
    account=res['account']
    id=res['id']
    # 验证token
    # 查询用户收藏夹id
    # 判断收藏夹是否有该收藏
    token=res['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')
    res={'account':account,'id':id}
    sql='select collect.id from collect join collect_folder on collect.folder_id=collect_folder.id  where account=:account and blog_id=:id'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        return jsonify([{'code':26}])
    elif qy[0]['code'] == 1:
        sql='delete from collect where blog_id=:id'
        qy=get_sion(sql,'up',res)
        return jsonify(qy)
    else:
        return jsonify(qy)
    return jsonify(qy)


# 删除收藏夹
@cm.route('/del/my_folder',methods=['post'])
def umf():
    res=request.json
    id=res['id']
    account=res['account']
    token=res['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')
    res={'id':id,'account':account}
    sql='select id from collect_folder where account=:account'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:

        sql='delete from collect_folder where  id=:id '
        sql2='delete from collect where folder_id=:id'
        qy=get_sion([sql,sql2],'up',[res,res])
        return jsonify([qy[0]])
    else:
        return jsonify(qy)

# 添加收藏夹
@cm.route('/add/folder',methods=['post'])
def af():
    res=request.json
    name=res['name']
    account=res['account']
    token=res['token']
    if check_token(str(account)+'token',token):
        return  jsonify([{'code':24}])
    if ex_data.account(account):
        return jsonify('')
    res={'name':name,'account':account,'time':date()}
    sql='select count(*) from collect_folder where account=:account'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        if qy[1][0][0]>5:
            return jsonify([{'code':32}])
        else:
            sql="select id from collect_folder where folder=:name and account=:account"
            qy=get_sion(sql,'find',res)
            if qy[0]['code']==0:
                return jsonify([{'code':26}])
            elif qy[0]['code']==1:
                sql="insert into collect_folder (folder,account,time ) values(:name,:account,:time)"
                qy=get_sion(sql,'up',res)
                if qy[0]['code']==0:
                    sql="select id from collect_folder where folder=:name and account=:account"
                    qy=get_sion(sql,'find',res)
                    if qy[0]['code']==0:
                        ls=[{'code':0},{'id':qy[1][0][0]}]
                        return jsonify(ls)
                else:
                    return jsonify(qy)
            else:
                return jsonify(qy)
    else:
        return jsonify([qy[0]])
# 查看收藏夹
@cm.route('/find_folder',methods=['post'])
def ff():
    res=request.json
    account=res['account']
    token = res['token']
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    if ex_data.account(account):
        return jsonify('')
    res={'account':account}
    sql='select id,folder from collect_folder where account=:account'
    qy=get_sion(sql,'find',res)
    if qy[0]['code'] == 0:
        ls=[qy[0],{'msg':[]}]
        for i in qy[1]:
            ls[1]['msg'].append({'id':i[0],'folder':i[1]})
        return jsonify(ls)
    else:
        return jsonify(qy)