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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack111111l1l_opy_():
  def __init__(self, args, logger, bstack1111lll111_opy_, bstack1111l1ll1l_opy_, bstack1111l1ll11_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111lll111_opy_ = bstack1111lll111_opy_
    self.bstack1111l1ll1l_opy_ = bstack1111l1ll1l_opy_
    self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
  def bstack1llll111ll_opy_(self, bstack1111ll1111_opy_, bstack1ll11lll1l_opy_, bstack1111l1l1ll_opy_=False):
    bstack1l111111ll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111lllll1_opy_ = manager.list()
    bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
    if bstack1111l1l1ll_opy_:
      for index, platform in enumerate(self.bstack1111lll111_opy_[bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪန")]):
        if index == 0:
          bstack1ll11lll1l_opy_[bstack11ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫပ")] = self.args
        bstack1l111111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1111_opy_,
                                                    args=(bstack1ll11lll1l_opy_, bstack1111lllll1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111lll111_opy_[bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬဖ")]):
        bstack1l111111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1111_opy_,
                                                    args=(bstack1ll11lll1l_opy_, bstack1111lllll1_opy_)))
    i = 0
    for t in bstack1l111111ll_opy_:
      try:
        if bstack11lll1l1l_opy_.get_property(bstack11ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫဗ")):
          os.environ[bstack11ll111_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬဘ")] = json.dumps(self.bstack1111lll111_opy_[bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨမ")][i % self.bstack1111l1ll11_opy_])
      except Exception as e:
        self.logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴ࠼ࠣࡿࢂࠨယ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l111111ll_opy_:
      t.join()
    return list(bstack1111lllll1_opy_)