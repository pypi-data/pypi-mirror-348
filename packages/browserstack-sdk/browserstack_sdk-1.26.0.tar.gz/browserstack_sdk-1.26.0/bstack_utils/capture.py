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
import builtins
import logging
class bstack111llll111_opy_:
    def __init__(self, handler):
        self._11ll1lllll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll111111_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11ll111_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᙵ"), bstack11ll111_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᙶ"), bstack11ll111_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬᙷ"), bstack11ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᙸ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll1111ll_opy_
        self._11ll1llllll_opy_()
    def _11lll1111ll_opy_(self, *args, **kwargs):
        self._11ll1lllll1_opy_(*args, **kwargs)
        message = bstack11ll111_opy_ (u"࠭ࠠࠨᙹ").join(map(str, args)) + bstack11ll111_opy_ (u"ࠧ࡝ࡰࠪᙺ")
        self._log_message(bstack11ll111_opy_ (u"ࠨࡋࡑࡊࡔ࠭ᙻ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11ll111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᙼ"): level, bstack11ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙽ"): msg})
    def _11ll1llllll_opy_(self):
        for level, bstack11lll1111l1_opy_ in self._11lll111111_opy_.items():
            setattr(logging, level, self._11lll11111l_opy_(level, bstack11lll1111l1_opy_))
    def _11lll11111l_opy_(self, level, bstack11lll1111l1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll1111l1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll1lllll1_opy_
        for level, bstack11lll1111l1_opy_ in self._11lll111111_opy_.items():
            setattr(logging, level, bstack11lll1111l1_opy_)