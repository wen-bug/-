from flask import jsonify, Blueprint, request
from app.views.tools import get_sion,hash_name,user_count
from loguru import logger
from app.models import sion
from app.views.tools import getToken
er = Blueprint('err', __name__)


# @er.app_errorhandler(Exception)
# def e400(e):
#     print(e)
#     logger.warning('[view]'+str(e))
#     return jsonify([{'code': 110}])

#
# @er.app_errorhandler(500)
# def e400(e):
#     logger.warning('[view]'+e)
#     return jsonify([{'code': 111}])


@er.before_app_request
def before():
    res=request.json
    if res:
        if 'token' in res:
            if user_count(str(res['account'])):
                logger.warning('[dos]'+str(res['account']))
                return jsonify(0)

