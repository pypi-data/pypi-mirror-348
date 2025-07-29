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
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack11l1llll_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1ll1ll1l_opy_:
    pass
class bstack1l111l11_opy_:
    bstack1l1ll1ll_opy_ = bstack11ll111_opy_ (u"ࠥࡦࡴࡵࡴࡴࡶࡵࡥࡵࠨჰ")
    CONNECT = bstack11ll111_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧჱ")
    bstack1ll1lll1ll_opy_ = bstack11ll111_opy_ (u"ࠧࡹࡨࡶࡶࡧࡳࡼࡴࠢჲ")
    CONFIG = bstack11ll111_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨჳ")
    bstack1ll1ll1l1l1_opy_ = bstack11ll111_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡶࠦჴ")
    bstack11lllll1l1_opy_ = bstack11ll111_opy_ (u"ࠣࡧࡻ࡭ࡹࠨჵ")
class bstack1ll1ll1l111_opy_:
    bstack1ll1ll1ll11_opy_ = bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡵࡷࡥࡷࡺࡥࡥࠤჶ")
    FINISHED = bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦჷ")
class bstack1ll1ll1lll1_opy_:
    bstack1ll1ll1ll11_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡳࡵࡣࡵࡸࡪࡪࠢჸ")
    FINISHED = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤჹ")
class bstack1ll1ll1l1ll_opy_:
    bstack1ll1ll1ll11_opy_ = bstack11ll111_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡵࡷࡥࡷࡺࡥࡥࠤჺ")
    FINISHED = bstack11ll111_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦ჻")
class bstack1ll1ll1llll_opy_:
    bstack1ll1ll1l11l_opy_ = bstack11ll111_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪࠢჼ")
class bstack1ll1ll1ll1l_opy_:
    _1lll11lllll_opy_ = None
    def __new__(cls):
        if not cls._1lll11lllll_opy_:
            cls._1lll11lllll_opy_ = super(bstack1ll1ll1ll1l_opy_, cls).__new__(cls)
        return cls._1lll11lllll_opy_
    def __init__(self):
        self._hooks = defaultdict(lambda: defaultdict(list))
        self._lock = Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def clear(self):
        with self._lock:
            self._hooks = defaultdict(list)
    def register(self, event_name, callback):
        with self._lock:
            if not callable(callback):
                raise ValueError(bstack11ll111_opy_ (u"ࠤࡆࡥࡱࡲࡢࡢࡥ࡮ࠤࡲࡻࡳࡵࠢࡥࡩࠥࡩࡡ࡭࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࠧჽ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡖࡪ࡭ࡩࡴࡶࡨࡶ࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࠦࠧࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡶࡩࡥࠢࠥჾ") + str(pid) + bstack11ll111_opy_ (u"ࠦࠧჿ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack11ll111_opy_ (u"ࠧࡔ࡯ࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦᄀ") + str(pid) + bstack11ll111_opy_ (u"ࠨࠢᄁ"))
                return
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡊࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࡰࡪࡴࠨࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠬࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࠣᄂ") + str(pid) + bstack11ll111_opy_ (u"ࠣࠤᄃ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack11ll111_opy_ (u"ࠤࡌࡲࡻࡵ࡫ࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧᄄ") + str(pid) + bstack11ll111_opy_ (u"ࠥࠦᄅ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࠣࠫࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠪࠤࡼ࡯ࡴࡩࠢࡳ࡭ࡩࠦࡻࡱ࡫ࡧࢁ࠿ࠦࠢᄆ") + str(e) + bstack11ll111_opy_ (u"ࠧࠨᄇ"))
                    traceback.print_exc()
bstack1l1lllll1_opy_ = bstack1ll1ll1ll1l_opy_()