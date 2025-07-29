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
bstack11l1111111l_opy_ = {bstack11ll111_opy_ (u"ࠪࡶࡪࡺࡲࡺࡖࡨࡷࡹࡹࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠩᲝ")}
class bstack1l111111l_opy_:
    @staticmethod
    def bstack11ll11l1ll_opy_(config: dict) -> bool:
        bstack11l111111l1_opy_ = config.get(bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨᲞ"), {}).get(bstack11ll111_opy_ (u"ࠬࡸࡥࡵࡴࡼࡘࡪࡹࡴࡴࡑࡱࡊࡦ࡯࡬ࡶࡴࡨࠫᲟ"), {})
        return bstack11l111111l1_opy_.get(bstack11ll111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧᲠ"), False)
    @staticmethod
    def bstack11lll111_opy_(config: dict) -> int:
        bstack11l111111l1_opy_ = config.get(bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫᲡ"), {}).get(bstack11ll111_opy_ (u"ࠨࡴࡨࡸࡷࡿࡔࡦࡵࡷࡷࡔࡴࡆࡢ࡫࡯ࡹࡷ࡫ࠧᲢ"), {})
        retries = 0
        if bstack1l111111l_opy_.bstack11ll11l1ll_opy_(config):
            retries = bstack11l111111l1_opy_.get(bstack11ll111_opy_ (u"ࠩࡰࡥࡽࡘࡥࡵࡴ࡬ࡩࡸ࠭Უ"), 1)
        return retries
    @staticmethod
    def bstack11llll11l_opy_(config: dict) -> dict:
        bstack11l111111ll_opy_ = config.get(bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡱࡶ࡬ࡳࡳࡹࠧᲤ"), {})
        return {
            key: value for key, value in bstack11l111111ll_opy_.items() if key in bstack11l1111111l_opy_
        }