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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1llllll1ll1_opy_,
)
from bstack_utils.helper import  bstack1lll1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll1l11l_opy_, bstack1llll1lllll_opy_, bstack1ll1lll1ll1_opy_, bstack1lll1l11111_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1111l11l_opy_ import bstack1l1lll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1llll11lll1_opy_
from bstack_utils.percy import bstack1l11l1llll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll1l11lll_opy_(bstack1lll1l1111l_opy_):
    def __init__(self, bstack1l1ll11ll11_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1ll11ll11_opy_ = bstack1l1ll11ll11_opy_
        self.percy = bstack1l11l1llll_opy_()
        self.bstack11l11llll_opy_ = bstack1l1lll11l1_opy_()
        self.bstack1l1ll11ll1l_opy_()
        bstack1llll1llll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack11111ll1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1ll1l111l_opy_)
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.POST), self.bstack1ll1l111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1111l_opy_(self, instance: bstack1llllll1ll1_opy_, driver: object):
        bstack1l1lll111l1_opy_ = TestFramework.bstack111111111l_opy_(instance.context)
        for t in bstack1l1lll111l1_opy_:
            bstack1l1lll1ll11_opy_ = TestFramework.bstack1llllll1lll_opy_(t, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll1ll11_opy_) or instance == driver:
                return t
    def bstack1l1ll1l111l_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llll1llll1_opy_.bstack1ll1l1lll1l_opy_(method_name):
                return
            platform_index = f.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1ll1l1l1l1l_opy_, 0)
            bstack1l1llll11ll_opy_ = self.bstack1l1lll1111l_opy_(instance, driver)
            bstack1l1ll1l1111_opy_ = TestFramework.bstack1llllll1lll_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1l1ll1l1l11_opy_, None)
            if not bstack1l1ll1l1111_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡷ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡢࡵࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡾ࡫ࡴࠡࡵࡷࡥࡷࡺࡥࡥࠤሸ"))
                return
            driver_command = f.bstack1ll1l1111l1_opy_(*args)
            for command in bstack1lll1ll1_opy_:
                if command == driver_command:
                    self.bstack1ll1ll111_opy_(driver, platform_index)
            bstack1l11ll11_opy_ = self.percy.bstack1llllll1l1_opy_()
            if driver_command in bstack1l11l1ll_opy_[bstack1l11ll11_opy_]:
                self.bstack11l11llll_opy_.bstack1l11l111ll_opy_(bstack1l1ll1l1111_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥ࡫ࡲࡳࡱࡵࠦሹ"), e)
    def bstack1ll1l111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
        bstack1l1lll1ll11_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, [])
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨሺ") + str(kwargs) + bstack11ll111_opy_ (u"ࠧࠨሻ"))
            return
        if len(bstack1l1lll1ll11_opy_) > 1:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣሼ") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣሽ"))
        bstack1l1ll11l111_opy_, bstack1l1ll11lll1_opy_ = bstack1l1lll1ll11_opy_[0]
        driver = bstack1l1ll11l111_opy_()
        if not driver:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤሾ") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥሿ"))
            return
        bstack1l1ll11llll_opy_ = {
            TestFramework.bstack1ll1l1111ll_opy_: bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨቀ"),
            TestFramework.bstack1ll1l11l1l1_opy_: bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢቁ"),
            TestFramework.bstack1l1ll1l1l11_opy_: bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࠣࡶࡪࡸࡵ࡯ࠢࡱࡥࡲ࡫ࠢቂ")
        }
        bstack1l1ll11l1ll_opy_ = { key: f.bstack1llllll1lll_opy_(instance, key) for key in bstack1l1ll11llll_opy_ }
        bstack1l1ll1l11l1_opy_ = [key for key, value in bstack1l1ll11l1ll_opy_.items() if not value]
        if bstack1l1ll1l11l1_opy_:
            for key in bstack1l1ll1l11l1_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠤቃ") + str(key) + bstack11ll111_opy_ (u"ࠢࠣቄ"))
            return
        platform_index = f.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1ll1l1l1l1l_opy_, 0)
        if self.bstack1l1ll11ll11_opy_.percy_capture_mode == bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥቅ"):
            bstack1111l1l1_opy_ = bstack1l1ll11l1ll_opy_.get(TestFramework.bstack1l1ll1l1l11_opy_) + bstack11ll111_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧቆ")
            bstack1ll1l111ll1_opy_ = bstack1llll11l1ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1l1ll11l1l1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1111l1l1_opy_,
                bstack1lllll11l1_opy_=bstack1l1ll11l1ll_opy_[TestFramework.bstack1ll1l1111ll_opy_],
                bstack1l11lll1l1_opy_=bstack1l1ll11l1ll_opy_[TestFramework.bstack1ll1l11l1l1_opy_],
                bstack1l11l11l1_opy_=platform_index
            )
            bstack1llll11l1ll_opy_.end(EVENTS.bstack1l1ll11l1l1_opy_.value, bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥቇ"), bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤቈ"), True, None, None, None, None, test_name=bstack1111l1l1_opy_)
    def bstack1ll1ll111_opy_(self, driver, platform_index):
        if self.bstack11l11llll_opy_.bstack1ll1l11l1_opy_() is True or self.bstack11l11llll_opy_.capturing() is True:
            return
        self.bstack11l11llll_opy_.bstack11llll11_opy_()
        while not self.bstack11l11llll_opy_.bstack1ll1l11l1_opy_():
            bstack1l1ll1l1111_opy_ = self.bstack11l11llll_opy_.bstack1l11ll1lll_opy_()
            self.bstack1llll11ll1_opy_(driver, bstack1l1ll1l1111_opy_, platform_index)
        self.bstack11l11llll_opy_.bstack1lll1l1ll1_opy_()
    def bstack1llll11ll1_opy_(self, driver, bstack1l11l11l11_opy_, platform_index, test=None):
        from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
        bstack1ll1l111ll1_opy_ = bstack1llll11l1ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack11l1ll11ll_opy_.value)
        if test != None:
            bstack1lllll11l1_opy_ = getattr(test, bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ቉"), None)
            bstack1l11lll1l1_opy_ = getattr(test, bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫቊ"), None)
            PercySDK.screenshot(driver, bstack1l11l11l11_opy_, bstack1lllll11l1_opy_=bstack1lllll11l1_opy_, bstack1l11lll1l1_opy_=bstack1l11lll1l1_opy_, bstack1l11l11l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l11l11l11_opy_)
        bstack1llll11l1ll_opy_.end(EVENTS.bstack11l1ll11ll_opy_.value, bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢቋ"), bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨቌ"), True, None, None, None, None, test_name=bstack1l11l11l11_opy_)
    def bstack1l1ll11ll1l_opy_(self):
        os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧቍ")] = str(self.bstack1l1ll11ll11_opy_.success)
        os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧ቎")] = str(self.bstack1l1ll11ll11_opy_.percy_capture_mode)
        self.percy.bstack1l1ll1l11ll_opy_(self.bstack1l1ll11ll11_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll11l11l_opy_(self.bstack1l1ll11ll11_opy_.percy_build_id)