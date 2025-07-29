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
from browserstack_sdk.bstack1l11lll1ll_opy_ import bstack1lll1111l_opy_
from browserstack_sdk.bstack111ll111l1_opy_ import RobotHandler
def bstack1l1111ll11_opy_(framework):
    if framework.lower() == bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᦵ"):
        return bstack1lll1111l_opy_.version()
    elif framework.lower() == bstack11ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᦶ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11ll111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᦷ"):
        import behave
        return behave.__version__
    else:
        return bstack11ll111_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬᦸ")
def bstack1ll11ll111_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11ll111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᦹ"))
        framework_version.append(importlib.metadata.version(bstack11ll111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᦺ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᦻ"))
        framework_version.append(importlib.metadata.version(bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᦼ")))
    except:
        pass
    return {
        bstack11ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᦽ"): bstack11ll111_opy_ (u"ࠪࡣࠬᦾ").join(framework_name),
        bstack11ll111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᦿ"): bstack11ll111_opy_ (u"ࠬࡥࠧᧀ").join(framework_version)
    }