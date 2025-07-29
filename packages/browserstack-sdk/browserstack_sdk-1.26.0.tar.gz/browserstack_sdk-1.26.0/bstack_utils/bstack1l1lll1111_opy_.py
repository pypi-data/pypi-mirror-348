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
import re
from bstack_utils.bstack1l11lll1l_opy_ import bstack111l11lllll_opy_
def bstack111l11l1l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵨ")):
        return bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᵩ")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵪ")):
        return bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᵫ")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵬ")):
        return bstack11ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᵭ")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᵮ")):
        return bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᵯ")
def bstack111l11llll1_opy_(fixture_name):
    return bool(re.match(bstack11ll111_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᵰ"), fixture_name))
def bstack111l11ll111_opy_(fixture_name):
    return bool(re.match(bstack11ll111_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᵱ"), fixture_name))
def bstack111l11ll1ll_opy_(fixture_name):
    return bool(re.match(bstack11ll111_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᵲ"), fixture_name))
def bstack111l11lll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll111_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵳ")):
        return bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵴ"), bstack11ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᵵ")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵶ")):
        return bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᵷ"), bstack11ll111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᵸ")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵹ")):
        return bstack11ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᵺ"), bstack11ll111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᵻ")
    elif fixture_name.startswith(bstack11ll111_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵼ")):
        return bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᵽ"), bstack11ll111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᵾ")
    return None, None
def bstack111l11lll11_opy_(hook_name):
    if hook_name in [bstack11ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᵿ"), bstack11ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᶀ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1l111l1_opy_(hook_name):
    if hook_name in [bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᶁ"), bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᶂ")]:
        return bstack11ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᶃ")
    elif hook_name in [bstack11ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᶄ"), bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᶅ")]:
        return bstack11ll111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᶆ")
    elif hook_name in [bstack11ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᶇ"), bstack11ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᶈ")]:
        return bstack11ll111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᶉ")
    elif hook_name in [bstack11ll111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᶊ"), bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᶋ")]:
        return bstack11ll111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᶌ")
    return hook_name
def bstack111l11l1ll1_opy_(node, scenario):
    if hasattr(node, bstack11ll111_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᶍ")):
        parts = node.nodeid.rsplit(bstack11ll111_opy_ (u"ࠨ࡛ࠣᶎ"))
        params = parts[-1]
        return bstack11ll111_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᶏ").format(scenario.name, params)
    return scenario.name
def bstack111l1l1111l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11ll111_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᶐ")):
            examples = list(node.callspec.params[bstack11ll111_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᶑ")].values())
        return examples
    except:
        return []
def bstack111l11ll11l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l11ll1l1_opy_(report):
    try:
        status = bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᶒ")
        if report.passed or (report.failed and hasattr(report, bstack11ll111_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᶓ"))):
            status = bstack11ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᶔ")
        elif report.skipped:
            status = bstack11ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᶕ")
        bstack111l11lllll_opy_(status)
    except:
        pass
def bstack1l111lll1_opy_(status):
    try:
        bstack111l11l1lll_opy_ = bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᶖ")
        if status == bstack11ll111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᶗ"):
            bstack111l11l1lll_opy_ = bstack11ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᶘ")
        elif status == bstack11ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᶙ"):
            bstack111l11l1lll_opy_ = bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᶚ")
        bstack111l11lllll_opy_(bstack111l11l1lll_opy_)
    except:
        pass
def bstack111l1l11111_opy_(item=None, report=None, summary=None, extra=None):
    return