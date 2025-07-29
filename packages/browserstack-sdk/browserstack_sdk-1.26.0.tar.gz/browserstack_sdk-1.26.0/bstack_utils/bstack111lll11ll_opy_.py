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
import threading
from bstack_utils.helper import bstack11lll11ll_opy_
from bstack_utils.constants import bstack11ll11lll11_opy_, EVENTS, STAGE
from bstack_utils.bstack1l1l1ll11l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11ll11_opy_:
    bstack111l111llll_opy_ = None
    @classmethod
    def bstack11l11lllll_opy_(cls):
        if cls.on() and os.getenv(bstack11ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥὩ")):
            logger.info(
                bstack11ll111_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩὪ").format(os.getenv(bstack11ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧὫ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬὬ"), None) is None or os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ὥ")] == bstack11ll111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣὮ"):
            return False
        return True
    @classmethod
    def bstack1111l111l1l_opy_(cls, bs_config, framework=bstack11ll111_opy_ (u"ࠦࠧὯ")):
        bstack11ll1llll11_opy_ = False
        for fw in bstack11ll11lll11_opy_:
            if fw in framework:
                bstack11ll1llll11_opy_ = True
        return bstack11lll11ll_opy_(bs_config.get(bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩὰ"), bstack11ll1llll11_opy_))
    @classmethod
    def bstack1111l11111l_opy_(cls, framework):
        return framework in bstack11ll11lll11_opy_
    @classmethod
    def bstack1111ll11l11_opy_(cls, bs_config, framework):
        return cls.bstack1111l111l1l_opy_(bs_config, framework) is True and cls.bstack1111l11111l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪά"), None)
    @staticmethod
    def bstack111lllll11_opy_():
        if getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫὲ"), None):
            return {
                bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭έ"): bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺࠧὴ"),
                bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪή"): getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨὶ"), None)
            }
        if getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩί"), None):
            return {
                bstack11ll111_opy_ (u"࠭ࡴࡺࡲࡨࠫὸ"): bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࠬό"),
                bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨὺ"): getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ύ"), None)
            }
        return None
    @staticmethod
    def bstack1111l1111ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11ll11ll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111ll1lll1_opy_(test, hook_name=None):
        bstack1111l111111_opy_ = test.parent
        if hook_name in [bstack11ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨὼ"), bstack11ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬώ"), bstack11ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ὾"), bstack11ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ὿")]:
            bstack1111l111111_opy_ = test
        scope = []
        while bstack1111l111111_opy_ is not None:
            scope.append(bstack1111l111111_opy_.name)
            bstack1111l111111_opy_ = bstack1111l111111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack11111llllll_opy_(hook_type):
        if hook_type == bstack11ll111_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧᾀ"):
            return bstack11ll111_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧᾁ")
        elif hook_type == bstack11ll111_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨᾂ"):
            return bstack11ll111_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥᾃ")
    @staticmethod
    def bstack1111l1111l1_opy_(bstack11l1l1ll_opy_):
        try:
            if not bstack11ll11ll11_opy_.on():
                return bstack11l1l1ll_opy_
            if os.environ.get(bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤᾄ"), None) == bstack11ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥᾅ"):
                tests = os.environ.get(bstack11ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥᾆ"), None)
                if tests is None or tests == bstack11ll111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᾇ"):
                    return bstack11l1l1ll_opy_
                bstack11l1l1ll_opy_ = tests.split(bstack11ll111_opy_ (u"ࠨ࠮ࠪᾈ"))
                return bstack11l1l1ll_opy_
        except Exception as exc:
            logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥᾉ") + str(str(exc)) + bstack11ll111_opy_ (u"ࠥࠦᾊ"))
        return bstack11l1l1ll_opy_