"""
@Author: kang.yang
@Date: 2025/4/11 14:59
"""
import kytest
from kytest.core.ios import IosElem


class IosPage(kytest.Page):
    music_tab = IosElem(label='儿童')
    gold_tab = IosElem(name='金币')
