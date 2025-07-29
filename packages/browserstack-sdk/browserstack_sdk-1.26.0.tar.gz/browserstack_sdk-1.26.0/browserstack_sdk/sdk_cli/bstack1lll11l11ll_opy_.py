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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111l11l1l_opy_ import bstack1111l1111l_opy_
class bstack1lll1l1111l_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l11l1l_opy_: bstack1111l1111l_opy_
    def __init__(self):
        self.bstack1lll11111ll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l11l1l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll11l111l_opy_(self):
        return (self.bstack1lll11111ll_opy_ != None and self.bin_session_id != None and self.bstack1111l11l1l_opy_ != None)
    def configure(self, bstack1lll11111ll_opy_, config, bin_session_id: str, bstack1111l11l1l_opy_: bstack1111l1111l_opy_):
        self.bstack1lll11111ll_opy_ = bstack1lll11111ll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l11l1l_opy_ = bstack1111l11l1l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧࠤࡲࡵࡤࡶ࡮ࡨࠤࢀࡹࡥ࡭ࡨ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤ࠴࡟ࡠࡰࡤࡱࡪࡥ࡟ࡾ࠼ࠣࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧᆫ") + str(self.bin_session_id) + bstack11ll111_opy_ (u"ࠤࠥᆬ"))
    def bstack1ll11ll1ll1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11ll111_opy_ (u"ࠥࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡨࡧ࡮࡯ࡱࡷࠤࡧ࡫ࠠࡏࡱࡱࡩࠧᆭ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False