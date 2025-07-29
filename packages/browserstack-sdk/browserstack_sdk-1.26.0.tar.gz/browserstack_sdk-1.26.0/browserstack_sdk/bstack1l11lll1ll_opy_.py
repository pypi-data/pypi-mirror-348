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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from browserstack_sdk.bstack111l1l111_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11lll11l_opy_
from bstack_utils.bstack1l1lll1l1_opy_ import bstack1l111111l_opy_
from bstack_utils.constants import bstack1111llllll_opy_
class bstack1lll1111l_opy_:
    def __init__(self, args, logger, bstack1111lll111_opy_, bstack1111l1ll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111lll111_opy_ = bstack1111lll111_opy_
        self.bstack1111l1ll1l_opy_ = bstack1111l1ll1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l1l1ll_opy_ = []
        self.bstack1111ll1ll1_opy_ = None
        self.bstack11ll1ll11_opy_ = []
        self.bstack1111ll1lll_opy_ = self.bstack11l1l11l11_opy_()
        self.bstack1l11llll11_opy_ = -1
    def bstack1ll11lll1l_opy_(self, bstack1111lll11l_opy_):
        self.parse_args()
        self.bstack1111ll1l1l_opy_()
        self.bstack1111ll1l11_opy_(bstack1111lll11l_opy_)
        self.bstack1111llll11_opy_()
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111ll111l_opy_():
        import importlib
        if getattr(importlib, bstack11ll111_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬ࿱"), False):
            bstack1111l1llll_opy_ = importlib.find_loader(bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ࿲"))
        else:
            bstack1111l1llll_opy_ = importlib.util.find_spec(bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ࿳"))
    def bstack1111lll1l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l11llll11_opy_ = -1
        if self.bstack1111l1ll1l_opy_ and bstack11ll111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ࿴") in self.bstack1111lll111_opy_:
            self.bstack1l11llll11_opy_ = int(self.bstack1111lll111_opy_[bstack11ll111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ࿵")])
        try:
            bstack1111ll11ll_opy_ = [bstack11ll111_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧ࿶"), bstack11ll111_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩ࿷"), bstack11ll111_opy_ (u"ࠧ࠮ࡲࠪ࿸")]
            if self.bstack1l11llll11_opy_ >= 0:
                bstack1111ll11ll_opy_.extend([bstack11ll111_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ࿹"), bstack11ll111_opy_ (u"ࠩ࠰ࡲࠬ࿺")])
            for arg in bstack1111ll11ll_opy_:
                self.bstack1111lll1l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111ll1l1l_opy_(self):
        bstack1111ll1ll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
        return bstack1111ll1ll1_opy_
    def bstack111l11ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111ll111l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l11lll11l_opy_)
    def bstack1111ll1l11_opy_(self, bstack1111lll11l_opy_):
        bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
        if bstack1111lll11l_opy_:
            self.bstack1111ll1ll1_opy_.append(bstack11ll111_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ࿻"))
            self.bstack1111ll1ll1_opy_.append(bstack11ll111_opy_ (u"࡙ࠫࡸࡵࡦࠩ࿼"))
        if bstack11lll1l1l_opy_.bstack1111lll1ll_opy_():
            self.bstack1111ll1ll1_opy_.append(bstack11ll111_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࿽"))
            self.bstack1111ll1ll1_opy_.append(bstack11ll111_opy_ (u"࠭ࡔࡳࡷࡨࠫ࿾"))
        self.bstack1111ll1ll1_opy_.append(bstack11ll111_opy_ (u"ࠧ࠮ࡲࠪ࿿"))
        self.bstack1111ll1ll1_opy_.append(bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭က"))
        self.bstack1111ll1ll1_opy_.append(bstack11ll111_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫခ"))
        self.bstack1111ll1ll1_opy_.append(bstack11ll111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪဂ"))
        if self.bstack1l11llll11_opy_ > 1:
            self.bstack1111ll1ll1_opy_.append(bstack11ll111_opy_ (u"ࠫ࠲ࡴࠧဃ"))
            self.bstack1111ll1ll1_opy_.append(str(self.bstack1l11llll11_opy_))
    def bstack1111llll11_opy_(self):
        if bstack1l111111l_opy_.bstack11ll11l1ll_opy_(self.bstack1111lll111_opy_):
             self.bstack1111ll1ll1_opy_ += [
                bstack1111llllll_opy_.get(bstack11ll111_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫင")), str(bstack1l111111l_opy_.bstack11lll111_opy_(self.bstack1111lll111_opy_)),
                bstack1111llllll_opy_.get(bstack11ll111_opy_ (u"࠭ࡤࡦ࡮ࡤࡽࠬစ")), str(bstack1111llllll_opy_.get(bstack11ll111_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠳ࡤࡦ࡮ࡤࡽࠬဆ")))
            ]
    def bstack1111l1lll1_opy_(self):
        bstack11ll1ll11_opy_ = []
        for spec in self.bstack11l1l1ll_opy_:
            bstack1l111l11ll_opy_ = [spec]
            bstack1l111l11ll_opy_ += self.bstack1111ll1ll1_opy_
            bstack11ll1ll11_opy_.append(bstack1l111l11ll_opy_)
        self.bstack11ll1ll11_opy_ = bstack11ll1ll11_opy_
        return bstack11ll1ll11_opy_
    def bstack11l1l11l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1111ll1lll_opy_ = True
            return True
        except Exception as e:
            self.bstack1111ll1lll_opy_ = False
        return self.bstack1111ll1lll_opy_
    def bstack1llll111ll_opy_(self, bstack1111ll1111_opy_, bstack1ll11lll1l_opy_):
        bstack1ll11lll1l_opy_[bstack11ll111_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨဇ")] = self.bstack1111lll111_opy_
        multiprocessing.set_start_method(bstack11ll111_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨဈ"))
        bstack1l111111ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111lllll1_opy_ = manager.list()
        if bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ဉ") in self.bstack1111lll111_opy_:
            for index, platform in enumerate(self.bstack1111lll111_opy_[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧည")]):
                bstack1l111111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1111ll1111_opy_,
                                                            args=(self.bstack1111ll1ll1_opy_, bstack1ll11lll1l_opy_, bstack1111lllll1_opy_)))
            bstack111l111111_opy_ = len(self.bstack1111lll111_opy_[bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဋ")])
        else:
            bstack1l111111ll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1111ll1111_opy_,
                                                        args=(self.bstack1111ll1ll1_opy_, bstack1ll11lll1l_opy_, bstack1111lllll1_opy_)))
            bstack111l111111_opy_ = 1
        i = 0
        for t in bstack1l111111ll_opy_:
            os.environ[bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ဌ")] = str(i)
            if bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဍ") in self.bstack1111lll111_opy_:
                os.environ[bstack11ll111_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩဎ")] = json.dumps(self.bstack1111lll111_opy_[bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬဏ")][i % bstack111l111111_opy_])
            i += 1
            t.start()
        for t in bstack1l111111ll_opy_:
            t.join()
        return list(bstack1111lllll1_opy_)
    @staticmethod
    def bstack11ll1111l1_opy_(driver, bstack1111ll11l1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧတ"), None)
        if item and getattr(item, bstack11ll111_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭ထ"), None) and not getattr(item, bstack11ll111_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧဒ"), False):
            logger.info(
                bstack11ll111_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧဓ"))
            bstack1111llll1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll11llll1_opy_.bstack1l1l111ll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)