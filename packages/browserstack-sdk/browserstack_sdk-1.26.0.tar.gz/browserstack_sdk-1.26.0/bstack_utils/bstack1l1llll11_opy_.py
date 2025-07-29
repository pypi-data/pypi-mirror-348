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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll111l11_opy_ import bstack11lll11ll11_opy_
from bstack_utils.constants import *
import json
class bstack11l1l1l111_opy_:
    def __init__(self, bstack1l1l11111_opy_, bstack11lll11l1l1_opy_):
        self.bstack1l1l11111_opy_ = bstack1l1l11111_opy_
        self.bstack11lll11l1l1_opy_ = bstack11lll11l1l1_opy_
        self.bstack11lll111l1l_opy_ = None
    def __call__(self):
        bstack11lll111ll1_opy_ = {}
        while True:
            self.bstack11lll111l1l_opy_ = bstack11lll111ll1_opy_.get(
                bstack11ll111_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᙢ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll11l11l_opy_ = self.bstack11lll111l1l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll11l11l_opy_ > 0:
                sleep(bstack11lll11l11l_opy_ / 1000)
            params = {
                bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᙣ"): self.bstack1l1l11111_opy_,
                bstack11ll111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᙤ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll11l1ll_opy_ = bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᙥ") + bstack11lll111lll_opy_ + bstack11ll111_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᙦ")
            if self.bstack11lll11l1l1_opy_.lower() == bstack11ll111_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥᙧ"):
                bstack11lll111ll1_opy_ = bstack11lll11ll11_opy_.results(bstack11lll11l1ll_opy_, params)
            else:
                bstack11lll111ll1_opy_ = bstack11lll11ll11_opy_.bstack11lll11l111_opy_(bstack11lll11l1ll_opy_, params)
            if str(bstack11lll111ll1_opy_.get(bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᙨ"), bstack11ll111_opy_ (u"ࠫ࠷࠶࠰ࠨᙩ"))) != bstack11ll111_opy_ (u"ࠬ࠺࠰࠵ࠩᙪ"):
                break
        return bstack11lll111ll1_opy_.get(bstack11ll111_opy_ (u"࠭ࡤࡢࡶࡤࠫᙫ"), bstack11lll111ll1_opy_)