import re

from django.contrib.auth.backends import ModelBackend

from apps.users.models import User
def jwt_response_payload_handler(token,user=None,request=None):
    """重写jwt登录视图的构造响应数据函数，多追加id，username"""
    return {
        'token':token,
        'user_id':user.id,
        'username':user.username
    }


def get_user_by_account(account):
    """
    通过传入的账号动态获取user
    :param account:
    :return:
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            user=User.objects.get(mobile=account)
        else:
            user=User.objects.get(username=account)

    except User.DoesNotExist:
        return None
    else:
        return user

class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        #获取user
        user=get_user_by_account(username)
        #判断当前传入的密码是否正确
        if user and user.check_password(password):

            return user