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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l11l1ll_opy_, bstack1ll111111l_opy_, bstack1lll1ll1ll_opy_, bstack11ll11llll_opy_, \
    bstack11l1ll1ll1l_opy_
from bstack_utils.measure import measure
def bstack1ll1llll1_opy_(bstack1111lllllll_opy_):
    for driver in bstack1111lllllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l1lll1l_opy_, stage=STAGE.bstack111lllll_opy_)
def bstack1l1l1ll1l_opy_(driver, status, reason=bstack11ll111_opy_ (u"ࠨࠩᶳ")):
    bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
    if bstack11lll1l1l_opy_.bstack1111lll1ll_opy_():
        return
    bstack1ll1l1ll_opy_ = bstack111l1111_opy_(bstack11ll111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᶴ"), bstack11ll111_opy_ (u"ࠪࠫᶵ"), status, reason, bstack11ll111_opy_ (u"ࠫࠬᶶ"), bstack11ll111_opy_ (u"ࠬ࠭ᶷ"))
    driver.execute_script(bstack1ll1l1ll_opy_)
@measure(event_name=EVENTS.bstack1l1l1lll1l_opy_, stage=STAGE.bstack111lllll_opy_)
def bstack11111ll11_opy_(page, status, reason=bstack11ll111_opy_ (u"࠭ࠧᶸ")):
    try:
        if page is None:
            return
        bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
        if bstack11lll1l1l_opy_.bstack1111lll1ll_opy_():
            return
        bstack1ll1l1ll_opy_ = bstack111l1111_opy_(bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᶹ"), bstack11ll111_opy_ (u"ࠨࠩᶺ"), status, reason, bstack11ll111_opy_ (u"ࠩࠪᶻ"), bstack11ll111_opy_ (u"ࠪࠫᶼ"))
        page.evaluate(bstack11ll111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᶽ"), bstack1ll1l1ll_opy_)
    except Exception as e:
        print(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥᶾ"), e)
def bstack111l1111_opy_(type, name, status, reason, bstack11l1lll1_opy_, bstack1l1lll11ll_opy_):
    bstack1lll1ll11l_opy_ = {
        bstack11ll111_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ᶿ"): type,
        bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᷀"): {}
    }
    if type == bstack11ll111_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ᷁"):
        bstack1lll1ll11l_opy_[bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷ᷂ࠬ")][bstack11ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ᷃")] = bstack11l1lll1_opy_
        bstack1lll1ll11l_opy_[bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ᷄")][bstack11ll111_opy_ (u"ࠬࡪࡡࡵࡣࠪ᷅")] = json.dumps(str(bstack1l1lll11ll_opy_))
    if type == bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᷆"):
        bstack1lll1ll11l_opy_[bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᷇")][bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭᷈")] = name
    if type == bstack11ll111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ᷉"):
        bstack1lll1ll11l_opy_[bstack11ll111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ᷊࠭")][bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ᷋")] = status
        if status == bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᷌") and str(reason) != bstack11ll111_opy_ (u"ࠨࠢ᷍"):
            bstack1lll1ll11l_opy_[bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ᷎ࠪ")][bstack11ll111_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ᷏")] = json.dumps(str(reason))
    bstack11l1lllll1_opy_ = bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃ᷐ࠧ").format(json.dumps(bstack1lll1ll11l_opy_))
    return bstack11l1lllll1_opy_
def bstack1ll111lll1_opy_(url, config, logger, bstack11ll111l_opy_=False):
    hostname = bstack1ll111111l_opy_(url)
    is_private = bstack11ll11llll_opy_(hostname)
    try:
        if is_private or bstack11ll111l_opy_:
            file_path = bstack11l1l11l1ll_opy_(bstack11ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᷑"), bstack11ll111_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ᷒"), logger)
            if os.environ.get(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᷓ")) and eval(
                    os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᷔ"))):
                return
            if (bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᷕ") in config and not config[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᷖ")]):
                os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᷗ")] = str(True)
                bstack1111llllll1_opy_ = {bstack11ll111_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬᷘ"): hostname}
                bstack11l1ll1ll1l_opy_(bstack11ll111_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᷙ"), bstack11ll111_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪᷚ"), bstack1111llllll1_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1111l_opy_(caps, bstack1111lllll1l_opy_):
    if bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᷛ") in caps:
        caps[bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᷜ")][bstack11ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧᷝ")] = True
        if bstack1111lllll1l_opy_:
            caps[bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᷞ")][bstack11ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᷟ")] = bstack1111lllll1l_opy_
    else:
        caps[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᷠ")] = True
        if bstack1111lllll1l_opy_:
            caps[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᷡ")] = bstack1111lllll1l_opy_
def bstack111l11lllll_opy_(bstack111l1111ll_opy_):
    bstack111l1111111_opy_ = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᷢ"), bstack11ll111_opy_ (u"ࠧࠨᷣ"))
    if bstack111l1111111_opy_ == bstack11ll111_opy_ (u"ࠨࠩᷤ") or bstack111l1111111_opy_ == bstack11ll111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᷥ"):
        threading.current_thread().testStatus = bstack111l1111ll_opy_
    else:
        if bstack111l1111ll_opy_ == bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᷦ"):
            threading.current_thread().testStatus = bstack111l1111ll_opy_