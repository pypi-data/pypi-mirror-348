"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest
from kytest import WebConfig


if __name__ == '__main__':
    WebConfig.host = 'https://www-test.qizhidao.com/'
    WebConfig.browser = 'firefox'

    kytest.main(path="tests/test_web.py")


