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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll11lllll_opy_, bstack11ll11l1lll_opy_
import tempfile
import json
bstack11l111l11l1_opy_ = os.getenv(bstack11ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡋࡤࡌࡉࡍࡇࠥᰐ"), None) or os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠧᰑ"))
bstack11l1111l1l1_opy_ = os.path.join(bstack11ll111_opy_ (u"ࠦࡱࡵࡧࠣᰒ"), bstack11ll111_opy_ (u"ࠬࡹࡤ࡬࠯ࡦࡰ࡮࠳ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩᰓ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11ll111_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩᰔ"),
      datefmt=bstack11ll111_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬᰕ"),
      stream=sys.stdout
    )
  return logger
def bstack1ll1lll11ll_opy_():
  bstack11l111l1111_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡅࡇࡅ࡙ࡌࠨᰖ"), bstack11ll111_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣᰗ"))
  return logging.DEBUG if bstack11l111l1111_opy_.lower() == bstack11ll111_opy_ (u"ࠥࡸࡷࡻࡥࠣᰘ") else logging.INFO
def bstack1l1ll1l1lll_opy_():
  global bstack11l111l11l1_opy_
  if os.path.exists(bstack11l111l11l1_opy_):
    os.remove(bstack11l111l11l1_opy_)
  if os.path.exists(bstack11l1111l1l1_opy_):
    os.remove(bstack11l1111l1l1_opy_)
