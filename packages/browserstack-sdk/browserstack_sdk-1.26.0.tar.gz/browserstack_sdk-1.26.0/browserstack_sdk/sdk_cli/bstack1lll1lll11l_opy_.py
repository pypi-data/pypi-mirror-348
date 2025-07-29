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
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lllllll11l_opy_,
    bstack1llllll1ll1_opy_,
    bstack11111lll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_, bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lllll_opy_ import bstack1ll11l11l1l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1ll1ll1l1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll11lll1_opy_(bstack1ll11l11l1l_opy_):
    bstack1l1l1ll1l11_opy_ = bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡳ࡫ࡹࡩࡷࡹࠢ጗")
    bstack1ll111111ll_opy_ = bstack11ll111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣጘ")
    bstack1l1l1l1l1l1_opy_ = bstack11ll111_opy_ (u"ࠥࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጙ")
    bstack1l1l1l1l11l_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡶࠦጚ")
    bstack1l1l1l1l1ll_opy_ = bstack11ll111_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡷ࡫ࡦࡴࠤጛ")
    bstack1ll111l1l1l_opy_ = bstack11ll111_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡨࡸࡥࡢࡶࡨࡨࠧጜ")
    bstack1l1l1l111ll_opy_ = bstack11ll111_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥጝ")
    bstack1l1l1l1llll_opy_ = bstack11ll111_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࠨጞ")
    def __init__(self):
        super().__init__(bstack1ll111llll1_opy_=self.bstack1l1l1ll1l11_opy_, frameworks=[bstack1llll1llll1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.BEFORE_EACH, bstack1ll1lll1ll1_opy_.POST), self.bstack1l1l1111l1l_opy_)
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.POST), self.bstack1ll1l111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1lll1ll11_opy_ = self.bstack1l11lllllll_opy_(instance.context)
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጟ") + str(bstack11111ll1l1_opy_) + bstack11ll111_opy_ (u"ࠥࠦጠ"))
        f.bstack111111ll11_opy_(instance, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, bstack1l1lll1ll11_opy_)
        bstack1l11llllll1_opy_ = self.bstack1l11lllllll_opy_(instance.context, bstack1l1l1111l11_opy_=False)
        f.bstack111111ll11_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l1l1l1_opy_, bstack1l11llllll1_opy_)
    def bstack1ll1l111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l1l_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        if not f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l111ll_opy_, False):
            self.__1l1l1111111_opy_(f,instance,bstack11111ll1l1_opy_)
    def bstack1ll1l111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l1l_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        if not f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l111ll_opy_, False):
            self.__1l1l1111111_opy_(f, instance, bstack11111ll1l1_opy_)
        if not f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l1llll_opy_, False):
            self.__1l1l11111ll_opy_(f, instance, bstack11111ll1l1_opy_)
    def bstack1l11lllll11_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll11llllll_opy_(instance):
            return
        if f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l1llll_opy_, False):
            return
        driver.execute_script(
            bstack11ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጡ").format(
                json.dumps(
                    {
                        bstack11ll111_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጢ"): bstack11ll111_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤጣ"),
                        bstack11ll111_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥጤ"): {bstack11ll111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣጥ"): result},
                    }
                )
            )
        )
        f.bstack111111ll11_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l1llll_opy_, True)
    def bstack1l11lllllll_opy_(self, context: bstack11111lll1l_opy_, bstack1l1l1111l11_opy_= True):
        if bstack1l1l1111l11_opy_:
            bstack1l1lll1ll11_opy_ = self.bstack1ll111ll1ll_opy_(context, reverse=True)
        else:
            bstack1l1lll1ll11_opy_ = self.bstack1ll111ll11l_opy_(context, reverse=True)
        return [f for f in bstack1l1lll1ll11_opy_ if f[1].state != bstack11111l1l1l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l1l1lll1l_opy_, stage=STAGE.bstack111lllll_opy_)
    def __1l1l11111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢጦ")).get(bstack11ll111_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢጧ")):
            bstack1l1lll1ll11_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, [])
            if not bstack1l1lll1ll11_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጨ") + str(bstack11111ll1l1_opy_) + bstack11ll111_opy_ (u"ࠧࠨጩ"))
                return
            driver = bstack1l1lll1ll11_opy_[0][0]()
            status = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_, None)
            if not status:
                self.logger.debug(bstack11ll111_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࠣጪ") + str(bstack11111ll1l1_opy_) + bstack11ll111_opy_ (u"ࠢࠣጫ"))
                return
            bstack1l1l1l1ll1l_opy_ = {bstack11ll111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣጬ"): status.lower()}
            bstack1l1l1ll11ll_opy_ = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1l1ll11l1_opy_, None)
            if status.lower() == bstack11ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩጭ") and bstack1l1l1ll11ll_opy_ is not None:
                bstack1l1l1l1ll1l_opy_[bstack11ll111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪጮ")] = bstack1l1l1ll11ll_opy_[0][bstack11ll111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧጯ")][0] if isinstance(bstack1l1l1ll11ll_opy_, list) else str(bstack1l1l1ll11ll_opy_)
            driver.execute_script(
                bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥጰ").format(
                    json.dumps(
                        {
                            bstack11ll111_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጱ"): bstack11ll111_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥጲ"),
                            bstack11ll111_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጳ"): bstack1l1l1l1ll1l_opy_,
                        }
                    )
                )
            )
            f.bstack111111ll11_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l1llll_opy_, True)
    @measure(event_name=EVENTS.bstack1l111ll11l_opy_, stage=STAGE.bstack111lllll_opy_)
    def __1l1l1111111_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠢጴ")).get(bstack11ll111_opy_ (u"ࠥࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧጵ")):
            test_name = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1l1111ll1_opy_, None)
            if not test_name:
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥጶ"))
                return
            bstack1l1lll1ll11_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, [])
            if not bstack1l1lll1ll11_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጷ") + str(bstack11111ll1l1_opy_) + bstack11ll111_opy_ (u"ࠨࠢጸ"))
                return
            for bstack1l1ll11l111_opy_, bstack1l1l111111l_opy_ in bstack1l1lll1ll11_opy_:
                if not bstack1llll1llll1_opy_.bstack1ll11llllll_opy_(bstack1l1l111111l_opy_):
                    continue
                driver = bstack1l1ll11l111_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧጹ").format(
                        json.dumps(
                            {
                                bstack11ll111_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣጺ"): bstack11ll111_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥጻ"),
                                bstack11ll111_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨጼ"): {bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤጽ"): test_name},
                            }
                        )
                    )
                )
            f.bstack111111ll11_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l111ll_opy_, True)
    def bstack1ll111ll111_opy_(
        self,
        instance: bstack1llll1lllll_opy_,
        f: TestFramework,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l1l_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        bstack1l1lll1ll11_opy_ = [d for d, _ in f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, [])]
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧጾ"))
            return
        if not bstack1l1ll1ll1l1_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦጿ"))
            return
        for bstack1l1l11111l1_opy_ in bstack1l1lll1ll11_opy_:
            driver = bstack1l1l11111l1_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11ll111_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧፀ") + str(timestamp)
            driver.execute_script(
                bstack11ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨፁ").format(
                    json.dumps(
                        {
                            bstack11ll111_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤፂ"): bstack11ll111_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧፃ"),
                            bstack11ll111_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢፄ"): {
                                bstack11ll111_opy_ (u"ࠧࡺࡹࡱࡧࠥፅ"): bstack11ll111_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥፆ"),
                                bstack11ll111_opy_ (u"ࠢࡥࡣࡷࡥࠧፇ"): data,
                                bstack11ll111_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢፈ"): bstack11ll111_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣፉ")
                            }
                        }
                    )
                )
            )
    def bstack1ll11111111_opy_(
        self,
        instance: bstack1llll1lllll_opy_,
        f: TestFramework,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l1l_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        bstack1l1lll1ll11_opy_ = [d for _, d in f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, [])] + [d for _, d in f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l1l1l1l1_opy_, [])]
        keys = [
            bstack1llll11lll1_opy_.bstack1ll111111ll_opy_,
            bstack1llll11lll1_opy_.bstack1l1l1l1l1l1_opy_,
        ]
        bstack1l1lll1ll11_opy_ = [
            d for key in keys for _, d in f.bstack1llllll1lll_opy_(instance, key, [])
        ]
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧ࡮ࡺࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧፊ"))
            return
        if f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1ll111l1l1l_opy_, False):
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡉࡂࡕࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡧࡷ࡫ࡡࡵࡧࡧࠦፋ"))
            return
        self.bstack1ll11ll1ll1_opy_()
        bstack11ll1lll1l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1l1l1l_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1ll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
        req.test_framework_state = bstack11111ll1l1_opy_[0].name
        req.test_hook_state = bstack11111ll1l1_opy_[1].name
        req.test_uuid = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l11l1l1_opy_)
        for driver in bstack1l1lll1ll11_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦፌ")
                if bstack1llll1llll1_opy_.bstack1llllll1lll_opy_(driver, bstack1llll1llll1_opy_.bstack1l11lllll1l_opy_, False)
                else bstack11ll111_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧፍ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1llll1llll1_opy_.bstack1llllll1lll_opy_(driver, bstack1llll1llll1_opy_.bstack1l1l1lll111_opy_, bstack11ll111_opy_ (u"ࠢࠣፎ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1llll1llll1_opy_.bstack1llllll1lll_opy_(driver, bstack1llll1llll1_opy_.bstack1l1l1ll1ll1_opy_, bstack11ll111_opy_ (u"ࠣࠤፏ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll1ll11_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, [])
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፐ") + str(kwargs) + bstack11ll111_opy_ (u"ࠥࠦፑ"))
            return {}
        if len(bstack1l1lll1ll11_opy_) > 1:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፒ") + str(kwargs) + bstack11ll111_opy_ (u"ࠧࠨፓ"))
            return {}
        bstack1l1ll11l111_opy_, bstack1l1ll11lll1_opy_ = bstack1l1lll1ll11_opy_[0]
        driver = bstack1l1ll11l111_opy_()
        if not driver:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፔ") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣፕ"))
            return {}
        capabilities = f.bstack1llllll1lll_opy_(bstack1l1ll11lll1_opy_, bstack1llll1llll1_opy_.bstack1l1ll1111ll_opy_)
        if not capabilities:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፖ") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥፗ"))
            return {}
        return capabilities.get(bstack11ll111_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣፘ"), {})
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lll1ll11_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, [])
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፙ") + str(kwargs) + bstack11ll111_opy_ (u"ࠧࠨፚ"))
            return
        if len(bstack1l1lll1ll11_opy_) > 1:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ፛") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣ፜"))
        bstack1l1ll11l111_opy_, bstack1l1ll11lll1_opy_ = bstack1l1lll1ll11_opy_[0]
        driver = bstack1l1ll11l111_opy_()
        if not driver:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ፝") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥ፞"))
            return
        return driver