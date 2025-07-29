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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1llllll1ll1_opy_,
    bstack11111lll1l_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1ll1l1_opy_, bstack1ll1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_, bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lllll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lllll_opy_ import bstack1ll11l11l1l_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l11lll1l_opy_ import bstack111l1111_opy_, bstack1l1l1ll1l_opy_, bstack11111ll11_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1llll11111l_opy_(bstack1ll11l11l1l_opy_):
    bstack1l1l1ll1l11_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨቮ")
    bstack1ll111111ll_opy_ = bstack11ll111_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢቯ")
    bstack1l1l1l1l1l1_opy_ = bstack11ll111_opy_ (u"ࠤࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦተ")
    bstack1l1l1l1l11l_opy_ = bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥቱ")
    bstack1l1l1l1l1ll_opy_ = bstack11ll111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡶࡪ࡬ࡳࠣቲ")
    bstack1ll111l1l1l_opy_ = bstack11ll111_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡧࡷ࡫ࡡࡵࡧࡧࠦታ")
    bstack1l1l1l111ll_opy_ = bstack11ll111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤቴ")
    bstack1l1l1l1llll_opy_ = bstack11ll111_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠧት")
    def __init__(self):
        super().__init__(bstack1ll111llll1_opy_=self.bstack1l1l1ll1l11_opy_, frameworks=[bstack1llll1llll1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.BEFORE_EACH, bstack1ll1lll1ll1_opy_.POST), self.bstack1l1l1l1lll1_opy_)
        if bstack1ll1l1lll_opy_():
            TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.POST), self.bstack1ll1l111l1l_opy_)
        else:
            TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.POST), self.bstack1ll1l111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1ll1111_opy_ = self.bstack1l1l1l11ll1_opy_(instance.context)
        if not bstack1l1l1ll1111_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡶࡡࡨࡧ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨቶ") + str(bstack11111ll1l1_opy_) + bstack11ll111_opy_ (u"ࠤࠥቷ"))
            return
        f.bstack111111ll11_opy_(instance, bstack1llll11111l_opy_.bstack1ll111111ll_opy_, bstack1l1l1ll1111_opy_)
    def bstack1l1l1l11ll1_opy_(self, context: bstack11111lll1l_opy_, bstack1l1l1l1ll11_opy_= True):
        if bstack1l1l1l1ll11_opy_:
            bstack1l1l1ll1111_opy_ = self.bstack1ll111ll1ll_opy_(context, reverse=True)
        else:
            bstack1l1l1ll1111_opy_ = self.bstack1ll111ll11l_opy_(context, reverse=True)
        return [f for f in bstack1l1l1ll1111_opy_ if f[1].state != bstack11111l1l1l_opy_.QUIT]
    def bstack1ll1l111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1l1lll1_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        if not bstack1l1ll1ll1l1_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቸ") + str(kwargs) + bstack11ll111_opy_ (u"ࠦࠧቹ"))
            return
        bstack1l1l1ll1111_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1llll11111l_opy_.bstack1ll111111ll_opy_, [])
        if not bstack1l1l1ll1111_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣቺ") + str(kwargs) + bstack11ll111_opy_ (u"ࠨࠢቻ"))
            return
        if len(bstack1l1l1ll1111_opy_) > 1:
            self.logger.debug(
                bstack1ll1llll11l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤቼ"))
        bstack1l1l1l11l1l_opy_, bstack1l1ll11lll1_opy_ = bstack1l1l1ll1111_opy_[0]
        page = bstack1l1l1l11l1l_opy_()
        if not page:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣች") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥቾ"))
            return
        bstack11l1l11ll1_opy_ = getattr(args[0], bstack11ll111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥቿ"), None)
        try:
            page.evaluate(bstack11ll111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧኀ"),
                        bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩኁ") + json.dumps(
                            bstack11l1l11ll1_opy_) + bstack11ll111_opy_ (u"ࠨࡽࡾࠤኂ"))
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧኃ"), e)
    def bstack1ll1l111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1l1lll1_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        if not bstack1l1ll1ll1l1_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦኄ") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥኅ"))
            return
        bstack1l1l1ll1111_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1llll11111l_opy_.bstack1ll111111ll_opy_, [])
        if not bstack1l1l1ll1111_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨኆ") + str(kwargs) + bstack11ll111_opy_ (u"ࠦࠧኇ"))
            return
        if len(bstack1l1l1ll1111_opy_) > 1:
            self.logger.debug(
                bstack1ll1llll11l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡶࡡࡨࡧࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢኈ"))
        bstack1l1l1l11l1l_opy_, bstack1l1ll11lll1_opy_ = bstack1l1l1ll1111_opy_[0]
        page = bstack1l1l1l11l1l_opy_()
        if not page:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ኉") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣኊ"))
            return
        status = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_, None)
        if not status:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦኋ") + str(bstack11111ll1l1_opy_) + bstack11ll111_opy_ (u"ࠤࠥኌ"))
            return
        bstack1l1l1l1ll1l_opy_ = {bstack11ll111_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥኍ"): status.lower()}
        bstack1l1l1ll11ll_opy_ = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1l1ll11l1_opy_, None)
        if status.lower() == bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ኎") and bstack1l1l1ll11ll_opy_ is not None:
            bstack1l1l1l1ll1l_opy_[bstack11ll111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ኏")] = bstack1l1l1ll11ll_opy_[0][bstack11ll111_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩነ")][0] if isinstance(bstack1l1l1ll11ll_opy_, list) else str(bstack1l1l1ll11ll_opy_)
        try:
              page.evaluate(
                    bstack11ll111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣኑ"),
                    bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥ࠭ኒ")
                    + json.dumps(bstack1l1l1l1ll1l_opy_)
                    + bstack11ll111_opy_ (u"ࠤࢀࠦና")
                )
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥኔ"), e)
    def bstack1ll111ll111_opy_(
        self,
        instance: bstack1llll1lllll_opy_,
        f: TestFramework,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1l1lll1_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        if not bstack1l1ll1ll1l1_opy_:
            self.logger.debug(
                bstack1ll1llll11l_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧን"))
            return
        bstack1l1l1ll1111_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1llll11111l_opy_.bstack1ll111111ll_opy_, [])
        if not bstack1l1l1ll1111_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኖ") + str(kwargs) + bstack11ll111_opy_ (u"ࠨࠢኗ"))
            return
        if len(bstack1l1l1ll1111_opy_) > 1:
            self.logger.debug(
                bstack1ll1llll11l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤኘ"))
        bstack1l1l1l11l1l_opy_, bstack1l1ll11lll1_opy_ = bstack1l1l1ll1111_opy_[0]
        page = bstack1l1l1l11l1l_opy_()
        if not page:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣኙ") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥኚ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack11ll111_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣኛ") + str(timestamp)
        try:
            page.evaluate(
                bstack11ll111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧኜ"),
                bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪኝ").format(
                    json.dumps(
                        {
                            bstack11ll111_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨኞ"): bstack11ll111_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤኟ"),
                            bstack11ll111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦአ"): {
                                bstack11ll111_opy_ (u"ࠤࡷࡽࡵ࡫ࠢኡ"): bstack11ll111_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢኢ"),
                                bstack11ll111_opy_ (u"ࠦࡩࡧࡴࡢࠤኣ"): data,
                                bstack11ll111_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦኤ"): bstack11ll111_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧእ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡳ࠶࠷ࡹࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡻࡾࠤኦ"), e)
    def bstack1ll11111111_opy_(
        self,
        instance: bstack1llll1lllll_opy_,
        f: TestFramework,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1l1lll1_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        if f.bstack1llllll1lll_opy_(instance, bstack1llll11111l_opy_.bstack1ll111l1l1l_opy_, False):
            return
        self.bstack1ll11ll1ll1_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1l1l1l_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1ll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
        req.test_framework_state = bstack11111ll1l1_opy_[0].name
        req.test_hook_state = bstack11111ll1l1_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l11l1l1_opy_)
        for bstack1l1l1l11l11_opy_ in bstack1lllll1lll1_opy_.bstack11111111l1_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack11ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢኧ")
                if bstack1l1ll1ll1l1_opy_
                else bstack11ll111_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣከ")
            )
            session.ref = bstack1l1l1l11l11_opy_.ref()
            session.hub_url = bstack1lllll1lll1_opy_.bstack1llllll1lll_opy_(bstack1l1l1l11l11_opy_, bstack1lllll1lll1_opy_.bstack1l1l1lll111_opy_, bstack11ll111_opy_ (u"ࠥࠦኩ"))
            session.framework_name = bstack1l1l1l11l11_opy_.framework_name
            session.framework_version = bstack1l1l1l11l11_opy_.framework_version
            session.framework_session_id = bstack1lllll1lll1_opy_.bstack1llllll1lll_opy_(bstack1l1l1l11l11_opy_, bstack1lllll1lll1_opy_.bstack1l1l1ll1ll1_opy_, bstack11ll111_opy_ (u"ࠦࠧኪ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1ll1111_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1llll11111l_opy_.bstack1ll111111ll_opy_, [])
        if not bstack1l1l1ll1111_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨካ") + str(kwargs) + bstack11ll111_opy_ (u"ࠨࠢኬ"))
            return
        if len(bstack1l1l1ll1111_opy_) > 1:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣክ") + str(kwargs) + bstack11ll111_opy_ (u"ࠣࠤኮ"))
        bstack1l1l1l11l1l_opy_, bstack1l1ll11lll1_opy_ = bstack1l1l1ll1111_opy_[0]
        page = bstack1l1l1l11l1l_opy_()
        if not page:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡱࡣࡪࡩࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኯ") + str(kwargs) + bstack11ll111_opy_ (u"ࠥࠦኰ"))
            return
        return page
    def bstack1ll1l1l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l1l1l111_opy_ = {}
        for bstack1l1l1l11l11_opy_ in bstack1lllll1lll1_opy_.bstack11111111l1_opy_.values():
            caps = bstack1lllll1lll1_opy_.bstack1llllll1lll_opy_(bstack1l1l1l11l11_opy_, bstack1lllll1lll1_opy_.bstack1l1ll1111ll_opy_, bstack11ll111_opy_ (u"ࠦࠧ኱"))
        bstack1l1l1l1l111_opy_[bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥኲ")] = caps.get(bstack11ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢኳ"), bstack11ll111_opy_ (u"ࠢࠣኴ"))
        bstack1l1l1l1l111_opy_[bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢኵ")] = caps.get(bstack11ll111_opy_ (u"ࠤࡲࡷࠧ኶"), bstack11ll111_opy_ (u"ࠥࠦ኷"))
        bstack1l1l1l1l111_opy_[bstack11ll111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨኸ")] = caps.get(bstack11ll111_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤኹ"), bstack11ll111_opy_ (u"ࠨࠢኺ"))
        bstack1l1l1l1l111_opy_[bstack11ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣኻ")] = caps.get(bstack11ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥኼ"), bstack11ll111_opy_ (u"ࠤࠥኽ"))
        return bstack1l1l1l1l111_opy_
    def bstack1ll1l1ll1ll_opy_(self, page: object, bstack1ll1l1l1111_opy_, args={}):
        try:
            bstack1l1l1l11lll_opy_ = bstack11ll111_opy_ (u"ࠥࠦࠧ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪ࠱࠲࠳ࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࠫࡶࡪࡹ࡯࡭ࡸࡨ࠰ࠥࡸࡥ࡫ࡧࡦࡸ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶ࠲ࡵࡻࡳࡩࠪࡵࡩࡸࡵ࡬ࡷࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢀ࡬࡮ࡠࡤࡲࡨࡾࢃࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࢁ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪࠪࡾࡥࡷ࡭࡟࡫ࡵࡲࡲࢂ࠯ࠢࠣࠤኾ")
            bstack1ll1l1l1111_opy_ = bstack1ll1l1l1111_opy_.replace(bstack11ll111_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ኿"), bstack11ll111_opy_ (u"ࠧࡨࡳࡵࡣࡦ࡯ࡘࡪ࡫ࡂࡴࡪࡷࠧዀ"))
            script = bstack1l1l1l11lll_opy_.format(fn_body=bstack1ll1l1l1111_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠨࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡅࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶ࠯ࠤࠧ዁") + str(e) + bstack11ll111_opy_ (u"ࠢࠣዂ"))