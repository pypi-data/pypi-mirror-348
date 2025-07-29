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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll1l11l1_opy_, bstack11lll1ll1_opy_, get_host_info, bstack11l1ll1l1ll_opy_, \
 bstack111l11lll_opy_, bstack1lll1ll1ll_opy_, bstack111l1ll11l_opy_, bstack11l1ll11l1l_opy_, bstack1l1l1llll_opy_
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11ll11ll11_opy_
from bstack_utils.percy import bstack1l11l1llll_opy_
from bstack_utils.config import Config
bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l11l1llll_opy_()
@bstack111l1ll11l_opy_(class_method=False)
def bstack1111l1ll1ll_opy_(bs_config, bstack1ll1ll1ll1_opy_):
  try:
    data = {
        bstack11ll111_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫἢ"): bstack11ll111_opy_ (u"ࠬࡰࡳࡰࡰࠪἣ"),
        bstack11ll111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬἤ"): bs_config.get(bstack11ll111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬἥ"), bstack11ll111_opy_ (u"ࠨࠩἦ")),
        bstack11ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧἧ"): bs_config.get(bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭Ἠ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧἩ"): bs_config.get(bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧἪ")),
        bstack11ll111_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫἫ"): bs_config.get(bstack11ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪἬ"), bstack11ll111_opy_ (u"ࠨࠩἭ")),
        bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ἦ"): bstack1l1l1llll_opy_(),
        bstack11ll111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨἯ"): bstack11l1ll1l1ll_opy_(bs_config),
        bstack11ll111_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧἰ"): get_host_info(),
        bstack11ll111_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ἱ"): bstack11lll1ll1_opy_(),
        bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ἲ"): os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ἳ")),
        bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ἴ"): os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧἵ"), False),
        bstack11ll111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬἶ"): bstack11lll1l11l1_opy_(),
        bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫἷ"): bstack1111l11l1ll_opy_(),
        bstack11ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩἸ"): bstack1111l111ll1_opy_(bstack1ll1ll1ll1_opy_),
        bstack11ll111_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫἹ"): bstack1111l11ll11_opy_(bs_config, bstack1ll1ll1ll1_opy_.get(bstack11ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨἺ"), bstack11ll111_opy_ (u"ࠨࠩἻ"))),
        bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫἼ"): bstack111l11lll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦἽ").format(str(error)))
    return None
def bstack1111l111ll1_opy_(framework):
  return {
    bstack11ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫἾ"): framework.get(bstack11ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭Ἷ"), bstack11ll111_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ὀ")),
    bstack11ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪὁ"): framework.get(bstack11ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬὂ")),
    bstack11ll111_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ὃ"): framework.get(bstack11ll111_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨὄ")),
    bstack11ll111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ὅ"): bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ὆"),
    bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭὇"): framework.get(bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧὈ"))
  }
def bstack1lllll11_opy_(bs_config, framework):
  bstack11l1l1l1ll_opy_ = False
  bstack1l111l1l1_opy_ = False
  bstack1111l111l11_opy_ = False
  if bstack11ll111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬὉ") in bs_config:
    bstack1111l111l11_opy_ = True
  elif bstack11ll111_opy_ (u"ࠩࡤࡴࡵ࠭Ὂ") in bs_config:
    bstack11l1l1l1ll_opy_ = True
  else:
    bstack1l111l1l1_opy_ = True
  bstack1l1l1l1ll_opy_ = {
    bstack11ll111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪὋ"): bstack11ll11ll11_opy_.bstack1111l111l1l_opy_(bs_config, framework),
    bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫὌ"): bstack1ll11llll1_opy_.bstack11l111l11_opy_(bs_config),
    bstack11ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫὍ"): bs_config.get(bstack11ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ὎"), False),
    bstack11ll111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ὏"): bstack1l111l1l1_opy_,
    bstack11ll111_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧὐ"): bstack11l1l1l1ll_opy_,
    bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ὑ"): bstack1111l111l11_opy_
  }
  return bstack1l1l1l1ll_opy_
@bstack111l1ll11l_opy_(class_method=False)
def bstack1111l11l1ll_opy_():
  try:
    bstack1111l11l1l1_opy_ = json.loads(os.getenv(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫὒ"), bstack11ll111_opy_ (u"ࠫࢀࢃࠧὓ")))
    return {
        bstack11ll111_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧὔ"): bstack1111l11l1l1_opy_
    }
  except Exception as error:
    logger.error(bstack11ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧὕ").format(str(error)))
    return {}
def bstack1111ll1l11l_opy_(array, bstack1111l111lll_opy_, bstack1111l11ll1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l111lll_opy_]
    result[key] = o[bstack1111l11ll1l_opy_]
  return result
def bstack1111ll1l111_opy_(bstack11l1llll1_opy_=bstack11ll111_opy_ (u"ࠧࠨὖ")):
  bstack1111l11lll1_opy_ = bstack1ll11llll1_opy_.on()
  bstack1111l11llll_opy_ = bstack11ll11ll11_opy_.on()
  bstack1111l11l111_opy_ = percy.bstack11l1l111_opy_()
  if bstack1111l11l111_opy_ and not bstack1111l11llll_opy_ and not bstack1111l11lll1_opy_:
    return bstack11l1llll1_opy_ not in [bstack11ll111_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬὗ"), bstack11ll111_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭὘")]
  elif bstack1111l11lll1_opy_ and not bstack1111l11llll_opy_:
    return bstack11l1llll1_opy_ not in [bstack11ll111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫὙ"), bstack11ll111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭὚"), bstack11ll111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩὛ")]
  return bstack1111l11lll1_opy_ or bstack1111l11llll_opy_ or bstack1111l11l111_opy_
@bstack111l1ll11l_opy_(class_method=False)
def bstack1111l1l1l11_opy_(bstack11l1llll1_opy_, test=None):
  bstack1111l11l11l_opy_ = bstack1ll11llll1_opy_.on()
  if not bstack1111l11l11l_opy_ or bstack11l1llll1_opy_ not in [bstack11ll111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ὜")] or test == None:
    return None
  return {
    bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧὝ"): bstack1111l11l11l_opy_ and bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ὞"), None) == True and bstack1ll11llll1_opy_.bstack11ll1l11ll_opy_(test[bstack11ll111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧὟ")])
  }
def bstack1111l11ll11_opy_(bs_config, framework):
  bstack11l1l1l1ll_opy_ = False
  bstack1l111l1l1_opy_ = False
  bstack1111l111l11_opy_ = False
  if bstack11ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧὠ") in bs_config:
    bstack1111l111l11_opy_ = True
  elif bstack11ll111_opy_ (u"ࠫࡦࡶࡰࠨὡ") in bs_config:
    bstack11l1l1l1ll_opy_ = True
  else:
    bstack1l111l1l1_opy_ = True
  bstack1l1l1l1ll_opy_ = {
    bstack11ll111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬὢ"): bstack11ll11ll11_opy_.bstack1111l111l1l_opy_(bs_config, framework),
    bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ὣ"): bstack1ll11llll1_opy_.bstack1ll111l11l_opy_(bs_config),
    bstack11ll111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ὤ"): bs_config.get(bstack11ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧὥ"), False),
    bstack11ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫὦ"): bstack1l111l1l1_opy_,
    bstack11ll111_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩὧ"): bstack11l1l1l1ll_opy_,
    bstack11ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨὨ"): bstack1111l111l11_opy_
  }
  return bstack1l1l1l1ll_opy_