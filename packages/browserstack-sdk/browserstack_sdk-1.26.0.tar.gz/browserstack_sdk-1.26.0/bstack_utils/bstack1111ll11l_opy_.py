# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1ll1lll_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l111_opy_):
    global bstack111_opy_
    bstack1lll1l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstackl_opy_ = bstack1l1l111_opy_ [:-1]
    bstack1l1l11_opy_ = bstack1lll1l_opy_ % len (bstackl_opy_)
    bstack1l1111l_opy_ = bstackl_opy_ [:bstack1l1l11_opy_] + bstackl_opy_ [bstack1l1l11_opy_:]
    if bstack11l11ll_opy_:
        bstack1l111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1lll_opy_ - (bstack1lll111_opy_ + bstack1lll1l_opy_) % bstack1ll11l1_opy_) for bstack1lll111_opy_, char in enumerate (bstack1l1111l_opy_)])
    else:
        bstack1l111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1lll_opy_ - (bstack1lll111_opy_ + bstack1lll1l_opy_) % bstack1ll11l1_opy_) for bstack1lll111_opy_, char in enumerate (bstack1l1111l_opy_)])
    return eval (bstack1l111l_opy_)
class bstack1ll11ll11l_opy_:
    def __init__(self, handler):
        self._111l111111l_opy_ = None
        self.handler = handler
        self._111l1111l11_opy_ = self.bstack111l11111l1_opy_()
        self.patch()
    def patch(self):
        self._111l111111l_opy_ = self._111l1111l11_opy_.execute
        self._111l1111l11_opy_.execute = self.bstack111l11111ll_opy_()
    def bstack111l11111ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11ll111_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨᶱ"), driver_command, None, this, args)
            response = self._111l111111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11ll111_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨᶲ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l1111l11_opy_.execute = self._111l111111l_opy_
    @staticmethod
    def bstack111l11111l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver