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
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1ll11ll1l_opy_ = {}
        bstack11l111l1ll_opy_ = os.environ.get(bstack11ll111_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧຮ"), bstack11ll111_opy_ (u"ࠧࠨຯ"))
        if not bstack11l111l1ll_opy_:
            return bstack1ll11ll1l_opy_
        try:
            bstack11l111l1l1_opy_ = json.loads(bstack11l111l1ll_opy_)
            if bstack11ll111_opy_ (u"ࠣࡱࡶࠦະ") in bstack11l111l1l1_opy_:
                bstack1ll11ll1l_opy_[bstack11ll111_opy_ (u"ࠤࡲࡷࠧັ")] = bstack11l111l1l1_opy_[bstack11ll111_opy_ (u"ࠥࡳࡸࠨາ")]
            if bstack11ll111_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣຳ") in bstack11l111l1l1_opy_ or bstack11ll111_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣິ") in bstack11l111l1l1_opy_:
                bstack1ll11ll1l_opy_[bstack11ll111_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤີ")] = bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦຶ"), bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦື")))
            if bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴຸࠥ") in bstack11l111l1l1_opy_ or bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥູࠣ") in bstack11l111l1l1_opy_:
                bstack1ll11ll1l_opy_[bstack11ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ຺")] = bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨົ"), bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦຼ")))
            if bstack11ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤຽ") in bstack11l111l1l1_opy_ or bstack11ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ຾") in bstack11l111l1l1_opy_:
                bstack1ll11ll1l_opy_[bstack11ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ຿")] = bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧເ"), bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧແ")))
            if bstack11ll111_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧໂ") in bstack11l111l1l1_opy_ or bstack11ll111_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥໃ") in bstack11l111l1l1_opy_:
                bstack1ll11ll1l_opy_[bstack11ll111_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦໄ")] = bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣ໅"), bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨໆ")))
            if bstack11ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ໇") in bstack11l111l1l1_opy_ or bstack11ll111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧ່ࠥ") in bstack11l111l1l1_opy_:
                bstack1ll11ll1l_opy_[bstack11ll111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨ້ࠦ")] = bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭໊ࠣ"), bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ໋")))
            if bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦ໌") in bstack11l111l1l1_opy_ or bstack11ll111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦໍ") in bstack11l111l1l1_opy_:
                bstack1ll11ll1l_opy_[bstack11ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ໎")] = bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ໏"), bstack11l111l1l1_opy_.get(bstack11ll111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ໐")))
            if bstack11ll111_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ໑") in bstack11l111l1l1_opy_:
                bstack1ll11ll1l_opy_[bstack11ll111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤ໒")] = bstack11l111l1l1_opy_[bstack11ll111_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ໓")]
        except Exception as error:
            logger.error(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡤࡸࡦࡀࠠࠣ໔") +  str(error))
        return bstack1ll11ll1l_opy_