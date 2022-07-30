from app.models import sion,redisP
from app.myEm import salt,sendH
import random,time,hashlib
import  re
from loguru import logger
file_path= 'D:/myflask/mydata/'
salt='ppttx1'
token_salt='asdfk'
img_salt='wer'
ALLOWED_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "webp"
}


def get_sion(sq,ty,arg):
    sql=sq
    try:
        s=sion()
        if ty=='up':
            if type(sql)==list:
                for i in range(len(sql)):
                    s.execute(sql[i],arg[i]).rowcount
                    # if qy<=0:
                    #     s.rollback()
                    #     return [{'code': 1}]
                s.commit()
                s.close()
                return [{'code': 0}]

            else:
                qy=s.execute(sql,arg).rowcount
                s.commit()
                s.close()
                if qy>0:
                    return [{'code':0}]
                else:
                    return [{'code':1}]
        elif ty=='find':
            qy=s.execute(sql,arg).fetchall()
            s.commit()
            s.close()
            if len(qy)>0:
                return [{'code':0},qy]
            else:
                return [{'code':1},qy]
    except Exception as e:
        # print(e)
        logger.error('[base]'+str(e))
        s.rollback()
        return [{'code':-1}]

def user_count(name):

    sc="""
    local key=KEYS[1]
    if redis.call("exists",key)==0
    then
        redis.call("set",key,1)
        redis.call("expire",key,1000)
        return 0
    else
        local v=redis.call("get",key)
        if tonumber(v)>10
        then
            redis.call("expire",key,1000*v)
            return 34
        else
            redis.call("set",key,1+v)
            return 0
        end
    end
    """
    cmd=redisP.register_script(sc)
    print(name+'count')
    qy=cmd(keys=[name+'count'])
    if qy==34:
        return True
    if qy==0:
       return False

def hash_img(name):
    loginDate = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + img_salt+name
    return hashlib.md5(loginDate.encode('utf8')).hexdigest()
def hash_name(name):
    loginDate = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + salt+name
    return hashlib.md5(loginDate.encode('utf8')).hexdigest()

def hash_token(name):
    loginDate = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + token_salt + name
    return hashlib.md5(loginDate.encode('utf8')).hexdigest()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sendCode(to):
    print('发送')
    ccode=random.randint(100,10000)
    redisP.set(to,ccode,ex=60)
    res=sendH(to, ccode)
    return 200


def setToken(user,val):
    try:
        redisP.set(user,val,ex=86164)
        return True
    except Exception as e:
        print(e)
        return False


def getToken(user):
    try:
        v=redisP.get(user)
        return v
    except Exception as e:
        print(e)
        return False
def check_token(val,token):
    v=getToken(val)
    if getToken(val):
        if v!=token:
            return True
    else:
        return True
# 获取时间
def date():
    return  str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# xss
def xss(val):
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    re_event = re.compile('on[\s\S]*=[\'\"][\s\S]*[\'\"]', re.I)
    re_java = re.compile('[\s][\S]*=[\'\"]javascript:[\s\S]*[\'\"]', re.I)
    val = re_script.sub('', val)
    val = re_java.sub('', val)
    val= re_event.sub('', val)
    return val

# 数据验证
class exx:
    def pwd(self,v):
        if len(v) < 8:
            return True
        else:
            return  False
    def account(self,v):
        # ex='/^\d+$/'
        if  v=='':
            return True
        else:
            return  False
    def em(self,v):
        r_emali = '^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        if re.match(r_emali, v):
            return False
        else:
            return True
ex_data=exx()