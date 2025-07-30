"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest
from kytest import AppConfig


if __name__ == '__main__':
    AppConfig.did = 'xxx'
    AppConfig.pkg = 'com.qzd.hm'
    AppConfig.ability = 'EntryAbility'

    kytest.main(path="tests/test_hm.py")

