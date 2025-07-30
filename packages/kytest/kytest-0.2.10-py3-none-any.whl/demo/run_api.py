"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest
from kytest import ApiConfig
from data.login_data import get_headers


if __name__ == '__main__':
    ApiConfig.host = 'https://app-test.qizhidao.com/'
    ApiConfig.headers = get_headers()

    kytest.main(path="tests/test_api.py")



