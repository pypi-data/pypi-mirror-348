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
logger = logging.getLogger(__name__)
bstack111l11l1111_opy_ = 1000
bstack111l11l11ll_opy_ = 2
class bstack111l11l11l1_opy_:
    def __init__(self, handler, bstack111l111l1ll_opy_=bstack111l11l1111_opy_, bstack111l111ll11_opy_=bstack111l11l11ll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111l111l1ll_opy_ = bstack111l111l1ll_opy_
        self.bstack111l111ll11_opy_ = bstack111l111ll11_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1111l11ll1_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack111l11l1l11_opy_()
    def bstack111l11l1l11_opy_(self):
        self.bstack1111l11ll1_opy_ = threading.Event()
        def bstack111l111lll1_opy_():
            self.bstack1111l11ll1_opy_.wait(self.bstack111l111ll11_opy_)
            if not self.bstack1111l11ll1_opy_.is_set():
                self.bstack111l11l111l_opy_()
        self.timer = threading.Thread(target=bstack111l111lll1_opy_, daemon=True)
        self.timer.start()
    def bstack111l111l1l1_opy_(self):
        try:
            if self.bstack1111l11ll1_opy_ and not self.bstack1111l11ll1_opy_.is_set():
                self.bstack1111l11ll1_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠬࡡࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࡴࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࠩᶛ") + (str(e) or bstack11ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡥࡲࡲࡻ࡫ࡲࡵࡧࡧࠤࡹࡵࠠࡴࡶࡵ࡭ࡳ࡭ࠢᶜ")))
        finally:
            self.timer = None
    def bstack111l111ll1l_opy_(self):
        if self.timer:
            self.bstack111l111l1l1_opy_()
        self.bstack111l11l1l11_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111l111l1ll_opy_:
                threading.Thread(target=self.bstack111l11l111l_opy_).start()
    def bstack111l11l111l_opy_(self, source = bstack11ll111_opy_ (u"ࠧࠨᶝ")):
        with self.lock:
            if not self.queue:
                self.bstack111l111ll1l_opy_()
                return
            data = self.queue[:self.bstack111l111l1ll_opy_]
            del self.queue[:self.bstack111l111l1ll_opy_]
        self.handler(data)
        if source != bstack11ll111_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪᶞ"):
            self.bstack111l111ll1l_opy_()
    def shutdown(self):
        self.bstack111l111l1l1_opy_()
        while self.queue:
            self.bstack111l11l111l_opy_(source=bstack11ll111_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫᶟ"))