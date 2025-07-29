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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l1l1ll11l_opy_ import get_logger
logger = get_logger(__name__)
bstack111l1l1lll1_opy_: Dict[str, float] = {}
bstack111l1ll11ll_opy_: List = []
bstack111l1ll11l1_opy_ = 5
bstack1llll1l111_opy_ = os.path.join(os.getcwd(), bstack11ll111_opy_ (u"ࠪࡰࡴ࡭ࠧᴩ"), bstack11ll111_opy_ (u"ࠫࡰ࡫ࡹ࠮࡯ࡨࡸࡷ࡯ࡣࡴ࠰࡭ࡷࡴࡴࠧᴪ"))
logging.getLogger(bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠧᴫ")).setLevel(logging.WARNING)
lock = FileLock(bstack1llll1l111_opy_+bstack11ll111_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧᴬ"))
class bstack111l1l1llll_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1ll111l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1ll111l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11ll111_opy_ (u"ࠢ࡮ࡧࡤࡷࡺࡸࡥࠣᴭ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1llll11l1ll_opy_:
    global bstack111l1l1lll1_opy_
    @staticmethod
    def bstack1ll1l111111_opy_(key: str):
        bstack1ll1l111ll1_opy_ = bstack1llll11l1ll_opy_.bstack11lll1lll1l_opy_(key)
        bstack1llll11l1ll_opy_.mark(bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᴮ"))
        return bstack1ll1l111ll1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l1l1lll1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᴯ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1llll11l1ll_opy_.mark(end)
            bstack1llll11l1ll_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢᴰ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l1l1lll1_opy_ or end not in bstack111l1l1lll1_opy_:
                logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥࡱࡥࡺࠢࡺ࡭ࡹ࡮ࠠࡷࡣ࡯ࡹࡪࠦࡻࡾࠢࡲࡶࠥ࡫࡮ࡥࠢ࡮ࡩࡾࠦࡷࡪࡶ࡫ࠤࡻࡧ࡬ࡶࡧࠣࡿࢂࠨᴱ").format(start,end))
                return
            duration: float = bstack111l1l1lll1_opy_[end] - bstack111l1l1lll1_opy_[start]
            bstack111l1l1ll1l_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣᴲ"), bstack11ll111_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧᴳ")).lower() == bstack11ll111_opy_ (u"ࠢࡵࡴࡸࡩࠧᴴ")
            bstack111l1ll1111_opy_: bstack111l1l1llll_opy_ = bstack111l1l1llll_opy_(duration, label, bstack111l1l1lll1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᴵ"), 0), command, test_name, hook_type, bstack111l1l1ll1l_opy_)
            del bstack111l1l1lll1_opy_[start]
            del bstack111l1l1lll1_opy_[end]
            bstack1llll11l1ll_opy_.bstack111l1l1l1l1_opy_(bstack111l1ll1111_opy_)
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡧࡤࡷࡺࡸࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧᴶ").format(e))
    @staticmethod
    def bstack111l1l1l1l1_opy_(bstack111l1ll1111_opy_):
        os.makedirs(os.path.dirname(bstack1llll1l111_opy_)) if not os.path.exists(os.path.dirname(bstack1llll1l111_opy_)) else None
        bstack1llll11l1ll_opy_.bstack111l1l1l1ll_opy_()
        try:
            with lock:
                with open(bstack1llll1l111_opy_, bstack11ll111_opy_ (u"ࠥࡶ࠰ࠨᴷ"), encoding=bstack11ll111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᴸ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l1ll1111_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1l1ll11_opy_:
            logger.debug(bstack11ll111_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠦࡻࡾࠤᴹ").format(bstack111l1l1ll11_opy_))
            with lock:
                with open(bstack1llll1l111_opy_, bstack11ll111_opy_ (u"ࠨࡷࠣᴺ"), encoding=bstack11ll111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᴻ")) as file:
                    data = [bstack111l1ll1111_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡣࡳࡴࡪࡴࡤࠡࡽࢀࠦᴼ").format(str(e)))
        finally:
            if os.path.exists(bstack1llll1l111_opy_+bstack11ll111_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣᴽ")):
                os.remove(bstack1llll1l111_opy_+bstack11ll111_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤᴾ"))
    @staticmethod
    def bstack111l1l1l1ll_opy_():
        attempt = 0
        while (attempt < bstack111l1ll11l1_opy_):
            attempt += 1
            if os.path.exists(bstack1llll1l111_opy_+bstack11ll111_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᴿ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lll1lll1l_opy_(label: str) -> str:
        try:
            return bstack11ll111_opy_ (u"ࠧࢁࡽ࠻ࡽࢀࠦᵀ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᵁ").format(e))