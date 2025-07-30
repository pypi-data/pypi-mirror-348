"""
@Author: kang.yang
@Date: 2023/11/16 17:50
"""
import kytest
from kytest.core.web import WebTC
from page.pub_page import PubPage


@kytest.story('登录模块')
class TestWebDemo(WebTC):
    def start(self):
        self.pub = PubPage(self.dr)

    @kytest.title("登录")
    def test_login(self):
        self.pub.login()
        self.sleep(5)




