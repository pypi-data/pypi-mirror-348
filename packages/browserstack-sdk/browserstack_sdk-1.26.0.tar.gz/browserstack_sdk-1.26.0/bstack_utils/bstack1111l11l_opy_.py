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
from collections import deque
from bstack_utils.constants import *
class bstack1l1lll11l1_opy_:
    def __init__(self):
        self._111l1llllll_opy_ = deque()
        self._111l1lll1ll_opy_ = {}
        self._111l1ll1ll1_opy_ = False
    def bstack111l1lll111_opy_(self, test_name, bstack111l1ll1lll_opy_):
        bstack111l1llll11_opy_ = self._111l1lll1ll_opy_.get(test_name, {})
        return bstack111l1llll11_opy_.get(bstack111l1ll1lll_opy_, 0)
    def bstack111l1ll1l11_opy_(self, test_name, bstack111l1ll1lll_opy_):
        bstack111l1llll1l_opy_ = self.bstack111l1lll111_opy_(test_name, bstack111l1ll1lll_opy_)
        self.bstack111l1ll1l1l_opy_(test_name, bstack111l1ll1lll_opy_)
        return bstack111l1llll1l_opy_
    def bstack111l1ll1l1l_opy_(self, test_name, bstack111l1ll1lll_opy_):
        if test_name not in self._111l1lll1ll_opy_:
            self._111l1lll1ll_opy_[test_name] = {}
        bstack111l1llll11_opy_ = self._111l1lll1ll_opy_[test_name]
        bstack111l1llll1l_opy_ = bstack111l1llll11_opy_.get(bstack111l1ll1lll_opy_, 0)
        bstack111l1llll11_opy_[bstack111l1ll1lll_opy_] = bstack111l1llll1l_opy_ + 1
    def bstack1l11l111ll_opy_(self, bstack111l1lllll1_opy_, bstack111ll111111_opy_):
        bstack111l1lll11l_opy_ = self.bstack111l1ll1l11_opy_(bstack111l1lllll1_opy_, bstack111ll111111_opy_)
        event_name = bstack11ll1l11l1l_opy_[bstack111ll111111_opy_]
        bstack1l1ll1l1111_opy_ = bstack11ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᴨ").format(bstack111l1lllll1_opy_, event_name, bstack111l1lll11l_opy_)
        self._111l1llllll_opy_.append(bstack1l1ll1l1111_opy_)
    def bstack1ll1l11l1_opy_(self):
        return len(self._111l1llllll_opy_) == 0
    def bstack1l11ll1lll_opy_(self):
        bstack111l1lll1l1_opy_ = self._111l1llllll_opy_.popleft()
        return bstack111l1lll1l1_opy_
    def capturing(self):
        return self._111l1ll1ll1_opy_
    def bstack11llll11_opy_(self):
        self._111l1ll1ll1_opy_ = True
    def bstack1lll1l1ll1_opy_(self):
        self._111l1ll1ll1_opy_ = False