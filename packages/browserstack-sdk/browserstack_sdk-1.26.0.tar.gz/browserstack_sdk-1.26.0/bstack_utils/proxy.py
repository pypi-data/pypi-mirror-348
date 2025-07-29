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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l11111lll_opy_
bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
def bstack111l1l11l11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1l11ll1_opy_(bstack111l1l1l11l_opy_, bstack111l1l111ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1l1l11l_opy_):
        with open(bstack111l1l1l11l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1l11l11_opy_(bstack111l1l1l11l_opy_):
        pac = get_pac(url=bstack111l1l1l11l_opy_)
    else:
        raise Exception(bstack11ll111_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧᵂ").format(bstack111l1l1l11l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11ll111_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤᵃ"), 80))
        bstack111l1l11l1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1l11l1l_opy_ = bstack11ll111_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪᵄ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1l111ll_opy_, bstack111l1l11l1l_opy_)
    return proxy_url
def bstack11l1l1ll1l_opy_(config):
    return bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᵅ") in config or bstack11ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᵆ") in config
def bstack111111lll_opy_(config):
    if not bstack11l1l1ll1l_opy_(config):
        return
    if config.get(bstack11ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᵇ")):
        return config.get(bstack11ll111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᵈ"))
    if config.get(bstack11ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᵉ")):
        return config.get(bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᵊ"))
def bstack111lllll1_opy_(config, bstack111l1l111ll_opy_):
    proxy = bstack111111lll_opy_(config)
    proxies = {}
    if config.get(bstack11ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᵋ")) or config.get(bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᵌ")):
        if proxy.endswith(bstack11ll111_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᵍ")):
            proxies = bstack111111l1_opy_(proxy, bstack111l1l111ll_opy_)
        else:
            proxies = {
                bstack11ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᵎ"): proxy
            }
    bstack11lll1l1l_opy_.bstack1l1lllll11_opy_(bstack11ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᵏ"), proxies)
    return proxies
def bstack111111l1_opy_(bstack111l1l1l11l_opy_, bstack111l1l111ll_opy_):
    proxies = {}
    global bstack111l1l11lll_opy_
    if bstack11ll111_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪᵐ") in globals():
        return bstack111l1l11lll_opy_
    try:
        proxy = bstack111l1l11ll1_opy_(bstack111l1l1l11l_opy_, bstack111l1l111ll_opy_)
        if bstack11ll111_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣᵑ") in proxy:
            proxies = {}
        elif bstack11ll111_opy_ (u"ࠤࡋࡘ࡙ࡖࠢᵒ") in proxy or bstack11ll111_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤᵓ") in proxy or bstack11ll111_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥᵔ") in proxy:
            bstack111l1l1l111_opy_ = proxy.split(bstack11ll111_opy_ (u"ࠧࠦࠢᵕ"))
            if bstack11ll111_opy_ (u"ࠨ࠺࠰࠱ࠥᵖ") in bstack11ll111_opy_ (u"ࠢࠣᵗ").join(bstack111l1l1l111_opy_[1:]):
                proxies = {
                    bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᵘ"): bstack11ll111_opy_ (u"ࠤࠥᵙ").join(bstack111l1l1l111_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᵚ"): str(bstack111l1l1l111_opy_[0]).lower() + bstack11ll111_opy_ (u"ࠦ࠿࠵࠯ࠣᵛ") + bstack11ll111_opy_ (u"ࠧࠨᵜ").join(bstack111l1l1l111_opy_[1:])
                }
        elif bstack11ll111_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧᵝ") in proxy:
            bstack111l1l1l111_opy_ = proxy.split(bstack11ll111_opy_ (u"ࠢࠡࠤᵞ"))
            if bstack11ll111_opy_ (u"ࠣ࠼࠲࠳ࠧᵟ") in bstack11ll111_opy_ (u"ࠤࠥᵠ").join(bstack111l1l1l111_opy_[1:]):
                proxies = {
                    bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᵡ"): bstack11ll111_opy_ (u"ࠦࠧᵢ").join(bstack111l1l1l111_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᵣ"): bstack11ll111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᵤ") + bstack11ll111_opy_ (u"ࠢࠣᵥ").join(bstack111l1l1l111_opy_[1:])
                }
        else:
            proxies = {
                bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᵦ"): proxy
            }
    except Exception as e:
        print(bstack11ll111_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᵧ"), bstack11l11111lll_opy_.format(bstack111l1l1l11l_opy_, str(e)))
    bstack111l1l11lll_opy_ = proxies
    return proxies