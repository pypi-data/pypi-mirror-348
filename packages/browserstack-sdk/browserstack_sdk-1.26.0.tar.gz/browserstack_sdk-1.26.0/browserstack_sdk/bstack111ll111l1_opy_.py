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
class RobotHandler():
    def __init__(self, args, logger, bstack1111lll111_opy_, bstack1111l1ll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111lll111_opy_ = bstack1111lll111_opy_
        self.bstack1111l1ll1l_opy_ = bstack1111l1ll1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111ll1lll1_opy_(bstack1111l1l1l1_opy_):
        bstack1111l11lll_opy_ = []
        if bstack1111l1l1l1_opy_:
            tokens = str(os.path.basename(bstack1111l1l1l1_opy_)).split(bstack11ll111_opy_ (u"ࠢࡠࠤရ"))
            camelcase_name = bstack11ll111_opy_ (u"ࠣࠢࠥလ").join(t.title() for t in tokens)
            suite_name, bstack1111l1l111_opy_ = os.path.splitext(camelcase_name)
            bstack1111l11lll_opy_.append(suite_name)
        return bstack1111l11lll_opy_
    @staticmethod
    def bstack1111l1l11l_opy_(typename):
        if bstack11ll111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧဝ") in typename:
            return bstack11ll111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦသ")
        return bstack11ll111_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧဟ")