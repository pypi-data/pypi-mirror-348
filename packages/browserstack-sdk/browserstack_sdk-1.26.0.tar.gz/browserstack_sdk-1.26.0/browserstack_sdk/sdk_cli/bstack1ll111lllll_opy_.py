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
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lllllll11l_opy_,
    bstack1llllll1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lllll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack11111lll1l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
import weakref
class bstack1ll11l11l1l_opy_(bstack1lll1l1111l_opy_):
    bstack1ll111llll1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1llllll1ll1_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1llllll1ll1_opy_]]
    def __init__(self, bstack1ll111llll1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll111ll1l1_opy_ = dict()
        self.bstack1ll111llll1_opy_ = bstack1ll111llll1_opy_
        self.frameworks = frameworks
        bstack1lllll1lll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack111111l1ll_opy_, bstack1llllll1l1l_opy_.POST), self.__1ll11l11l11_opy_)
        if any(bstack1llll1llll1_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1llll1llll1_opy_.bstack1ll11llll1l_opy_(
                (bstack11111l1l1l_opy_.bstack11111ll1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.__1ll111lll11_opy_
            )
            bstack1llll1llll1_opy_.bstack1ll11llll1l_opy_(
                (bstack11111l1l1l_opy_.QUIT, bstack1llllll1l1l_opy_.POST), self.__1ll11l111ll_opy_
            )
    def __1ll11l11l11_opy_(
        self,
        f: bstack1lllll1lll1_opy_,
        bstack1ll111lll1l_opy_: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack11ll111_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᆮ"):
                return
            contexts = bstack1ll111lll1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack11ll111_opy_ (u"ࠧࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠥᆯ") in page.url:
                                self.logger.debug(bstack11ll111_opy_ (u"ࠨࡓࡵࡱࡵ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡳ࡫ࡷࠡࡲࡤ࡫ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣᆰ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1lllllll11l_opy_.bstack111111ll11_opy_(instance, self.bstack1ll111llll1_opy_, True)
                                self.logger.debug(bstack11ll111_opy_ (u"ࠢࡠࡡࡲࡲࡤࡶࡡࡨࡧࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᆱ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠣࠤᆲ"))
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࠿ࠨᆳ"),e)
    def __1ll111lll11_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1lllllll11l_opy_.bstack1llllll1lll_opy_(instance, self.bstack1ll111llll1_opy_, False):
            return
        if not f.bstack1ll11l1lll1_opy_(f.hub_url(driver)):
            self.bstack1ll111ll1l1_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1lllllll11l_opy_.bstack111111ll11_opy_(instance, self.bstack1ll111llll1_opy_, True)
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢࡱࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡪࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᆴ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠦࠧᆵ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1lllllll11l_opy_.bstack111111ll11_opy_(instance, self.bstack1ll111llll1_opy_, True)
        self.logger.debug(bstack11ll111_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᆶ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠨࠢᆷ"))
    def __1ll11l111ll_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11l111l1_opy_(instance)
        self.logger.debug(bstack11ll111_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡲࡷ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᆸ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠣࠤᆹ"))
    def bstack1ll111ll1ll_opy_(self, context: bstack11111lll1l_opy_, reverse=True) -> List[Tuple[Callable, bstack1llllll1ll1_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll11l11111_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1llll1llll1_opy_.bstack1ll11llllll_opy_(data[1])
                    and data[1].bstack1ll11l11111_opy_(context)
                    and getattr(data[0](), bstack11ll111_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᆺ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111l1ll1_opy_, reverse=reverse)
    def bstack1ll111ll11l_opy_(self, context: bstack11111lll1l_opy_, reverse=True) -> List[Tuple[Callable, bstack1llllll1ll1_opy_]]:
        matches = []
        for data in self.bstack1ll111ll1l1_opy_.values():
            if (
                data[1].bstack1ll11l11111_opy_(context)
                and getattr(data[0](), bstack11ll111_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᆻ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111l1ll1_opy_, reverse=reverse)
    def bstack1ll11l1111l_opy_(self, instance: bstack1llllll1ll1_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11l111l1_opy_(self, instance: bstack1llllll1ll1_opy_) -> bool:
        if self.bstack1ll11l1111l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1lllllll11l_opy_.bstack111111ll11_opy_(instance, self.bstack1ll111llll1_opy_, False)
            return True
        return False