
from .running.runner import (
    main,
    ApiConfig,
    WebConfig,
    AppConfig,
    SonicConfig,
    OcrConfig
)
from .running.conf import App
from .page import Page
from .utils.config import FileConfig
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger
from .core.api import HttpReq, TC
# from .core.adr import AdrTC, AdrElem
# from .core.ios import IosTC, IosElem
# from .core.web import WebTC, WebElem
# from .core.hm import HmTC, HmElem

__version__ = "0.2.10"
__description__ = "API/安卓/IOS/WEB/鸿蒙Next平台自动化测试框架"
