"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest
from kytest import AppConfig


if __name__ == '__main__':
    AppConfig.did = ['00008110-0018386236A2801E', '00008110-00126192228A801E']
    AppConfig.pkg = 'com.tencent.QQMusic'
    AppConfig.wda_project_path = '/Users/UI/Downloads/WebDriverAgent-master/WebDriverAgent.xcodeproj'
    AppConfig.run_mode = 'full'

    kytest.main(path="tests/test_ios.py")



