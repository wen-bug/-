from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
# from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,UniqueConstraint,Index
from sqlalchemy.orm import scoped_session,sessionmaker
base=declarative_base()
import redis
# pool = redis.ConnectionPool( decode_responses=True)
redis_pool = redis.ConnectionPool(host='localhost', port=6379,max_connections=5, decode_responses=True,password='mypassword')
redisP=redis.Redis(connection_pool=redis_pool)
def eng():
    host = "127.0.0.1"
    user = 'root'
    pwd = '123456'
    db = 'lty'
    engine = create_engine("mysql+pymysql://{0}:{1}@{2}:3306/{3}?charset=utf8mb4".format(user, pwd, host, db),
                           max_overflow=0,
                           pool_size=5,
                           pool_timeout=30,
                           pool_recycle=-1,
                           )
    return engine
session=sessionmaker(eng())
sion=scoped_session(session)
# 用户表
# class User(base):
#     __tablename__='user'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     userName = Column(String(255))
#     Email = Column(String(255))
#     loginDate=(DateTime)
#     headP=(String(255))
#     pwad=(String(255))
def create():
    base.metadata.create_all(eng())

def dele():
    base.metadata.drop_all(eng())

