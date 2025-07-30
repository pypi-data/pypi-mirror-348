import kytest
from kytest.core.adr import AdrTC
from page.adr_page import AdrPage


@kytest.story('测试demo')
class TestAdrDemo(AdrTC):
    def start(self):
        self.start_app()
        self.adr = AdrPage(self.dr)

    def end(self):
        self.stop_app()

    @kytest.title('进入我的页')
    def test_switch_to_my(self):
        if self.adr.ad_btn.exists():
            self.adr.ad_btn.click()
        self.adr.my_tab.click()
        self.sleep(5)

    @kytest.title('进入科创空间')
    def test_switch_to_space(self):
        if self.adr.ad_btn.exists():
            self.adr.ad_btn.click()
        self.adr.space_tab.click()
        self.sleep(5)







