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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll11ll11_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l111l111_opy_ = urljoin(builder, bstack11ll111_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵࠪᶠ"))
        if params:
            bstack111l111l111_opy_ += bstack11ll111_opy_ (u"ࠦࡄࢁࡽࠣᶡ").format(urlencode({bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᶢ"): params.get(bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶣ"))}))
        return bstack11lll11ll11_opy_.bstack111l111l11l_opy_(bstack111l111l111_opy_)
    @staticmethod
    def bstack11lll11l111_opy_(builder,params=None):
        bstack111l111l111_opy_ = urljoin(builder, bstack11ll111_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨᶤ"))
        if params:
            bstack111l111l111_opy_ += bstack11ll111_opy_ (u"ࠣࡁࡾࢁࠧᶥ").format(urlencode({bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᶦ"): params.get(bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᶧ"))}))
        return bstack11lll11ll11_opy_.bstack111l111l11l_opy_(bstack111l111l111_opy_)
    @staticmethod
    def bstack111l111l11l_opy_(bstack111l1111ll1_opy_):
        bstack111l1111l1l_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᶨ"), os.environ.get(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᶩ"), bstack11ll111_opy_ (u"࠭ࠧᶪ")))
        headers = {bstack11ll111_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᶫ"): bstack11ll111_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᶬ").format(bstack111l1111l1l_opy_)}
        response = requests.get(bstack111l1111ll1_opy_, headers=headers)
        bstack111l1111lll_opy_ = {}
        try:
            bstack111l1111lll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣᶭ").format(e))
            pass
        if bstack111l1111lll_opy_ is not None:
            bstack111l1111lll_opy_[bstack11ll111_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫᶮ")] = response.headers.get(bstack11ll111_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᶯ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l1111lll_opy_[bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᶰ")] = response.status_code
        return bstack111l1111lll_opy_