#系统
import os
# 三方
from loguru import logger
from flask import  Flask
from flasgger import Swagger
from flask_socketio import SocketIO
from flask_cors import CORS
from  flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
# 自定义
import mySettings
# 系统
# socketio=SocketIO()
# logger.remove(handler_id=None)
logger.add('D:/myflask/log/database/base.log',filter=lambda x: '[base]' in x['message'] ,rotation='500 MB',compression='zip',encoding="utf-8", enqueue=True,retention="1 week",serialize=True)
logger.add('D:/myflask/log/view/view.log',filter=lambda x: '[view]' in x['message'] ,rotation='500 MB',compression='zip',encoding="utf-8", enqueue=True,retention="1 week",serialize=True)
logger.add('D:/myflask/log/dos/dos.log',filter=lambda x: '[dos]' in x['message'] ,rotation='500 MB',compression='zip',encoding="utf-8", enqueue=True,retention="1 week",serialize=True)

# logger.info('This is info information')
def create():
    app=Flask(__name__,static_folder='/myflask/mydata/',static_url_path='/')
    app.config.from_object(mySettings.test)
    # Swagger(app)

    CORS(app)
    # socketio.init_app(app, cors_allowed_origins='*')


    from app.views import user,editor,public,finds,my_home,content_management,personal,home,blogs,to_error
    # 用户
    app.register_blueprint(user.us)
    # 博客编辑
    app.register_blueprint(editor.ed)
    # 验证码
    app.register_blueprint(public.us)
    # 查询
    app.register_blueprint(finds.fd)
    # 个人主页
    app.register_blueprint(my_home.mh)
    # 内容管理
    app.register_blueprint(content_management.cm)
    # 个人资料
    app.register_blueprint(personal.pl)
    # 主页
    app.register_blueprint(home.us)
    # 博客
    app.register_blueprint(blogs.us)
    # 异常
    app.register_blueprint(to_error.er)
    # from app import models
    return  app



