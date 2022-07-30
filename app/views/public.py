from flask import Blueprint,jsonify,request
from app.views.tools import sendCode
us=Blueprint('public',__name__)

@us.route('/getcode',methods=['post'])
def code():
    res=request.json
    em=res['email']
    states=sendCode(em)
    return jsonify({'states':states})

