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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l111ll1l_opy_, bstack11ll111ll1_opy_
from bstack_utils.measure import measure
class bstack1l11l1llll_opy_:
  working_dir = os.getcwd()
  bstack11l1l1l11l_opy_ = False
  config = {}
  bstack11l1lll1l1l_opy_ = bstack11ll111_opy_ (u"ࠫࠬᲥ")
  binary_path = bstack11ll111_opy_ (u"ࠬ࠭Ღ")
  bstack111lll1l11l_opy_ = bstack11ll111_opy_ (u"࠭ࠧᲧ")
  bstack11l11llll_opy_ = False
  bstack111ll1111l1_opy_ = None
  bstack111ll11111l_opy_ = {}
  bstack111llllll11_opy_ = 300
  bstack111lll1l1l1_opy_ = False
  logger = None
  bstack111llll11l1_opy_ = False
  bstack1l1l1l11ll_opy_ = False
  percy_build_id = None
  bstack111lllllll1_opy_ = bstack11ll111_opy_ (u"ࠧࠨᲨ")
  bstack111ll11ll11_opy_ = {
    bstack11ll111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᲩ") : 1,
    bstack11ll111_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᲪ") : 2,
    bstack11ll111_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᲫ") : 3,
    bstack11ll111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᲬ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111lll11l1l_opy_(self):
    bstack111lllll111_opy_ = bstack11ll111_opy_ (u"ࠬ࠭Ჭ")
    bstack111ll11ll1l_opy_ = sys.platform
    bstack111lll1llll_opy_ = bstack11ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᲮ")
    if re.match(bstack11ll111_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢᲯ"), bstack111ll11ll1l_opy_) != None:
      bstack111lllll111_opy_ = bstack11ll1l1l1ll_opy_ + bstack11ll111_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤᲰ")
      self.bstack111lllllll1_opy_ = bstack11ll111_opy_ (u"ࠩࡰࡥࡨ࠭Ჱ")
    elif re.match(bstack11ll111_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣᲲ"), bstack111ll11ll1l_opy_) != None:
      bstack111lllll111_opy_ = bstack11ll1l1l1ll_opy_ + bstack11ll111_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧᲳ")
      bstack111lll1llll_opy_ = bstack11ll111_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣᲴ")
      self.bstack111lllllll1_opy_ = bstack11ll111_opy_ (u"࠭ࡷࡪࡰࠪᲵ")
    else:
      bstack111lllll111_opy_ = bstack11ll1l1l1ll_opy_ + bstack11ll111_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥᲶ")
      self.bstack111lllllll1_opy_ = bstack11ll111_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᲷ")
    return bstack111lllll111_opy_, bstack111lll1llll_opy_
  def bstack111ll111l1l_opy_(self):
    try:
      bstack111ll111lll_opy_ = [os.path.join(expanduser(bstack11ll111_opy_ (u"ࠤࢁࠦᲸ")), bstack11ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᲹ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111ll111lll_opy_:
        if(self.bstack111ll1ll1l1_opy_(path)):
          return path
      raise bstack11ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᲺ")
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢ᲻").format(e))
  def bstack111ll1ll1l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111ll1l1111_opy_(self, bstack111llll11ll_opy_):
    return os.path.join(bstack111llll11ll_opy_, self.bstack11l1lll1l1l_opy_ + bstack11ll111_opy_ (u"ࠨ࠮ࡦࡶࡤ࡫ࠧ᲼"))
  def bstack111llll1l11_opy_(self, bstack111llll11ll_opy_, bstack111ll1l1lll_opy_):
    if not bstack111ll1l1lll_opy_: return
    try:
      bstack111ll1l11ll_opy_ = self.bstack111ll1l1111_opy_(bstack111llll11ll_opy_)
      with open(bstack111ll1l11ll_opy_, bstack11ll111_opy_ (u"ࠢࡸࠤᲽ")) as f:
        f.write(bstack111ll1l1lll_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡕࡤࡺࡪࡪࠠ࡯ࡧࡺࠤࡊ࡚ࡡࡨࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠧᲾ"))
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡸ࡭࡫ࠠࡦࡶࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᲿ").format(e))
  def bstack111ll1l1ll1_opy_(self, bstack111llll11ll_opy_):
    try:
      bstack111ll1l11ll_opy_ = self.bstack111ll1l1111_opy_(bstack111llll11ll_opy_)
      if os.path.exists(bstack111ll1l11ll_opy_):
        with open(bstack111ll1l11ll_opy_, bstack11ll111_opy_ (u"ࠥࡶࠧ᳀")) as f:
          bstack111ll1l1lll_opy_ = f.read().strip()
          return bstack111ll1l1lll_opy_ if bstack111ll1l1lll_opy_ else None
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡋࡔࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ᳁").format(e))
  def bstack111lll11ll1_opy_(self, bstack111llll11ll_opy_, bstack111lllll111_opy_):
    bstack111lllll11l_opy_ = self.bstack111ll1l1ll1_opy_(bstack111llll11ll_opy_)
    if bstack111lllll11l_opy_:
      try:
        bstack111ll1lll11_opy_ = self.bstack111ll1111ll_opy_(bstack111lllll11l_opy_, bstack111lllll111_opy_)
        if not bstack111ll1lll11_opy_:
          self.logger.debug(bstack11ll111_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡹࠠࡶࡲࠣࡸࡴࠦࡤࡢࡶࡨࠤ࠭ࡋࡔࡢࡩࠣࡹࡳࡩࡨࡢࡰࡪࡩࡩ࠯ࠢ᳂"))
          return True
        self.logger.debug(bstack11ll111_opy_ (u"ࠨࡎࡦࡹࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷࡩࠧ᳃"))
        return False
      except Exception as e:
        self.logger.warn(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡳࡷࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨ᳄").format(e))
    return False
  def bstack111ll1111ll_opy_(self, bstack111lllll11l_opy_, bstack111lllll111_opy_):
    try:
      headers = {
        bstack11ll111_opy_ (u"ࠣࡋࡩ࠱ࡓࡵ࡮ࡦ࠯ࡐࡥࡹࡩࡨࠣ᳅"): bstack111lllll11l_opy_
      }
      response = bstack11ll111ll1_opy_(bstack11ll111_opy_ (u"ࠩࡊࡉ࡙࠭᳆"), bstack111lllll111_opy_, {}, {bstack11ll111_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ᳇"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠼ࠣࡿࢂࠨ᳈").format(e))
  @measure(event_name=EVENTS.bstack11ll1l1l11l_opy_, stage=STAGE.bstack111lllll_opy_)
  def bstack111ll11l111_opy_(self, bstack111lllll111_opy_, bstack111lll1llll_opy_):
    try:
      bstack111llll1ll1_opy_ = self.bstack111ll111l1l_opy_()
      bstack111ll111l11_opy_ = os.path.join(bstack111llll1ll1_opy_, bstack11ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨ᳉"))
      bstack111llllllll_opy_ = os.path.join(bstack111llll1ll1_opy_, bstack111lll1llll_opy_)
      if self.bstack111lll11ll1_opy_(bstack111llll1ll1_opy_, bstack111lllll111_opy_):
        if os.path.exists(bstack111llllllll_opy_):
          self.logger.info(bstack11ll111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣ᳊").format(bstack111llllllll_opy_))
          return bstack111llllllll_opy_
        if os.path.exists(bstack111ll111l11_opy_):
          self.logger.info(bstack11ll111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧ᳋").format(bstack111ll111l11_opy_))
          return self.bstack111lll11111_opy_(bstack111ll111l11_opy_, bstack111lll1llll_opy_)
      self.logger.info(bstack11ll111_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨ᳌").format(bstack111lllll111_opy_))
      response = bstack11ll111ll1_opy_(bstack11ll111_opy_ (u"ࠩࡊࡉ࡙࠭᳍"), bstack111lllll111_opy_, {}, {})
      if response.status_code == 200:
        bstack111lll1ll1l_opy_ = response.headers.get(bstack11ll111_opy_ (u"ࠥࡉ࡙ࡧࡧࠣ᳎"), bstack11ll111_opy_ (u"ࠦࠧ᳏"))
        if bstack111lll1ll1l_opy_:
          self.bstack111llll1l11_opy_(bstack111llll1ll1_opy_, bstack111lll1ll1l_opy_)
        with open(bstack111ll111l11_opy_, bstack11ll111_opy_ (u"ࠬࡽࡢࠨ᳐")) as file:
          file.write(response.content)
        self.logger.info(bstack11ll111_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࢀࠦ᳑").format(bstack111ll111l11_opy_))
        return self.bstack111lll11111_opy_(bstack111ll111l11_opy_, bstack111lll1llll_opy_)
      else:
        raise(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡿࠥ᳒").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤ᳓").format(e))
  def bstack111llll111l_opy_(self, bstack111lllll111_opy_, bstack111lll1llll_opy_):
    try:
      retry = 2
      bstack111llllllll_opy_ = None
      bstack111lll1l1ll_opy_ = False
      while retry > 0:
        bstack111llllllll_opy_ = self.bstack111ll11l111_opy_(bstack111lllll111_opy_, bstack111lll1llll_opy_)
        bstack111lll1l1ll_opy_ = self.bstack111ll1l111l_opy_(bstack111lllll111_opy_, bstack111lll1llll_opy_, bstack111llllllll_opy_)
        if bstack111lll1l1ll_opy_:
          break
        retry -= 1
      return bstack111llllllll_opy_, bstack111lll1l1ll_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨ᳔").format(e))
    return bstack111llllllll_opy_, False
  def bstack111ll1l111l_opy_(self, bstack111lllll111_opy_, bstack111lll1llll_opy_, bstack111llllllll_opy_, bstack111ll1lll1l_opy_ = 0):
    if bstack111ll1lll1l_opy_ > 1:
      return False
    if bstack111llllllll_opy_ == None or os.path.exists(bstack111llllllll_opy_) == False:
      self.logger.warn(bstack11ll111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤ᳕ࠣ"))
      return False
    bstack111llll1111_opy_ = bstack11ll111_opy_ (u"ࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࡜࠰ࡥ࡯࡭ࠥࡢࡤ࠯࡞ࡧ࠯࠳ࡢࡤࠬࠤ᳖")
    command = bstack11ll111_opy_ (u"ࠬࢁࡽࠡ࠯࠰ࡺࡪࡸࡳࡪࡱࡱ᳗ࠫ").format(bstack111llllllll_opy_)
    bstack111ll1l11l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111llll1111_opy_, bstack111ll1l11l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack11ll111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨ᳘ࠧ"))
      return False
  def bstack111lll11111_opy_(self, bstack111ll111l11_opy_, bstack111lll1llll_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll111l11_opy_)
      shutil.unpack_archive(bstack111ll111l11_opy_, working_dir)
      bstack111llllllll_opy_ = os.path.join(working_dir, bstack111lll1llll_opy_)
      os.chmod(bstack111llllllll_opy_, 0o755)
      return bstack111llllllll_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ᳙ࠣ"))
  def bstack111ll1ll11l_opy_(self):
    try:
      bstack111llll1lll_opy_ = self.config.get(bstack11ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ᳚"))
      bstack111ll1ll11l_opy_ = bstack111llll1lll_opy_ or (bstack111llll1lll_opy_ is None and self.bstack11l1l1l11l_opy_)
      if not bstack111ll1ll11l_opy_ or self.config.get(bstack11ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ᳛"), None) not in bstack11ll1l1ll1l_opy_:
        return False
      self.bstack11l11llll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁ᳜ࠧ").format(e))
  def bstack11l11111111_opy_(self):
    try:
      bstack11l11111111_opy_ = self.percy_capture_mode
      return bstack11l11111111_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁ᳝ࠧ").format(e))
  def init(self, bstack11l1l1l11l_opy_, config, logger):
    self.bstack11l1l1l11l_opy_ = bstack11l1l1l11l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111ll1ll11l_opy_():
      return
    self.bstack111ll11111l_opy_ = config.get(bstack11ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶ᳞ࠫ"), {})
    self.percy_capture_mode = config.get(bstack11ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦ᳟ࠩ"))
    try:
      bstack111lllll111_opy_, bstack111lll1llll_opy_ = self.bstack111lll11l1l_opy_()
      self.bstack11l1lll1l1l_opy_ = bstack111lll1llll_opy_
      bstack111llllllll_opy_, bstack111lll1l1ll_opy_ = self.bstack111llll111l_opy_(bstack111lllll111_opy_, bstack111lll1llll_opy_)
      if bstack111lll1l1ll_opy_:
        self.binary_path = bstack111llllllll_opy_
        thread = Thread(target=self.bstack111lllll1l1_opy_)
        thread.start()
      else:
        self.bstack111llll11l1_opy_ = True
        self.logger.error(bstack11ll111_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦ᳠").format(bstack111llllllll_opy_))
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ᳡").format(e))
  def bstack111ll11llll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11ll111_opy_ (u"ࠩ࡯ࡳ࡬᳢࠭"), bstack11ll111_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬᳣࠭"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11ll111_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽ᳤ࠣ").format(logfile))
      self.bstack111lll1l11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᳥").format(e))
  @measure(event_name=EVENTS.bstack11ll1ll111l_opy_, stage=STAGE.bstack111lllll_opy_)
  def bstack111lllll1l1_opy_(self):
    bstack111lll1111l_opy_ = self.bstack111lllll1ll_opy_()
    if bstack111lll1111l_opy_ == None:
      self.bstack111llll11l1_opy_ = True
      self.logger.error(bstack11ll111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤ᳦"))
      return False
    command_args = [bstack11ll111_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴ᳧ࠣ") if self.bstack11l1l1l11l_opy_ else bstack11ll111_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸ᳨ࠬ")]
    bstack11l111lll1l_opy_ = self.bstack111lll11l11_opy_()
    if bstack11l111lll1l_opy_ != None:
      command_args.append(bstack11ll111_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣᳩ").format(bstack11l111lll1l_opy_))
    env = os.environ.copy()
    env[bstack11ll111_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣᳪ")] = bstack111lll1111l_opy_
    env[bstack11ll111_opy_ (u"࡙ࠦࡎ࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠦᳫ")] = os.environ.get(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᳬ"), bstack11ll111_opy_ (u"᳭࠭ࠧ"))
    bstack111ll1lllll_opy_ = [self.binary_path]
    self.bstack111ll11llll_opy_()
    self.bstack111ll1111l1_opy_ = self.bstack111llll1l1l_opy_(bstack111ll1lllll_opy_ + command_args, env)
    self.logger.debug(bstack11ll111_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣᳮ"))
    bstack111ll1lll1l_opy_ = 0
    while self.bstack111ll1111l1_opy_.poll() == None:
      bstack111ll1ll1ll_opy_ = self.bstack111ll11l1l1_opy_()
      if bstack111ll1ll1ll_opy_:
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦᳯ"))
        self.bstack111lll1l1l1_opy_ = True
        return True
      bstack111ll1lll1l_opy_ += 1
      self.logger.debug(bstack11ll111_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧᳰ").format(bstack111ll1lll1l_opy_))
      time.sleep(2)
    self.logger.error(bstack11ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣᳱ").format(bstack111ll1lll1l_opy_))
    self.bstack111llll11l1_opy_ = True
    return False
  def bstack111ll11l1l1_opy_(self, bstack111ll1lll1l_opy_ = 0):
    if bstack111ll1lll1l_opy_ > 10:
      return False
    try:
      bstack111ll111ll1_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫᳲ"), bstack11ll111_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭ᳳ"))
      bstack111ll11l11l_opy_ = bstack111ll111ll1_opy_ + bstack11ll11l1l1l_opy_
      response = requests.get(bstack111ll11l11l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬ᳴"), {}).get(bstack11ll111_opy_ (u"ࠧࡪࡦࠪᳵ"), None)
      return True
    except:
      self.logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢ࡮ࡷ࡬ࠥࡩࡨࡦࡥ࡮ࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᳶ"))
      return False
  def bstack111lllll1ll_opy_(self):
    bstack111lll111ll_opy_ = bstack11ll111_opy_ (u"ࠩࡤࡴࡵ࠭᳷") if self.bstack11l1l1l11l_opy_ else bstack11ll111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᳸")
    bstack111lll1ll11_opy_ = bstack11ll111_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢ᳹") if self.config.get(bstack11ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᳺ")) is None else True
    bstack11l1l1ll1l1_opy_ = bstack11ll111_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠫࡶࡥࡳࡥࡼࡁࢀࢃࠢ᳻").format(self.config[bstack11ll111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᳼")], bstack111lll111ll_opy_, bstack111lll1ll11_opy_)
    if self.percy_capture_mode:
      bstack11l1l1ll1l1_opy_ += bstack11ll111_opy_ (u"ࠣࠨࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫࠽ࡼࡿࠥ᳽").format(self.percy_capture_mode)
    uri = bstack1l111ll1l_opy_(bstack11l1l1ll1l1_opy_)
    try:
      response = bstack11ll111ll1_opy_(bstack11ll111_opy_ (u"ࠩࡊࡉ࡙࠭᳾"), uri, {}, {bstack11ll111_opy_ (u"ࠪࡥࡺࡺࡨࠨ᳿"): (self.config[bstack11ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᴀ")], self.config[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᴁ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l11llll_opy_ = data.get(bstack11ll111_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᴂ"))
        self.percy_capture_mode = data.get(bstack11ll111_opy_ (u"ࠧࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࠬᴃ"))
        os.environ[bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ᴄ")] = str(self.bstack11l11llll_opy_)
        os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᴅ")] = str(self.percy_capture_mode)
        if bstack111lll1ll11_opy_ == bstack11ll111_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᴆ") and str(self.bstack11l11llll_opy_).lower() == bstack11ll111_opy_ (u"ࠦࡹࡸࡵࡦࠤᴇ"):
          self.bstack1l1l1l11ll_opy_ = True
        if bstack11ll111_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᴈ") in data:
          return data[bstack11ll111_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᴉ")]
        else:
          raise bstack11ll111_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧᴊ").format(data)
      else:
        raise bstack11ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣᴋ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥᴌ").format(e))
  def bstack111lll11l11_opy_(self):
    bstack111ll1l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨᴍ"))
    try:
      if bstack11ll111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᴎ") not in self.bstack111ll11111l_opy_:
        self.bstack111ll11111l_opy_[bstack11ll111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᴏ")] = 2
      with open(bstack111ll1l1l1l_opy_, bstack11ll111_opy_ (u"࠭ࡷࠨᴐ")) as fp:
        json.dump(self.bstack111ll11111l_opy_, fp)
      return bstack111ll1l1l1l_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᴑ").format(e))
  def bstack111llll1l1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111lllllll1_opy_ == bstack11ll111_opy_ (u"ࠨࡹ࡬ࡲࠬᴒ"):
        bstack111lll1lll1_opy_ = [bstack11ll111_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪᴓ"), bstack11ll111_opy_ (u"ࠪ࠳ࡨ࠭ᴔ")]
        cmd = bstack111lll1lll1_opy_ + cmd
      cmd = bstack11ll111_opy_ (u"ࠫࠥ࠭ᴕ").join(cmd)
      self.logger.debug(bstack11ll111_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤᴖ").format(cmd))
      with open(self.bstack111lll1l11l_opy_, bstack11ll111_opy_ (u"ࠨࡡࠣᴗ")) as bstack111lll11lll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111lll11lll_opy_, text=True, stderr=bstack111lll11lll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111llll11l1_opy_ = True
      self.logger.error(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᴘ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111lll1l1l1_opy_:
        self.logger.info(bstack11ll111_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤᴙ"))
        cmd = [self.binary_path, bstack11ll111_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧᴚ")]
        self.bstack111llll1l1l_opy_(cmd)
        self.bstack111lll1l1l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᴛ").format(cmd, e))
  def bstack1111l11l1_opy_(self):
    if not self.bstack11l11llll_opy_:
      return
    try:
      bstack111ll1l1l11_opy_ = 0
      while not self.bstack111lll1l1l1_opy_ and bstack111ll1l1l11_opy_ < self.bstack111llllll11_opy_:
        if self.bstack111llll11l1_opy_:
          self.logger.info(bstack11ll111_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤᴜ"))
          return
        time.sleep(1)
        bstack111ll1l1l11_opy_ += 1
      os.environ[bstack11ll111_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫᴝ")] = str(self.bstack111lll111l1_opy_())
      self.logger.info(bstack11ll111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠢᴞ"))
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᴟ").format(e))
  def bstack111lll111l1_opy_(self):
    if self.bstack11l1l1l11l_opy_:
      return
    try:
      bstack111lll1l111_opy_ = [platform[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᴠ")].lower() for platform in self.config.get(bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᴡ"), [])]
      bstack111ll11l1ll_opy_ = sys.maxsize
      bstack111llllll1l_opy_ = bstack11ll111_opy_ (u"ࠪࠫᴢ")
      for browser in bstack111lll1l111_opy_:
        if browser in self.bstack111ll11ll11_opy_:
          bstack111ll11lll1_opy_ = self.bstack111ll11ll11_opy_[browser]
        if bstack111ll11lll1_opy_ < bstack111ll11l1ll_opy_:
          bstack111ll11l1ll_opy_ = bstack111ll11lll1_opy_
          bstack111llllll1l_opy_ = browser
      return bstack111llllll1l_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᴣ").format(e))
  @classmethod
  def bstack11l1l111_opy_(self):
    return os.getenv(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪᴤ"), bstack11ll111_opy_ (u"࠭ࡆࡢ࡮ࡶࡩࠬᴥ")).lower()
  @classmethod
  def bstack1llllll1l1_opy_(self):
    return os.getenv(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫᴦ"), bstack11ll111_opy_ (u"ࠨࠩᴧ"))
  @classmethod
  def bstack1l1ll1l11ll_opy_(cls, value):
    cls.bstack1l1l1l11ll_opy_ = value
  @classmethod
  def bstack111ll1ll111_opy_(cls):
    return cls.bstack1l1l1l11ll_opy_
  @classmethod
  def bstack1l1ll11l11l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111ll1llll1_opy_(cls):
    return cls.percy_build_id