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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11lllll111l_opy_ as bstack11llll1lll1_opy_, EVENTS
from bstack_utils.bstack1l11ll111l_opy_ import bstack1l11ll111l_opy_
from bstack_utils.helper import bstack1l1l1llll_opy_, bstack111l11l1l1_opy_, bstack111l11lll_opy_, bstack11llll11111_opy_, \
  bstack11lll1l1l11_opy_, bstack11lll1ll1_opy_, get_host_info, bstack11lll1l11l1_opy_, bstack11ll111ll1_opy_, bstack111l1ll11l_opy_, bstack1lll1ll1ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l1l1ll11l_opy_ import get_logger
from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1l1l11llll_opy_ = bstack1llll11l1ll_opy_()
@bstack111l1ll11l_opy_(class_method=False)
def _11llll1ll11_opy_(driver, bstack1111ll11l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11ll111_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬᕦ"): caps.get(bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᕧ"), None),
        bstack11ll111_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᕨ"): bstack1111ll11l1_opy_.get(bstack11ll111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᕩ"), None),
        bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᕪ"): caps.get(bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᕫ"), None),
        bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᕬ"): caps.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᕭ"), None)
    }
  except Exception as error:
    logger.debug(bstack11ll111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᕮ") + str(error))
  return response
def on():
    if os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᕯ"), None) is None or os.environ[bstack11ll111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᕰ")] == bstack11ll111_opy_ (u"ࠣࡰࡸࡰࡱࠨᕱ"):
        return False
    return True
