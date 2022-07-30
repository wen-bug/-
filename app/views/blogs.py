
from flask import Blueprint,jsonify,request
from app.views.tools import get_sion,date,file_path,ex_data,check_token
from app.models import redisP
us=Blueprint('blogUp',__name__)

#文章流量
@us.route('/blog_views',methods=['post'])
def bv():
    res=request.json
    id=res['id']
    title=res['title']
    # lua脚本
    d = date().split(' ')[0]
    sc="""
    local key=KEYS[1]
    local key2=KEYS[2]
    local value=ARGV[1]
    local value2=ARGV[2]
    if redis.call("exists",key)==0
    then
        redis.call("zadd",key,value,key2)
        redis.call("expire",key,86400000)
    end
    local r=redis.call("zincrby",key,value2,key2)
    return r
    """
    # if redisP.exists('hot' + d) == 0:
    #     redisP.zadd('hot' + d, {'b': 0})
    # redisP.zincrby('hot'+d,1,'www')
    cmd=redisP.register_script(sc)
    qy=cmd(keys=['hot'+d,title],args=[0,1])
    print(qy)
    res = {'id': id,}
    sql='select id from blog_data where blog_id=:id'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        sql='update blog_data set page_view=page_view+1 where blog_id=:id'
        qy=get_sion(sql,'up',res)
        if qy[0]['code']==0:
            return jsonify(qy)
        else:
            return jsonify(qy)
    elif qy[0]['code']==1:
        sql='insert into blog_data (blog_id,page_view) values(:id,1)'
        qy=get_sion(sql,'up',res)
        if qy[0]['code']==0:
            return jsonify(qy)
        else:
            return  jsonify(qy)
    else:
        return jsonify(qy)

# 文章信息
@us.route('/article_details',methods=['post'])
def ad():
    res=request.json
    id=res['id']
    account=res['account']
    res={'id':id,'account':account,'time':date()}


    sql="select blogs.id,blogs.account,blogs.title,cast(blogs.time as char) as time,blogs.text,user.userName,user.headP " \
        "from blogs join user on blogs.account=user.Account" \
        " where blogs.id=:id"
    qy=get_sion(sql,'find',res)
    path=qy[1][0][4]
    if qy[0]['code']==0:
        ls=[qy[0],{'msg':[]},{'text':''}]
        ls[1]['msg'].append({'id':qy[1][0][0],'account':qy[1][0][1],'title':qy[1][0][2],'time':qy[1][0][3],'userName':qy[1][0][5],'headP':qy[1][0][6],'view':0,'collect':0,'watch':''})
        if account==0:
            ls[1]['msg'][0]['watch']='no'
        elif account != ls[1]['msg'][0]['account']:
            res['naccount']=ls[1]['msg'][0]['account']
            sql='select id from fans where fan=:account and star=:naccount'
            qy=get_sion(sql,'find',res)
            if qy[0]['code']==0:
                ls[1]['msg'][0]['watch'] = 'true'
            elif qy[0]['code']==1 and account!=int(ls[1]['msg'][0]['account']):
                ls[1]['msg'][0]['watch'] = 'false'
        sql='select a.view,b.collect from ' \
            '(select page_view as view from blog_data where blog_data.blog_id=:id)as a join (select count(*)as collect from collect where collect.blog_id=:id) as b'
        qy=get_sion(sql,'find',res)
        if qy[0]['code'] == 0:
            ls[1]['msg'][0]['view']=qy[1][0][0]
            ls[1]['msg'][0]['collect'] = qy[1][0][1]
        path=file_path+path
        with open(path, 'rb') as f:
            w = f.read()
            ls[2]['text']=str(w, 'utf-8')
        return jsonify(ls)
    elif qy[0]['code']==1:
        return jsonify(qy)
    else:
        return jsonify(qy)

# 查询一级回复
@us.route('/find_comments',methods=['post'])
def fc():
    res=request.json
    id=res['id']
    page=res['page']
    res={'id':id,'page':page}
    sql='select reply.id,reply.account,reply.text,reply.blog_id,cast(reply.time as char) as time,user.userName,user.headP ' \
        'from reply join user on reply.account=user.Account  ' \
        'where reply.blog_id=:id order by reply.time desc limit :page,10 '
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        ls=[qy[0],{'msg':[]}]
        id=[]
        for i in qy[1]:
            ls[1]['msg'].append({'id':i[0],'account':i[1],'text':i[2],'blog_id':i[3],'time':i[4],'name':i[5],'headP':i[6],'like':0,'reply':0})
            id.append(str(i[0]))
        res['kk']=','.join(id)
        sql="select reply_id, count(reply_id)as reply " \
            "from reply_z where reply_id in(:kk) order by time desc "
        qy=get_sion(sql,'find',res)
        if qy[0]['code']==0:
            for i in range(len(ls[1]['msg'])):
                for i in range(len(qy[1])):
                    if ls[1]['msg'][i]['id']==qy[1][i][0]:
                        ls[1]['msg'][i]['reply']=qy[1][i][1]
        elif qy[0]['code']!=1:
            return jsonify([qy[0]])
        res['like']=','.join(id)
        sql='select reply_id, count(reply_id)as likes ' \
            'from likes where reply_id in(:like) GROUP BY reply_id '
        qy=get_sion(sql,'find',res)
        if qy[0]['code'] == 0:
            for i in range(len(ls[1]['msg'])):
                for i in range(len(qy[1])):
                    if ls[1]['msg'][i]['id']==qy[1][i][0]:
                        ls[1]['msg'][i]['like']=qy[1][i][1]
        elif qy[0]['code'] != 1:
            return jsonify([qy[0]])
        return jsonify(ls)
    else:
        return jsonify(qy)
