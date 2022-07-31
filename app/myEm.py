import smtplib
import time
from email.mime.text import  MIMEText

salt='ppttx1'



def sendH(to,code):#html
    mail_host = "smtp.qq.com"
    mail_user = 'xxxx'
    mail_pass = 'xxxx'
    sender = to
    contnent="""
    <h1>{0}</h1>
    """.format(code)
    #邮件格式
    msg=MIMEText(contnent,'html','utf-8')
    msg['From']=mail_user
    msg['To']=sender
    msg['Subject']='free code'#主题
    try:
        server=smtplib.SMTP(mail_host,25)#连接
        server.login(mail_user,mail_pass)#登录
        server.sendmail(mail_user,sender,msg.as_string())#发送
        server.quit()#断开连接
        print('yes')
        return 200
    except Exception as e:
        print(e)
        return 'err'
# sendH('1097641954@qq.com',7755)
