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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l1l1ll11l_opy_ import get_logger
from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
bstack1l1l11llll_opy_ = bstack1llll11l1ll_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11l1l11ll1_opy_: Optional[str] = None):
    bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡈࡪࡩ࡯ࡳࡣࡷࡳࡷࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡴࡩࡧࠣࡷࡹࡧࡲࡵࠢࡷ࡭ࡲ࡫ࠠࡰࡨࠣࡥࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠍࠤࠥࠦࠠࡢ࡮ࡲࡲ࡬ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ᱐")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1l111ll1_opy_: str = bstack1l1l11llll_opy_.bstack11lll1lll1l_opy_(label)
            start_mark: str = label + bstack11ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᱑")
            end_mark: str = label + bstack11ll111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᱒")
            result = None
            try:
                if stage.value == STAGE.bstack11ll1ll1l_opy_.value:
                    bstack1l1l11llll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l1l11llll_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11l1l11ll1_opy_)
                elif stage.value == STAGE.bstack111lllll_opy_.value:
                    start_mark: str = bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᱓")
                    end_mark: str = bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᱔")
                    bstack1l1l11llll_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l1l11llll_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11l1l11ll1_opy_)
            except Exception as e:
                bstack1l1l11llll_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11l1l11ll1_opy_)
            return result
        return wrapper
    return decorator