# 回复
@us.route('/to_reply',methods=['post'])
def tr():
    res=request.json
    account=res['account']
    id=res['id']
    txt=res['txt']
    token = res['token']
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    if ex_data.account(account):
        return jsonify('')

    res={'account':account,'id':id,'text':txt,'time':date()}
    sql="insert into reply (blog_id,text,account,time) values(:id,:text,:account,:time)"
    qy=get_sion(sql,'up',res)
    if qy[0]['code']==0:
        return jsonify(qy)
    else:
        return jsonify(qy)
#点赞
@us.route('/i_like',methods=['post'])
def il():
    res=request.json
    id=res['id']
    account=res['account']
    token = res['token']
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    if ex_data.account(account):
        return jsonify('')
    res={'id':id,'account':account}
    sql='select id from likes where reply_id=:id and account=:account'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        return jsonify([{'code':26}])
    elif qy[0]['code']==1:
        sql = 'insert into likes (reply_id,account) values(:id,:account)'
        qy=get_sion(sql,'up',res)
        if qy[0]['code']==0:
            return jsonify(qy)
        else:
            return jsonify(qy)
    else:
        return jsonify(qy)




# 查询二级回复
@us.route('/find_comments2',methods=['post'])
def fc2():
    res=request.json
    id=res['id']
    page=res['page']
    res={'id':id,'page':page}
    sql='select reply_z.id,reply_z.account,reply_z.text,cast(reply_z.time as char) as time,user.userName,user.headP,ton ' \
        'from reply_z join user on user.Account=reply_z.account ' \
        'where reply_z.reply_id=:id order by reply_z.time desc limit :page,10 '
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        ls=[qy[0],{'msg':[]}]
        id=[]
        for i in qy[1]:
            ls[1]['msg'].append({'id':i[0],'account':i[1],'text':i[2],'time':i[3],'name':i[4],'headP':i[5],'to':i[6],'like':0})
            id.append(str(i[0]))
        res['in']=','.join(id)
        sql = 'select reply_id, count(reply_id)as likes ' \
              'from likes_z where reply_id in(:in) GROUP BY reply_id '
        qy = get_sion(sql, 'find',res)
        if qy[0]['code'] == 0:
            for i in range(len(ls[1]['msg'])):
                for j in range(len(qy[1])):
                    if ls[1]['msg'][i]['id'] == qy[1][j][0]:
                        ls[1]['msg'][i]['like'] = qy[1][j][1]
            return jsonify(ls)
        elif qy[0]['code'] == 1:
            return jsonify(ls)
        else:
            return jsonify([qy[0]])
    else:
        return jsonify(qy)
# 二级回复
@us.route('/to_reply2',methods=['post'])
def tr2():
    res=request.json
    id=res['id']
    txt=res['txt']
    ton=res['ton']
    token = res['token']
    account=res['account']
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    if ex_data.account(account):
        return jsonify('')
    account=res['account']
    res={"account":account,'id':id,'text':txt,'ton':ton,'time':date()}
    sql = "insert into reply_z (reply_id,account,text,time,ton) values(:id,:account,:text,:time,:ton)"
    if ton==0:
        sql = "insert into reply_z (reply_id,account,text,time) values(:id,:account,:text,:time)"

    qy=get_sion(sql,'up',res)
    if qy[0]['code']==0:
        return jsonify(qy)
    else:
        return jsonify(qy)
# 二级点赞
@us.route('/i_like2',methods=['post'])
def il2():
    res=request.json
    id=res['id']
    account=res['account']
    token=res['token']
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    if ex_data.account(account):
        return jsonify('')
    res={'id':id,'account':account}
    sql='select id from likes_z where reply_id=:id and account=:account'
    qy=get_sion(sql,'find',res)
    if qy[0]['code']==0:
        return jsonify([{'code':26}])
    elif qy[0]['code']==1:
        sql = 'insert into likes_z (reply_id,account) values(:id,:account)'
        qy=get_sion(sql,'up',res)
        if qy[0]['code']==0:
            return jsonify(qy)
        else:
            return jsonify(qy)
    else:
        return jsonify(qy)

