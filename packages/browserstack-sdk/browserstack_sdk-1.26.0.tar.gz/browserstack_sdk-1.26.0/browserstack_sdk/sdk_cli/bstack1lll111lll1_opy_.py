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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import (
    bstack1lllllll11l_opy_,
    bstack1llllll1ll1_opy_,
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1lllll1lll1_opy_(bstack1lllllll11l_opy_):
    bstack1l11llll111_opy_ = bstack11ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥ፟")
    bstack1l1l1ll1ll1_opy_ = bstack11ll111_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦ፠")
    bstack1l1l1lll111_opy_ = bstack11ll111_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨ፡")
    bstack1l1ll1111ll_opy_ = bstack11ll111_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ።")
    bstack1l11lll1l1l_opy_ = bstack11ll111_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥ፣")
    bstack1l11llll11l_opy_ = bstack11ll111_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤ፤")
    NAME = bstack11ll111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ፥")
    bstack1l11llll1ll_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1lll111_opy_: Any
    bstack1l11lll1lll_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11ll111_opy_ (u"ࠥࡰࡦࡻ࡮ࡤࡪࠥ፦"), bstack11ll111_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧ፧"), bstack11ll111_opy_ (u"ࠧࡴࡥࡸࡡࡳࡥ࡬࡫ࠢ፨"), bstack11ll111_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࠧ፩"), bstack11ll111_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤ፪")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack11111l1111_opy_(methods)
    def bstack11111l11ll_opy_(self, instance: bstack1llllll1ll1_opy_, method_name: str, bstack1llllll11ll_opy_: timedelta, *args, **kwargs):
        pass
    def bstack11111lllll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllllll111_opy_, bstack1l11lll11ll_opy_ = bstack11111ll1l1_opy_
        bstack1l11lll11l1_opy_ = bstack1lllll1lll1_opy_.bstack1l11llll1l1_opy_(bstack11111ll1l1_opy_)
        if bstack1l11lll11l1_opy_ in bstack1lllll1lll1_opy_.bstack1l11llll1ll_opy_:
            bstack1l11lll1l11_opy_ = None
            for callback in bstack1lllll1lll1_opy_.bstack1l11llll1ll_opy_[bstack1l11lll11l1_opy_]:
                try:
                    bstack1l11lll1ll1_opy_ = callback(self, target, exec, bstack11111ll1l1_opy_, result, *args, **kwargs)
                    if bstack1l11lll1l11_opy_ == None:
                        bstack1l11lll1l11_opy_ = bstack1l11lll1ll1_opy_
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࠨ፫") + str(e) + bstack11ll111_opy_ (u"ࠤࠥ፬"))
                    traceback.print_exc()
            if bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.PRE and callable(bstack1l11lll1l11_opy_):
                return bstack1l11lll1l11_opy_
            elif bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.POST and bstack1l11lll1l11_opy_:
                return bstack1l11lll1l11_opy_
    def bstack11111111ll_opy_(
        self, method_name, previous_state: bstack11111l1l1l_opy_, *args, **kwargs
    ) -> bstack11111l1l1l_opy_:
        if method_name == bstack11ll111_opy_ (u"ࠪࡰࡦࡻ࡮ࡤࡪࠪ፭") or method_name == bstack11ll111_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬ፮") or method_name == bstack11ll111_opy_ (u"ࠬࡴࡥࡸࡡࡳࡥ࡬࡫ࠧ፯"):
            return bstack11111l1l1l_opy_.bstack111111l1ll_opy_
        if method_name == bstack11ll111_opy_ (u"࠭ࡤࡪࡵࡳࡥࡹࡩࡨࠨ፰"):
            return bstack11111l1l1l_opy_.bstack11111ll111_opy_
        if method_name == bstack11ll111_opy_ (u"ࠧࡤ࡮ࡲࡷࡪ࠭፱"):
            return bstack11111l1l1l_opy_.QUIT
        return bstack11111l1l1l_opy_.NONE
    @staticmethod
    def bstack1l11llll1l1_opy_(bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_]):
        return bstack11ll111_opy_ (u"ࠣ࠼ࠥ፲").join((bstack11111l1l1l_opy_(bstack11111ll1l1_opy_[0]).name, bstack1llllll1l1l_opy_(bstack11111ll1l1_opy_[1]).name))
    @staticmethod
    def bstack1ll11llll1l_opy_(bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_], callback: Callable):
        bstack1l11lll11l1_opy_ = bstack1lllll1lll1_opy_.bstack1l11llll1l1_opy_(bstack11111ll1l1_opy_)
        if not bstack1l11lll11l1_opy_ in bstack1lllll1lll1_opy_.bstack1l11llll1ll_opy_:
            bstack1lllll1lll1_opy_.bstack1l11llll1ll_opy_[bstack1l11lll11l1_opy_] = []
        bstack1lllll1lll1_opy_.bstack1l11llll1ll_opy_[bstack1l11lll11l1_opy_].append(callback)
    @staticmethod
    def bstack1ll1l1lll1l_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l1lllll_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l11lll1_opy_(instance: bstack1llllll1ll1_opy_, default_value=None):
        return bstack1lllllll11l_opy_.bstack1llllll1lll_opy_(instance, bstack1lllll1lll1_opy_.bstack1l1ll1111ll_opy_, default_value)
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack1llllll1ll1_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11lll111_opy_(instance: bstack1llllll1ll1_opy_, default_value=None):
        return bstack1lllllll11l_opy_.bstack1llllll1lll_opy_(instance, bstack1lllll1lll1_opy_.bstack1l1l1lll111_opy_, default_value)
    @staticmethod
    def bstack1ll1l1111l1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l1l1l11_opy_(method_name: str, *args):
        if not bstack1lllll1lll1_opy_.bstack1ll1l1lll1l_opy_(method_name):
            return False
        if not bstack1lllll1lll1_opy_.bstack1l11lll1l1l_opy_ in bstack1lllll1lll1_opy_.bstack1l1l11llll1_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1lllll1lll1_opy_.bstack1ll11l1l1l1_opy_(*args)
        return bstack1ll11l11lll_opy_ and bstack11ll111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ፳") in bstack1ll11l11lll_opy_ and bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ፴") in bstack1ll11l11lll_opy_[bstack11ll111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦ፵")]
    @staticmethod
    def bstack1ll1l11111l_opy_(method_name: str, *args):
        if not bstack1lllll1lll1_opy_.bstack1ll1l1lll1l_opy_(method_name):
            return False
        if not bstack1lllll1lll1_opy_.bstack1l11lll1l1l_opy_ in bstack1lllll1lll1_opy_.bstack1l1l11llll1_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1lllll1lll1_opy_.bstack1ll11l1l1l1_opy_(*args)
        return (
            bstack1ll11l11lll_opy_
            and bstack11ll111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ፶") in bstack1ll11l11lll_opy_
            and bstack11ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤ፷") in bstack1ll11l11lll_opy_[bstack11ll111_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ፸")]
        )
    @staticmethod
    def bstack1l1l11llll1_opy_(*args):
        return str(bstack1lllll1lll1_opy_.bstack1ll1l1111l1_opy_(*args)).lower()