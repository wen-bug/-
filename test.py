# def tags(tag_name,**args): # 获取为p
#     def tags_decorator(func):# 传入的函数
#         def func_wrapper(name):#传入的值
#             def j():
#                 return name+'j函数'
#             return j  #"<{0}>{1}</{0}>".format(tag_name, func(name))
#         return func_wrapper
#     return tags_decorator
#
# @tags("p")
# def get_text(name):
#     return "Hello "+name
# if __name__ == '__main__':
#     w=get_text('plo')
#     print('最后')
#     print(w())
p=None
with open('D:\myflask\mydata\html\\tt.txt','r',encoding='utf-8') as f:
    p=f.read()
    print(p)