def bstack11l111l11_opy_(config):
  return config.get(bstack11ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᕲ"), False) or any([p.get(bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᕳ"), False) == True for p in config.get(bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕴ"), [])])
def bstack11lll1l1ll_opy_(config, bstack11l1l111ll_opy_):
  try:
    if not bstack111l11lll_opy_(config):
      return False
    bstack11lll1ll11l_opy_ = config.get(bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕵ"), False)
    if int(bstack11l1l111ll_opy_) < len(config.get(bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᕶ"), [])) and config[bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᕷ")][bstack11l1l111ll_opy_]:
      bstack11llll1l1l1_opy_ = config[bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᕸ")][bstack11l1l111ll_opy_].get(bstack11ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᕹ"), None)
    else:
      bstack11llll1l1l1_opy_ = config.get(bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᕺ"), None)
    if bstack11llll1l1l1_opy_ != None:
      bstack11lll1ll11l_opy_ = bstack11llll1l1l1_opy_
    bstack11llll11lll_opy_ = os.getenv(bstack11ll111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᕻ")) is not None and len(os.getenv(bstack11ll111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᕼ"))) > 0 and os.getenv(bstack11ll111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᕽ")) != bstack11ll111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᕾ")
    return bstack11lll1ll11l_opy_ and bstack11llll11lll_opy_
  except Exception as error:
    logger.debug(bstack11ll111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᕿ") + str(error))
  return False
def bstack11ll1l11ll_opy_(test_tags):
  bstack1ll11lllll1_opy_ = os.getenv(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᖀ"))
  if bstack1ll11lllll1_opy_ is None:
    return True
  bstack1ll11lllll1_opy_ = json.loads(bstack1ll11lllll1_opy_)
  try:
    include_tags = bstack1ll11lllll1_opy_[bstack11ll111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᖁ")] if bstack11ll111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᖂ") in bstack1ll11lllll1_opy_ and isinstance(bstack1ll11lllll1_opy_[bstack11ll111_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᖃ")], list) else []
    exclude_tags = bstack1ll11lllll1_opy_[bstack11ll111_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᖄ")] if bstack11ll111_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᖅ") in bstack1ll11lllll1_opy_ and isinstance(bstack1ll11lllll1_opy_[bstack11ll111_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᖆ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᖇ") + str(error))
  return False
def bstack11llll11l11_opy_(config, bstack11lll1ll1l1_opy_, bstack11lll1l1lll_opy_, bstack11lll1l111l_opy_):
  bstack11llll1ll1l_opy_ = bstack11llll11111_opy_(config)
  bstack11llll11ll1_opy_ = bstack11lll1l1l11_opy_(config)
  if bstack11llll1ll1l_opy_ is None or bstack11llll11ll1_opy_ is None:
    logger.error(bstack11ll111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᖈ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᖉ"), bstack11ll111_opy_ (u"ࠬࢁࡽࠨᖊ")))
    data = {
        bstack11ll111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᖋ"): config[bstack11ll111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᖌ")],
        bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᖍ"): config.get(bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᖎ"), os.path.basename(os.getcwd())),
        bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ᖏ"): bstack1l1l1llll_opy_(),
        bstack11ll111_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᖐ"): config.get(bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᖑ"), bstack11ll111_opy_ (u"࠭ࠧᖒ")),
        bstack11ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᖓ"): {
            bstack11ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᖔ"): bstack11lll1ll1l1_opy_,
            bstack11ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᖕ"): bstack11lll1l1lll_opy_,
            bstack11ll111_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᖖ"): __version__,
            bstack11ll111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᖗ"): bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᖘ"),
            bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᖙ"): bstack11ll111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᖚ"),
            bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖛ"): bstack11lll1l111l_opy_
        },
        bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᖜ"): settings,
        bstack11ll111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᖝ"): bstack11lll1l11l1_opy_(),
        bstack11ll111_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᖞ"): bstack11lll1ll1_opy_(),
        bstack11ll111_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᖟ"): get_host_info(),
        bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᖠ"): bstack111l11lll_opy_(config)
    }
    headers = {
        bstack11ll111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᖡ"): bstack11ll111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᖢ"),
    }
    config = {
        bstack11ll111_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᖣ"): (bstack11llll1ll1l_opy_, bstack11llll11ll1_opy_),
        bstack11ll111_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᖤ"): headers
    }
    response = bstack11ll111ll1_opy_(bstack11ll111_opy_ (u"ࠫࡕࡕࡓࡕࠩᖥ"), bstack11llll1lll1_opy_ + bstack11ll111_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᖦ"), data, config)
    bstack11llll1l11l_opy_ = response.json()
    if bstack11llll1l11l_opy_[bstack11ll111_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᖧ")]:
      parsed = json.loads(os.getenv(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᖨ"), bstack11ll111_opy_ (u"ࠨࡽࢀࠫᖩ")))
      parsed[bstack11ll111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᖪ")] = bstack11llll1l11l_opy_[bstack11ll111_opy_ (u"ࠪࡨࡦࡺࡡࠨᖫ")][bstack11ll111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᖬ")]
      os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᖭ")] = json.dumps(parsed)
      bstack1l11ll111l_opy_.bstack11ll111l1l_opy_(bstack11llll1l11l_opy_[bstack11ll111_opy_ (u"࠭ࡤࡢࡶࡤࠫᖮ")][bstack11ll111_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᖯ")])
      bstack1l11ll111l_opy_.bstack11lll1lll11_opy_(bstack11llll1l11l_opy_[bstack11ll111_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖰ")][bstack11ll111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᖱ")])
      bstack1l11ll111l_opy_.store()
      return bstack11llll1l11l_opy_[bstack11ll111_opy_ (u"ࠪࡨࡦࡺࡡࠨᖲ")][bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᖳ")], bstack11llll1l11l_opy_[bstack11ll111_opy_ (u"ࠬࡪࡡࡵࡣࠪᖴ")][bstack11ll111_opy_ (u"࠭ࡩࡥࠩᖵ")]
    else:
      logger.error(bstack11ll111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᖶ") + bstack11llll1l11l_opy_[bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖷ")])
      if bstack11llll1l11l_opy_[bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖸ")] == bstack11ll111_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᖹ"):
        for bstack11lll1ll111_opy_ in bstack11llll1l11l_opy_[bstack11ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᖺ")]:
          logger.error(bstack11lll1ll111_opy_[bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖻ")])
      return None, None
  except Exception as error:
    logger.error(bstack11ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᖼ") +  str(error))
    return None, None
def bstack11llll1llll_opy_():
  if os.getenv(bstack11ll111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᖽ")) is None:
    return {
        bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᖾ"): bstack11ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᖿ"),
        bstack11ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᗀ"): bstack11ll111_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪᗁ")
    }
  data = {bstack11ll111_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ᗂ"): bstack1l1l1llll_opy_()}
  headers = {
      bstack11ll111_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᗃ"): bstack11ll111_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨᗄ") + os.getenv(bstack11ll111_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨᗅ")),
      bstack11ll111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᗆ"): bstack11ll111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᗇ")
  }
  response = bstack11ll111ll1_opy_(bstack11ll111_opy_ (u"ࠫࡕ࡛ࡔࠨᗈ"), bstack11llll1lll1_opy_ + bstack11ll111_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧᗉ"), data, { bstack11ll111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᗊ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11ll111_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣᗋ") + bstack111l11l1l1_opy_().isoformat() + bstack11ll111_opy_ (u"ࠨ࡜ࠪᗌ"))
      return {bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᗍ"): bstack11ll111_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᗎ"), bstack11ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᗏ"): bstack11ll111_opy_ (u"ࠬ࠭ᗐ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤᗑ") + str(error))
    return {
        bstack11ll111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᗒ"): bstack11ll111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᗓ"),
        bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᗔ"): str(error)
    }
def bstack11llll1l111_opy_(bstack11lll1lllll_opy_):
    return re.match(bstack11ll111_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫᗕ"), bstack11lll1lllll_opy_.strip()) is not None
def bstack11l1ll1l11_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11llll1111l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11llll1111l_opy_ = desired_capabilities
        else:
          bstack11llll1111l_opy_ = {}
        bstack11lll1l1l1l_opy_ = (bstack11llll1111l_opy_.get(bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᗖ"), bstack11ll111_opy_ (u"ࠬ࠭ᗗ")).lower() or caps.get(bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᗘ"), bstack11ll111_opy_ (u"ࠧࠨᗙ")).lower())
        if bstack11lll1l1l1l_opy_ == bstack11ll111_opy_ (u"ࠨ࡫ࡲࡷࠬᗚ"):
            return True
        if bstack11lll1l1l1l_opy_ == bstack11ll111_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᗛ"):
            bstack11llll11l1l_opy_ = str(float(caps.get(bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗜ")) or bstack11llll1111l_opy_.get(bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᗝ"), {}).get(bstack11ll111_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗞ"),bstack11ll111_opy_ (u"࠭ࠧᗟ"))))
            if bstack11lll1l1l1l_opy_ == bstack11ll111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᗠ") and int(bstack11llll11l1l_opy_.split(bstack11ll111_opy_ (u"ࠨ࠰ࠪᗡ"))[0]) < float(bstack11lll1l11ll_opy_):
                logger.warning(str(bstack11lll1llll1_opy_))
                return False
            return True
        bstack1ll1l1lll11_opy_ = caps.get(bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗢ"), {}).get(bstack11ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᗣ"), caps.get(bstack11ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᗤ"), bstack11ll111_opy_ (u"ࠬ࠭ᗥ")))
        if bstack1ll1l1lll11_opy_:
            logger.warn(bstack11ll111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᗦ"))
            return False
        browser = caps.get(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᗧ"), bstack11ll111_opy_ (u"ࠨࠩᗨ")).lower() or bstack11llll1111l_opy_.get(bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᗩ"), bstack11ll111_opy_ (u"ࠪࠫᗪ")).lower()
        if browser != bstack11ll111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᗫ"):
            logger.warning(bstack11ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᗬ"))
            return False
        browser_version = caps.get(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗭ")) or caps.get(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᗮ")) or bstack11llll1111l_opy_.get(bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᗯ")) or bstack11llll1111l_opy_.get(bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗰ"), {}).get(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᗱ")) or bstack11llll1111l_opy_.get(bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᗲ"), {}).get(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᗳ"))
        if browser_version and browser_version != bstack11ll111_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᗴ") and int(browser_version.split(bstack11ll111_opy_ (u"ࠧ࠯ࠩᗵ"))[0]) <= 98:
            logger.warning(bstack11ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢ࠼࠼࠳ࠨᗶ"))
            return False
        if not options:
            bstack1ll1l11llll_opy_ = caps.get(bstack11ll111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᗷ")) or bstack11llll1111l_opy_.get(bstack11ll111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᗸ"), {})
            if bstack11ll111_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᗹ") in bstack1ll1l11llll_opy_.get(bstack11ll111_opy_ (u"ࠬࡧࡲࡨࡵࠪᗺ"), []):
                logger.warn(bstack11ll111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᗻ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack11ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᗼ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1llll111l1l_opy_ = config.get(bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᗽ"), {})
    bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᗾ")] = os.getenv(bstack11ll111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᗿ"))
    bstack11llll111ll_opy_ = json.loads(os.getenv(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᘀ"), bstack11ll111_opy_ (u"ࠬࢁࡽࠨᘁ"))).get(bstack11ll111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᘂ"))
    caps[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘃ")] = True
    if not config[bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᘄ")].get(bstack11ll111_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣᘅ")):
      if bstack11ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᘆ") in caps:
        caps[bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘇ")][bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᘈ")] = bstack1llll111l1l_opy_
        caps[bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘉ")][bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᘊ")][bstack11ll111_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᘋ")] = bstack11llll111ll_opy_
      else:
        caps[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᘌ")] = bstack1llll111l1l_opy_
        caps[bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᘍ")][bstack11ll111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘎ")] = bstack11llll111ll_opy_
  except Exception as error:
    logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨᘏ") +  str(error))
def bstack1l1l1ll111_opy_(driver, bstack11lllll1111_opy_):
  try:
    setattr(driver, bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᘐ"), True)
    session = driver.session_id
    if session:
      bstack11lll1l1ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1l1ll1_opy_ = False
      bstack11lll1l1ll1_opy_ = url.scheme in [bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴࠧᘑ"), bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢᘒ")]
      if bstack11lll1l1ll1_opy_:
        if bstack11lllll1111_opy_:
          logger.info(bstack11ll111_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡨࡲࡶࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲ࠥࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡧ࡫ࡧࡪࡰࠣࡱࡴࡳࡥ࡯ࡶࡤࡶ࡮ࡲࡹ࠯ࠤᘓ"))
      return bstack11lllll1111_opy_
  except Exception as e:
    logger.error(bstack11ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᘔ") + str(e))
    return False
def bstack1l1l111ll_opy_(driver, name, path):
  try:
    bstack1ll1ll11l11_opy_ = {
        bstack11ll111_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᘕ"): threading.current_thread().current_test_uuid,
        bstack11ll111_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᘖ"): os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᘗ"), bstack11ll111_opy_ (u"ࠧࠨᘘ")),
        bstack11ll111_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬᘙ"): os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᘚ"), bstack11ll111_opy_ (u"ࠪࠫᘛ"))
    }
    bstack1ll1l111ll1_opy_ = bstack1l1l11llll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1l11l1l1ll_opy_.value)
    logger.debug(bstack11ll111_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᘜ"))
    try:
      if (bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᘝ"), None) and bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᘞ"), None)):
        scripts = {bstack11ll111_opy_ (u"ࠧࡴࡥࡤࡲࠬᘟ"): bstack1l11ll111l_opy_.perform_scan}
        bstack11llll1l1ll_opy_ = json.loads(scripts[bstack11ll111_opy_ (u"ࠣࡵࡦࡥࡳࠨᘠ")].replace(bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᘡ"), bstack11ll111_opy_ (u"ࠥࠦᘢ")))
        bstack11llll1l1ll_opy_[bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᘣ")][bstack11ll111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᘤ")] = None
        scripts[bstack11ll111_opy_ (u"ࠨࡳࡤࡣࡱࠦᘥ")] = bstack11ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘦ") + json.dumps(bstack11llll1l1ll_opy_)
        bstack1l11ll111l_opy_.bstack11ll111l1l_opy_(scripts)
        bstack1l11ll111l_opy_.store()
        logger.debug(driver.execute_script(bstack1l11ll111l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11ll111l_opy_.perform_scan, {bstack11ll111_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᘧ"): name}))
      bstack1l1l11llll_opy_.end(EVENTS.bstack1l11l1l1ll_opy_.value, bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘨ"), bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘩ"), True, None)
    except Exception as error:
      bstack1l1l11llll_opy_.end(EVENTS.bstack1l11l1l1ll_opy_.value, bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᘪ"), bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᘫ"), False, str(error))
    bstack1ll1l111ll1_opy_ = bstack1l1l11llll_opy_.bstack11lll1lll1l_opy_(EVENTS.bstack1ll1l1ll111_opy_.value)
    bstack1l1l11llll_opy_.mark(bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᘬ"))
    try:
      if (bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᘭ"), None) and bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᘮ"), None)):
        scripts = {bstack11ll111_opy_ (u"ࠩࡶࡧࡦࡴࠧᘯ"): bstack1l11ll111l_opy_.perform_scan}
        bstack11llll1l1ll_opy_ = json.loads(scripts[bstack11ll111_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᘰ")].replace(bstack11ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᘱ"), bstack11ll111_opy_ (u"ࠧࠨᘲ")))
        bstack11llll1l1ll_opy_[bstack11ll111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᘳ")][bstack11ll111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧᘴ")] = None
        scripts[bstack11ll111_opy_ (u"ࠣࡵࡦࡥࡳࠨᘵ")] = bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᘶ") + json.dumps(bstack11llll1l1ll_opy_)
        bstack1l11ll111l_opy_.bstack11ll111l1l_opy_(scripts)
        bstack1l11ll111l_opy_.store()
        logger.debug(driver.execute_script(bstack1l11ll111l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11ll111l_opy_.bstack11llll111l1_opy_, bstack1ll1ll11l11_opy_))
      bstack1l1l11llll_opy_.end(bstack1ll1l111ll1_opy_, bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᘷ"), bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᘸ"),True, None)
    except Exception as error:
      bstack1l1l11llll_opy_.end(bstack1ll1l111ll1_opy_, bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᘹ"), bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᘺ"),False, str(error))
    logger.info(bstack11ll111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᘻ"))
  except Exception as bstack1ll11ll11l1_opy_:
    logger.error(bstack11ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᘼ") + str(path) + bstack11ll111_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᘽ") + str(bstack1ll11ll11l1_opy_))
def bstack11lll1ll1ll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᘾ")) and str(caps.get(bstack11ll111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᘿ"))).lower() == bstack11ll111_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨᙀ"):
        bstack11llll11l1l_opy_ = caps.get(bstack11ll111_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᙁ")) or caps.get(bstack11ll111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᙂ"))
        if bstack11llll11l1l_opy_ and int(str(bstack11llll11l1l_opy_)) < bstack11lll1l11ll_opy_:
            return False
    return True
def bstack1ll111l11l_opy_(config):
  if bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᙃ") in config:
        return config[bstack11ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᙄ")]
  for platform in config.get(bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᙅ"), []):
      if bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᙆ") in platform:
          return platform[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᙇ")]
  return None