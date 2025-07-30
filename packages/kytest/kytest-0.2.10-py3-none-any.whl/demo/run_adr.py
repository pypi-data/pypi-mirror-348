"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest
from kytest import AppConfig


if __name__ == '__main__':
    AppConfig.did = ['417ff34c', 'UQG5T20414005787']
    AppConfig.pkg = 'com.qizhidao.clientapp'
    AppConfig.run_mode = 'polling'

    kytest.main(path="tests/test_adr.py")