def bstack1l11l1l1l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1lllllll1_opy_(config, log_level):
  bstack11l111llll1_opy_ = log_level
  if bstack11ll111_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᰙ") in config and config[bstack11ll111_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᰚ")] in bstack11ll11lllll_opy_:
    bstack11l111llll1_opy_ = bstack11ll11lllll_opy_[config[bstack11ll111_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᰛ")]]
  if config.get(bstack11ll111_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᰜ"), False):
    logging.getLogger().setLevel(bstack11l111llll1_opy_)
    return bstack11l111llll1_opy_
  global bstack11l111l11l1_opy_
  bstack1l11l1l1l1_opy_()
  bstack11l111ll11l_opy_ = logging.Formatter(
    fmt=bstack11ll111_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᰝ"),
    datefmt=bstack11ll111_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧᰞ"),
  )
  bstack11l111l1l11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111l11l1_opy_)
  file_handler.setFormatter(bstack11l111ll11l_opy_)
  bstack11l111l1l11_opy_.setFormatter(bstack11l111ll11l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l111l1l11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11ll111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬᰟ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l111l1l11_opy_.setLevel(bstack11l111llll1_opy_)
  logging.getLogger().addHandler(bstack11l111l1l11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l111llll1_opy_
def bstack11l111ll111_opy_(config):
  try:
    bstack11l111ll1l1_opy_ = set(bstack11ll11l1lll_opy_)
    bstack11l111ll1ll_opy_ = bstack11ll111_opy_ (u"ࠫࠬᰠ")
    with open(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᰡ")) as bstack11l1111ll1l_opy_:
      bstack11l1111llll_opy_ = bstack11l1111ll1l_opy_.read()
      bstack11l111ll1ll_opy_ = re.sub(bstack11ll111_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧᰢ"), bstack11ll111_opy_ (u"ࠧࠨᰣ"), bstack11l1111llll_opy_, flags=re.M)
      bstack11l111ll1ll_opy_ = re.sub(
        bstack11ll111_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫᰤ") + bstack11ll111_opy_ (u"ࠩࡿࠫᰥ").join(bstack11l111ll1l1_opy_) + bstack11ll111_opy_ (u"ࠪ࠭࠳࠰ࠤࠨᰦ"),
        bstack11ll111_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ᰧ"),
        bstack11l111ll1ll_opy_, flags=re.M | re.I
      )
    def bstack11l111l1l1l_opy_(dic):
      bstack11l111l1ll1_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l111ll1l1_opy_:
          bstack11l111l1ll1_opy_[key] = bstack11ll111_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩᰨ")
        else:
          if isinstance(value, dict):
            bstack11l111l1ll1_opy_[key] = bstack11l111l1l1l_opy_(value)
          else:
            bstack11l111l1ll1_opy_[key] = value
      return bstack11l111l1ll1_opy_
    bstack11l111l1ll1_opy_ = bstack11l111l1l1l_opy_(config)
    return {
      bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᰩ"): bstack11l111ll1ll_opy_,
      bstack11ll111_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᰪ"): json.dumps(bstack11l111l1ll1_opy_)
    }
  except Exception as e:
    return {}
def bstack11l1111l1ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠨ࡮ࡲ࡫ࠬᰫ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l111lll1l_opy_ = os.path.join(log_dir, bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵࠪᰬ"))
  if not os.path.exists(bstack11l111lll1l_opy_):
    bstack11l111lll11_opy_ = {
      bstack11ll111_opy_ (u"ࠥ࡭ࡳ࡯ࡰࡢࡶ࡫ࠦᰭ"): str(inipath),
      bstack11ll111_opy_ (u"ࠦࡷࡵ࡯ࡵࡲࡤࡸ࡭ࠨᰮ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫᰯ")), bstack11ll111_opy_ (u"࠭ࡷࠨᰰ")) as bstack11l1111l11l_opy_:
      bstack11l1111l11l_opy_.write(json.dumps(bstack11l111lll11_opy_))
def bstack11l1111ll11_opy_():
  try:
    bstack11l111lll1l_opy_ = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠧ࡭ࡱࡪࠫᰱ"), bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧᰲ"))
    if os.path.exists(bstack11l111lll1l_opy_):
      with open(bstack11l111lll1l_opy_, bstack11ll111_opy_ (u"ࠩࡵࠫᰳ")) as bstack11l1111l11l_opy_:
        bstack11l111l1lll_opy_ = json.load(bstack11l1111l11l_opy_)
      return bstack11l111l1lll_opy_.get(bstack11ll111_opy_ (u"ࠪ࡭ࡳ࡯ࡰࡢࡶ࡫ࠫᰴ"), bstack11ll111_opy_ (u"ࠫࠬᰵ")), bstack11l111l1lll_opy_.get(bstack11ll111_opy_ (u"ࠬࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠧᰶ"), bstack11ll111_opy_ (u"᰷࠭ࠧ"))
  except:
    pass
  return None, None
def bstack11l111lllll_opy_():
  try:
    bstack11l111lll1l_opy_ = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠧ࡭ࡱࡪࠫ᰸"), bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ᰹"))
    if os.path.exists(bstack11l111lll1l_opy_):
      os.remove(bstack11l111lll1l_opy_)
  except:
    pass
def bstack1l1ll1l111_opy_(config):
  from bstack_utils.helper import bstack11lll1l1l_opy_
  global bstack11l111l11l1_opy_
  try:
    if config.get(bstack11ll111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ᰺"), False):
      return
    uuid = os.getenv(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᰻")) if os.getenv(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᰼")) else bstack11lll1l1l_opy_.get_property(bstack11ll111_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢ᰽"))
    if not uuid or uuid == bstack11ll111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ᰾"):
      return
    bstack11l111l11ll_opy_ = [bstack11ll111_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪ᰿"), bstack11ll111_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩ᱀"), bstack11ll111_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪ᱁"), bstack11l111l11l1_opy_, bstack11l1111l1l1_opy_]
    bstack11l111l111l_opy_, root_path = bstack11l1111ll11_opy_()
    if bstack11l111l111l_opy_ != None:
      bstack11l111l11ll_opy_.append(bstack11l111l111l_opy_)
    if root_path != None:
      bstack11l111l11ll_opy_.append(os.path.join(root_path, bstack11ll111_opy_ (u"ࠪࡧࡴࡴࡦࡵࡧࡶࡸ࠳ࡶࡹࠨ᱂")))
    bstack1l11l1l1l1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪ᱃") + uuid + bstack11ll111_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭᱄"))
    with tarfile.open(output_file, bstack11ll111_opy_ (u"ࠨࡷ࠻ࡩࡽࠦ᱅")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l111l11ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l111ll111_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l1111lll1_opy_ = data.encode()
        tarinfo.size = len(bstack11l1111lll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l1111lll1_opy_))
    bstack11lll1111l_opy_ = MultipartEncoder(
      fields= {
        bstack11ll111_opy_ (u"ࠧࡥࡣࡷࡥࠬ᱆"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11ll111_opy_ (u"ࠨࡴࡥࠫ᱇")), bstack11ll111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧ᱈")),
        bstack11ll111_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᱉"): uuid
      }
    )
    response = requests.post(
      bstack11ll111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡻࡰ࡭ࡱࡤࡨ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡥ࡯࡭ࡪࡴࡴ࠮࡮ࡲ࡫ࡸ࠵ࡵࡱ࡮ࡲࡥࡩࠨ᱊"),
      data=bstack11lll1111l_opy_,
      headers={bstack11ll111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ᱋"): bstack11lll1111l_opy_.content_type},
      auth=(config[bstack11ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ᱌")], config[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᱍ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧᱎ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11ll111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨᱏ") + str(e))
  finally:
    try:
      bstack1l1ll1l1lll_opy_()
      bstack11l111lllll_opy_()
    except:
      pass