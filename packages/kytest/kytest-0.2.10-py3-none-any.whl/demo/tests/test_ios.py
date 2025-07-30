"""
@Author: kang.yang
@Date: 2025/4/11 16:16
"""
import kytest
from kytest.core.ios import IosTC
from page.ios_page import IosPage


class TestIosDemo(IosTC):

    def start(self):
        self.start_app()
        self.sleep(5)
        self.ip = IosPage(self.dr)

    def end(self):
        self.stop_app()

    def test_switch_to_lg(self):
        self.ip.music_tab.click()
        self.sleep(5)

    def test_switch_to_jb(self):
        self.ip.gold_tab.click()
        self.sleep(5)
