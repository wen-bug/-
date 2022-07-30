from flask import Blueprint, jsonify, request
from app.models import redisP
from app.views.tools import get_sion, date, check_token, ex_data

us = Blueprint('home', __name__)


# 推荐
@us.route('/find_suggest', methods=['post'])
def wf():
    res = request.json
    account = res['account']
    page = res['page']
    token = res['token']
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    if ex_data.account(account):
        return jsonify('')
    res = {'account': account, 'page': page, 'ex': ''}
    sql = 'select tag from label where  account=:account'
    qy = get_sion(sql, 'find', res)
    if qy[0]['code'] == 0:
        tl = [i[0] for i in qy[1]]
        condition = '|'.join(tl)
        res['ex'] = condition
        sql1 = "SELECT blogs.id,blogs.title,blogs.brief,blog_data.page_view,blogs.time " \
               "FROM blogs join blog_data on blogs.id=blog_data.blog_id " \
               "where title REGEXP :ex ORDER BY blog_data.page_view asc limit :page,10"
        qy = get_sion(sql1, 'find', res)
        if qy[0]['code'] == 0:
            ls = [{'code': 0}, {'msg': []}]
            for i in qy[1]:
                ls[1]['msg'].append({'id': i[0], 'title': i[1], 'brief': i[2], 'view': i[3], 'time': i[4]})
            return jsonify(ls)
        else:
            return jsonify(qy)
    elif qy[0]['code'] == 1:
        return jsonify([{'code': 28}])
    else:
        return jsonify(qy)


# 关注
@us.route('/find_fans', methods=['post'])
def ff():
    res = request.json
    account = res['account']
    page = res['page']
    token = res['token']
    if check_token(str(account) + 'token', token):
        return jsonify([{'code': 24}])
    if ex_data.account(account):
        return jsonify('')
    res = {'account': account, 'page': page}
    sql = 'select blogs.id,blogs.title,blogs.brief,blog_data.page_view,blogs.time ' \
          ' from (fans join blogs on blogs.account=fans.star) join blog_data on blog_data.blog_id=blogs.id' \
          ' where fans.fan=:account order by time asc limit :page,10'
    qy = get_sion(sql, 'find', res)
    if qy[0]['code'] == 0:
        ls = [qy[0], {'msg': []}]
        for i in qy[1]:
            ls[1]['msg'].append({'id': i[0], 'title': i[1], 'brief': i[2], 'view': i[3], 'time': i[4]})
        return jsonify(ls)
    else:
        return jsonify(qy)


# 热门
@us.route('/find_hot', methods=['post'])
def fh():
    res = request.json
    start = res['page']
    # lua脚本
    res = {'page': start, 'in': ''}
    sc = """
        local key=KEYS[1] 
        local key2=KEYS[2]
        local page=ARGV[1]
        local value=ARGV[2]
        if redis.call("exists",key)==0
        then
        redis.call("zadd",key,value,key2)
        redis.call("expire",key,86400000)
        end
        local li= redis.call("zrevrange",key,page,9)
        return li
       """
    d = date().split(' ')[0]
    cmd = redisP.register_script(sc)
    r_qy = cmd(keys=[str('hot' + d), 'l'], args=[start, 0])
    print(r_qy)
    if len(r_qy) < 10:
        sql = "select blogs.id,blogs.title,blogs.brief,blog_data.page_view,blogs.time " \
              "from blogs left join blog_data on blogs.id=blog_data.blog_id order by blogs.time desc limit :page,10 "
        qy = get_sion(sql, 'find', res)
        if qy[0]['code'] == 0:
            ls = [qy[0], {'msg': []}]
            for i in qy[1]:
                ls[1]['msg'].append({'id': i[0], 'title': i[1], 'brief': i[2], 'view': i[3], 'time': i[4]})
            return jsonify(ls)
        else:
            return jsonify(qy)
    else:
        res['in'] = "','".join(r_qy)
        sql = "select blogs.id,blogs.title,blogs.brief,blog_data.page_view,blogs.time " \
              "from blogs left join blog_data on blogs.id=blog_data.blog_id" \
              " where title in (:in) limit :page,10"
        qy = get_sion(sql, 'find', res)
        if qy[0]['code'] == 0:
            ls = [qy[0], {'msg': []}]
            for i in qy[1]:
                ls[1]['msg'].append({'id': i[0], 'title': i[1], 'brief': i[2], 'view': i[3], 'time': i[4]})
            return jsonify(ls)
        else:
            return jsonify(qy)
