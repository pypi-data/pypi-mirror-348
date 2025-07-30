"""
@Author: kang.yang
@Date: 2024/10/8 15:04
"""
import kytest
from kytest.core.hm import HmElem


class HmPage(kytest.Page):
    my_entry = HmElem(text='我的')
    login_entry = HmElem(text='登录/注册')
    pwd_login = HmElem(text='账号登录')
    forget_pwd = HmElem(text='忘记密码')

