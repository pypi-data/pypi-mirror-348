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
import threading
import logging
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from bstack_utils.helper import bstack1lll1ll1ll_opy_
logger = logging.getLogger(__name__)
def bstack11l111l1_opy_(bstack111l1l1l1_opy_):
  return True if bstack111l1l1l1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll11111ll_opy_(context, *args):
    tags = getattr(args[0], bstack11ll111_opy_ (u"ࠧࡵࡣࡪࡷࠬᙬ"), [])
    bstack1lll1llll1_opy_ = bstack1ll11llll1_opy_.bstack11ll1l11ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1lll1llll1_opy_
    try:
      bstack11ll11l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l111l1_opy_(bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ᙭")) else context.browser
      if bstack11ll11l1_opy_ and bstack11ll11l1_opy_.session_id and bstack1lll1llll1_opy_ and bstack1lll1ll1ll_opy_(
              threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᙮"), None):
          threading.current_thread().isA11yTest = bstack1ll11llll1_opy_.bstack1l1l1ll111_opy_(bstack11ll11l1_opy_, bstack1lll1llll1_opy_)
    except Exception as e:
       logger.debug(bstack11ll111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪᙯ").format(str(e)))
def bstack11l11lll1_opy_(bstack11ll11l1_opy_):
    if bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᙰ"), None) and bstack1lll1ll1ll_opy_(
      threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᙱ"), None) and not bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩᙲ"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll11llll1_opy_.bstack1l1l111ll_opy_(bstack11ll11l1_opy_, name=bstack11ll111_opy_ (u"ࠢࠣᙳ"), path=bstack11ll111_opy_ (u"ࠣࠤᙴ"))