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
from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
from bstack_utils.constants import EVENTS
class bstack1llll1llll1_opy_(bstack1lllllll11l_opy_):
    bstack1l11llll111_opy_ = bstack11ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᓈ")
    NAME = bstack11ll111_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᓉ")
    bstack1l1l1lll111_opy_ = bstack11ll111_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥᓊ")
    bstack1l1l1ll1ll1_opy_ = bstack11ll111_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᓋ")
    bstack1l1111l1l1l_opy_ = bstack11ll111_opy_ (u"ࠦ࡮ࡴࡰࡶࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᓌ")
    bstack1l1ll1111ll_opy_ = bstack11ll111_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᓍ")
    bstack1l11lllll1l_opy_ = bstack11ll111_opy_ (u"ࠨࡩࡴࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡪࡸࡦࠧᓎ")
    bstack1l1111ll111_opy_ = bstack11ll111_opy_ (u"ࠢࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᓏ")
    bstack1l1111l1lll_opy_ = bstack11ll111_opy_ (u"ࠣࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᓐ")
    bstack1ll1l1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᓑ")
    bstack1l1l11l1ll1_opy_ = bstack11ll111_opy_ (u"ࠥࡲࡪࡽࡳࡦࡵࡶ࡭ࡴࡴࠢᓒ")
    bstack1l1111l1ll1_opy_ = bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࠣᓓ")
    bstack1l1lll1ll1l_opy_ = bstack11ll111_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᓔ")
    bstack1l11lll1l1l_opy_ = bstack11ll111_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᓕ")
    bstack1l11llll11l_opy_ = bstack11ll111_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᓖ")
    bstack1l1111l111l_opy_ = bstack11ll111_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᓗ")
    bstack1l1111l11l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11lll11_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1lll111_opy_: Any
    bstack1l11lll1lll_opy_: Dict
    def __init__(
        self,
        bstack1l1l11lll11_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1lll111_opy_: Dict[str, Any],
        methods=[bstack11ll111_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᓘ"), bstack11ll111_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᓙ"), bstack11ll111_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᓚ"), bstack11ll111_opy_ (u"ࠧࡷࡵࡪࡶࠥᓛ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11lll11_opy_ = bstack1l1l11lll11_opy_
        self.platform_index = platform_index
        self.bstack11111l1111_opy_(methods)
        self.bstack1lll1lll111_opy_ = bstack1lll1lll111_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1lllllll11l_opy_.get_data(bstack1llll1llll1_opy_.bstack1l1l1ll1ll1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1lllllll11l_opy_.get_data(bstack1llll1llll1_opy_.bstack1l1l1lll111_opy_, target, strict)
    @staticmethod
    def bstack1l1111l1l11_opy_(target: object, strict=True):
        return bstack1lllllll11l_opy_.get_data(bstack1llll1llll1_opy_.bstack1l1111l1l1l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1lllllll11l_opy_.get_data(bstack1llll1llll1_opy_.bstack1l1ll1111ll_opy_, target, strict)
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack1llllll1ll1_opy_) -> bool:
        return bstack1lllllll11l_opy_.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1l11lllll1l_opy_, False)
    @staticmethod
    def bstack1ll11lll111_opy_(instance: bstack1llllll1ll1_opy_, default_value=None):
        return bstack1lllllll11l_opy_.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1lll111_opy_, default_value)
    @staticmethod
    def bstack1ll1l11lll1_opy_(instance: bstack1llllll1ll1_opy_, default_value=None):
        return bstack1lllllll11l_opy_.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1l1ll1111ll_opy_, default_value)
    @staticmethod
    def bstack1ll11l1lll1_opy_(hub_url: str, bstack1l1111l11ll_opy_=bstack11ll111_opy_ (u"ࠨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥᓜ")):
        try:
            bstack1l1111ll11l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1111ll11l_opy_.endswith(bstack1l1111l11ll_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l1lll1l_opy_(method_name: str):
        return method_name == bstack11ll111_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᓝ")
    @staticmethod
    def bstack1ll1l1lllll_opy_(method_name: str, *args):
        return (
            bstack1llll1llll1_opy_.bstack1ll1l1lll1l_opy_(method_name)
            and bstack1llll1llll1_opy_.bstack1l1l11llll1_opy_(*args) == bstack1llll1llll1_opy_.bstack1l1l11l1ll1_opy_
        )
    @staticmethod
    def bstack1ll1l1l1l11_opy_(method_name: str, *args):
        if not bstack1llll1llll1_opy_.bstack1ll1l1lll1l_opy_(method_name):
            return False
        if not bstack1llll1llll1_opy_.bstack1l11lll1l1l_opy_ in bstack1llll1llll1_opy_.bstack1l1l11llll1_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1llll1llll1_opy_.bstack1ll11l1l1l1_opy_(*args)
        return bstack1ll11l11lll_opy_ and bstack11ll111_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᓞ") in bstack1ll11l11lll_opy_ and bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᓟ") in bstack1ll11l11lll_opy_[bstack11ll111_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᓠ")]
    @staticmethod
    def bstack1ll1l11111l_opy_(method_name: str, *args):
        if not bstack1llll1llll1_opy_.bstack1ll1l1lll1l_opy_(method_name):
            return False
        if not bstack1llll1llll1_opy_.bstack1l11lll1l1l_opy_ in bstack1llll1llll1_opy_.bstack1l1l11llll1_opy_(*args):
            return False
        bstack1ll11l11lll_opy_ = bstack1llll1llll1_opy_.bstack1ll11l1l1l1_opy_(*args)
        return (
            bstack1ll11l11lll_opy_
            and bstack11ll111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᓡ") in bstack1ll11l11lll_opy_
            and bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᓢ") in bstack1ll11l11lll_opy_[bstack11ll111_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓣ")]
        )
    @staticmethod
    def bstack1l1l11llll1_opy_(*args):
        return str(bstack1llll1llll1_opy_.bstack1ll1l1111l1_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l1111l1_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11l1l1l1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11l1lll11l_opy_(driver):
        command_executor = getattr(driver, bstack11ll111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᓤ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11ll111_opy_ (u"ࠣࡡࡸࡶࡱࠨᓥ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11ll111_opy_ (u"ࠤࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠥᓦ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11ll111_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡢࡷࡪࡸࡶࡦࡴࡢࡥࡩࡪࡲࠣᓧ"), None)
        return hub_url
    def bstack1l1l1l111l1_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11ll111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᓨ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11ll111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᓩ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11ll111_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᓪ")):
                setattr(command_executor, bstack11ll111_opy_ (u"ࠢࡠࡷࡵࡰࠧᓫ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11lll11_opy_ = hub_url
            bstack1llll1llll1_opy_.bstack111111ll11_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1lll111_opy_, hub_url)
            bstack1llll1llll1_opy_.bstack111111ll11_opy_(
                instance, bstack1llll1llll1_opy_.bstack1l11lllll1l_opy_, bstack1llll1llll1_opy_.bstack1ll11l1lll1_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11llll1l1_opy_(bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_]):
        return bstack11ll111_opy_ (u"ࠣ࠼ࠥᓬ").join((bstack11111l1l1l_opy_(bstack11111ll1l1_opy_[0]).name, bstack1llllll1l1l_opy_(bstack11111ll1l1_opy_[1]).name))
    @staticmethod
    def bstack1ll11llll1l_opy_(bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_], callback: Callable):
        bstack1l11lll11l1_opy_ = bstack1llll1llll1_opy_.bstack1l11llll1l1_opy_(bstack11111ll1l1_opy_)
        if not bstack1l11lll11l1_opy_ in bstack1llll1llll1_opy_.bstack1l1111l11l1_opy_:
            bstack1llll1llll1_opy_.bstack1l1111l11l1_opy_[bstack1l11lll11l1_opy_] = []
        bstack1llll1llll1_opy_.bstack1l1111l11l1_opy_[bstack1l11lll11l1_opy_].append(callback)
    def bstack11111l11ll_opy_(self, instance: bstack1llllll1ll1_opy_, method_name: str, bstack1llllll11ll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11ll111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᓭ")):
            return
        cmd = args[0] if method_name == bstack11ll111_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᓮ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l1111l1111_opy_ = bstack11ll111_opy_ (u"ࠦ࠿ࠨᓯ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠨᓰ") + bstack1l1111l1111_opy_, bstack1llllll11ll_opy_)
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
        bstack1l11lll11l1_opy_ = bstack1llll1llll1_opy_.bstack1l11llll1l1_opy_(bstack11111ll1l1_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡯࡯ࡡ࡫ࡳࡴࡱ࠺ࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᓱ") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣᓲ"))
        if bstack1lllllll111_opy_ == bstack11111l1l1l_opy_.QUIT:
            if bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.PRE:
                bstack1ll1l111ll1_opy_ = bstack1llll11l1ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1ll11l1l1_opy_.value)
                bstack1lllllll11l_opy_.bstack111111ll11_opy_(instance, EVENTS.bstack1ll11l1l1_opy_.value, bstack1ll1l111ll1_opy_)
                self.logger.debug(bstack11ll111_opy_ (u"ࠣ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠧᓳ").format(instance, method_name, bstack1lllllll111_opy_, bstack1l11lll11ll_opy_))
        if bstack1lllllll111_opy_ == bstack11111l1l1l_opy_.bstack111111l1ll_opy_:
            if bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.POST and not bstack1llll1llll1_opy_.bstack1l1l1ll1ll1_opy_ in instance.data:
                session_id = getattr(target, bstack11ll111_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᓴ"), None)
                if session_id:
                    instance.data[bstack1llll1llll1_opy_.bstack1l1l1ll1ll1_opy_] = session_id
        elif (
            bstack1lllllll111_opy_ == bstack11111l1l1l_opy_.bstack11111ll1ll_opy_
            and bstack1llll1llll1_opy_.bstack1l1l11llll1_opy_(*args) == bstack1llll1llll1_opy_.bstack1l1l11l1ll1_opy_
        ):
            if bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.PRE:
                hub_url = bstack1llll1llll1_opy_.bstack11l1lll11l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llll1llll1_opy_.bstack1l1l1lll111_opy_: hub_url,
                            bstack1llll1llll1_opy_.bstack1l11lllll1l_opy_: bstack1llll1llll1_opy_.bstack1ll11l1lll1_opy_(hub_url),
                            bstack1llll1llll1_opy_.bstack1ll1l1l1l1l_opy_: int(
                                os.environ.get(bstack11ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᓵ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11l11lll_opy_ = bstack1llll1llll1_opy_.bstack1ll11l1l1l1_opy_(*args)
                bstack1l1111l1l11_opy_ = bstack1ll11l11lll_opy_.get(bstack11ll111_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᓶ"), None) if bstack1ll11l11lll_opy_ else None
                if isinstance(bstack1l1111l1l11_opy_, dict):
                    instance.data[bstack1llll1llll1_opy_.bstack1l1111l1l1l_opy_] = copy.deepcopy(bstack1l1111l1l11_opy_)
                    instance.data[bstack1llll1llll1_opy_.bstack1l1ll1111ll_opy_] = bstack1l1111l1l11_opy_
            elif bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11ll111_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᓷ"), dict()).get(bstack11ll111_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᓸ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llll1llll1_opy_.bstack1l1l1ll1ll1_opy_: framework_session_id,
                                bstack1llll1llll1_opy_.bstack1l1111ll111_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lllllll111_opy_ == bstack11111l1l1l_opy_.bstack11111ll1ll_opy_
            and bstack1llll1llll1_opy_.bstack1l1l11llll1_opy_(*args) == bstack1llll1llll1_opy_.bstack1l1111l111l_opy_
            and bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.POST
        ):
            instance.data[bstack1llll1llll1_opy_.bstack1l1111l1lll_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11lll11l1_opy_ in bstack1llll1llll1_opy_.bstack1l1111l11l1_opy_:
            bstack1l11lll1l11_opy_ = None
            for callback in bstack1llll1llll1_opy_.bstack1l1111l11l1_opy_[bstack1l11lll11l1_opy_]:
                try:
                    bstack1l11lll1ll1_opy_ = callback(self, target, exec, bstack11111ll1l1_opy_, result, *args, **kwargs)
                    if bstack1l11lll1l11_opy_ == None:
                        bstack1l11lll1l11_opy_ = bstack1l11lll1ll1_opy_
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᓹ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤᓺ"))
                    traceback.print_exc()
            if bstack1lllllll111_opy_ == bstack11111l1l1l_opy_.QUIT:
                if bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.POST:
                    bstack1ll1l111ll1_opy_ = bstack1lllllll11l_opy_.bstack1llllll1lll_opy_(instance, EVENTS.bstack1ll11l1l1_opy_.value)
                    if bstack1ll1l111ll1_opy_!=None:
                        bstack1llll11l1ll_opy_.end(EVENTS.bstack1ll11l1l1_opy_.value, bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᓻ"), bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᓼ"), True, None)
            if bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.PRE and callable(bstack1l11lll1l11_opy_):
                return bstack1l11lll1l11_opy_
            elif bstack1l11lll11ll_opy_ == bstack1llllll1l1l_opy_.POST and bstack1l11lll1l11_opy_:
                return bstack1l11lll1l11_opy_
    def bstack11111111ll_opy_(
        self, method_name, previous_state: bstack11111l1l1l_opy_, *args, **kwargs
    ) -> bstack11111l1l1l_opy_:
        if method_name == bstack11ll111_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᓽ") or method_name == bstack11ll111_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᓾ"):
            return bstack11111l1l1l_opy_.bstack111111l1ll_opy_
        if method_name == bstack11ll111_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᓿ"):
            return bstack11111l1l1l_opy_.QUIT
        if method_name == bstack11ll111_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᔀ"):
            if previous_state != bstack11111l1l1l_opy_.NONE:
                bstack1ll1l11l1ll_opy_ = bstack1llll1llll1_opy_.bstack1l1l11llll1_opy_(*args)
                if bstack1ll1l11l1ll_opy_ == bstack1llll1llll1_opy_.bstack1l1l11l1ll1_opy_:
                    return bstack11111l1l1l_opy_.bstack111111l1ll_opy_
            return bstack11111l1l1l_opy_.bstack11111ll1ll_opy_
        return bstack11111l1l1l_opy_.NONE