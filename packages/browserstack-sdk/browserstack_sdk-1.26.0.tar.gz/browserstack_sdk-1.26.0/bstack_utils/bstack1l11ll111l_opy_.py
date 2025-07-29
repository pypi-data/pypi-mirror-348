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
from bstack_utils.bstack1l1l1ll11l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll11ll1l_opy_(object):
  bstack11l1l11l1l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"࠭ࡾࠨᙈ")), bstack11ll111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᙉ"))
  bstack11lll11llll_opy_ = os.path.join(bstack11l1l11l1l_opy_, bstack11ll111_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨᙊ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1ll1l11l_opy_ = None
  bstack11l11llll1_opy_ = None
  bstack11llll111l1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11ll111_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᙋ")):
      cls.instance = super(bstack11lll11ll1l_opy_, cls).__new__(cls)
      cls.instance.bstack11lll11lll1_opy_()
    return cls.instance
  def bstack11lll11lll1_opy_(self):
    try:
      with open(self.bstack11lll11llll_opy_, bstack11ll111_opy_ (u"ࠪࡶࠬᙌ")) as bstack11l11111_opy_:
        bstack11lll1l1111_opy_ = bstack11l11111_opy_.read()
        data = json.loads(bstack11lll1l1111_opy_)
        if bstack11ll111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᙍ") in data:
          self.bstack11lll1lll11_opy_(data[bstack11ll111_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᙎ")])
        if bstack11ll111_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᙏ") in data:
          self.bstack11ll111l1l_opy_(data[bstack11ll111_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᙐ")])
    except:
      pass
  def bstack11ll111l1l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11ll111_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᙑ"),bstack11ll111_opy_ (u"ࠩࠪᙒ"))
      self.bstack1ll1l11l_opy_ = scripts.get(bstack11ll111_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧᙓ"),bstack11ll111_opy_ (u"ࠫࠬᙔ"))
      self.bstack11l11llll1_opy_ = scripts.get(bstack11ll111_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩᙕ"),bstack11ll111_opy_ (u"࠭ࠧᙖ"))
      self.bstack11llll111l1_opy_ = scripts.get(bstack11ll111_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᙗ"),bstack11ll111_opy_ (u"ࠨࠩᙘ"))
  def bstack11lll1lll11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll11llll_opy_, bstack11ll111_opy_ (u"ࠩࡺࠫᙙ")) as file:
        json.dump({
          bstack11ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧᙚ"): self.commands_to_wrap,
          bstack11ll111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᙛ"): {
            bstack11ll111_opy_ (u"ࠧࡹࡣࡢࡰࠥᙜ"): self.perform_scan,
            bstack11ll111_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᙝ"): self.bstack1ll1l11l_opy_,
            bstack11ll111_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᙞ"): self.bstack11l11llll1_opy_,
            bstack11ll111_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᙟ"): self.bstack11llll111l1_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠢᙠ").format(e))
      pass
  def bstack1ll111l1ll_opy_(self, bstack1ll1l11l1ll_opy_):
    try:
      return any(command.get(bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨᙡ")) == bstack1ll1l11l1ll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l11ll111l_opy_ = bstack11lll11ll1l_opy_()