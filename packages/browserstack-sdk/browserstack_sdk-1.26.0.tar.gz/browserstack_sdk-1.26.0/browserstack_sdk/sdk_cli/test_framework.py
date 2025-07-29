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
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l11l1l_opy_ import bstack1111l1111l_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack111111l11l_opy_, bstack11111lll1l_opy_
class bstack1ll1lll1ll1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11ll111_opy_ (u"ࠣࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᔁ").format(self.name)
class bstack1lllll1l11l_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11ll111_opy_ (u"ࠤࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᔂ").format(self.name)
class bstack1llll1lllll_opy_(bstack111111l11l_opy_):
    bstack1ll1ll111ll_opy_: List[str]
    bstack1l111lllll1_opy_: Dict[str, str]
    state: bstack1lllll1l11l_opy_
    bstack11111l1ll1_opy_: datetime
    bstack1llllllll11_opy_: datetime
    def __init__(
        self,
        context: bstack11111lll1l_opy_,
        bstack1ll1ll111ll_opy_: List[str],
        bstack1l111lllll1_opy_: Dict[str, str],
        state=bstack1lllll1l11l_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1ll111ll_opy_ = bstack1ll1ll111ll_opy_
        self.bstack1l111lllll1_opy_ = bstack1l111lllll1_opy_
        self.state = state
        self.bstack11111l1ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llllllll11_opy_ = datetime.now(tz=timezone.utc)
    def bstack111111ll11_opy_(self, bstack1111111l11_opy_: bstack1lllll1l11l_opy_):
        bstack111111l1l1_opy_ = bstack1lllll1l11l_opy_(bstack1111111l11_opy_).name
        if not bstack111111l1l1_opy_:
            return False
        if bstack1111111l11_opy_ == self.state:
            return False
        self.state = bstack1111111l11_opy_
        self.bstack1llllllll11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11l1l11ll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll1l11111_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1lll11111_opy_: int = None
    bstack1ll1111111l_opy_: str = None
    bstack1l1l1ll_opy_: str = None
    bstack1l1l11111_opy_: str = None
    bstack1l1ll1l1l1l_opy_: str = None
    bstack1l11ll1l11l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l11l1l1_opy_ = bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨᔃ")
    bstack1l11ll11lll_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᔄ")
    bstack1ll1l1111ll_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡲࡦࡳࡥࠣᔅ")
    bstack1l11ll111l1_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠢᔆ")
    bstack1l11l1111ll_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡺࡡࡨࡵࠥᔇ")
    bstack1l1l1ll111l_opy_ = bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࠨᔈ")
    bstack1ll11111l11_opy_ = bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺ࡟ࡢࡶࠥᔉ")
    bstack1l1lll1l1ll_opy_ = bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᔊ")
    bstack1ll1111l1l1_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᔋ")
    bstack1l111ll111l_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᔌ")
    bstack1ll1l1ll1l1_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠧᔍ")
    bstack1ll1111ll1l_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᔎ")
    bstack1l11ll1l1ll_opy_ = bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡣࡰࡦࡨࠦᔏ")
    bstack1l1ll1l1l11_opy_ = bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠦᔐ")
    bstack1ll1l1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᔑ")
    bstack1l1l1ll11l1_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࠥᔒ")
    bstack1l11l11111l_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠤᔓ")
    bstack1l11ll1ll1l_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡧࡴࠤᔔ")
    bstack1l111l1ll1l_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡳࡥࡵࡣࠥᔕ")
    bstack1l1111lll1l_opy_ = bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡳࡤࡱࡳࡩࡸ࠭ᔖ")
    bstack1l1l1111ll1_opy_ = bstack11ll111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᔗ")
    bstack1l11l1l11l1_opy_ = bstack11ll111_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᔘ")
    bstack1l111ll11l1_opy_ = bstack11ll111_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᔙ")
    bstack1l111l11lll_opy_ = bstack11ll111_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢ࡭ࡩࠨᔚ")
    bstack1l11ll111ll_opy_ = bstack11ll111_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷ࡫ࡳࡶ࡮ࡷࠦᔛ")
    bstack1l111ll1l1l_opy_ = bstack11ll111_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡲ࡯ࡨࡵࠥᔜ")
    bstack1l11ll1lll1_opy_ = bstack11ll111_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠦᔝ")
    bstack1l11l1ll111_opy_ = bstack11ll111_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᔞ")
    bstack1l111l111ll_opy_ = bstack11ll111_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᔟ")
    bstack1l11l11l1ll_opy_ = bstack11ll111_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᔠ")
    bstack1l111l1ll11_opy_ = bstack11ll111_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᔡ")
    bstack1ll111111l1_opy_ = bstack11ll111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠣᔢ")
    bstack1l1lll1l11l_opy_ = bstack11ll111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡒࡏࡈࠤᔣ")
    bstack1l1llll11l1_opy_ = bstack11ll111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᔤ")
    bstack11111111l1_opy_: Dict[str, bstack1llll1lllll_opy_] = dict()
    bstack1l1111l11l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1ll111ll_opy_: List[str]
    bstack1l111lllll1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1ll111ll_opy_: List[str],
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1111l11l1l_opy_: bstack1111l1111l_opy_
    ):
        self.bstack1ll1ll111ll_opy_ = bstack1ll1ll111ll_opy_
        self.bstack1l111lllll1_opy_ = bstack1l111lllll1_opy_
        self.bstack1111l11l1l_opy_ = bstack1111l11l1l_opy_
    def track_event(
        self,
        context: bstack1l11l1l11ll_opy_,
        test_framework_state: bstack1lllll1l11l_opy_,
        test_hook_state: bstack1ll1lll1ll1_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࢂࠨᔥ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111l1llll_opy_(
        self,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11lll11l1_opy_ = TestFramework.bstack1l11llll1l1_opy_(bstack11111ll1l1_opy_)
        if not bstack1l11lll11l1_opy_ in TestFramework.bstack1l1111l11l1_opy_:
            return
        self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࢁࡽࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠦᔦ").format(len(TestFramework.bstack1l1111l11l1_opy_[bstack1l11lll11l1_opy_])))
        for callback in TestFramework.bstack1l1111l11l1_opy_[bstack1l11lll11l1_opy_]:
            try:
                callback(self, instance, bstack11111ll1l1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11ll111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠦᔧ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1ll1111lll1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1ll1ll1ll_opy_(self, instance, bstack11111ll1l1_opy_):
        return
    @abc.abstractmethod
    def bstack1l1ll1l1lll_opy_(self, instance, bstack11111ll1l1_opy_):
        return
    @staticmethod
    def bstack111111lll1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack111111l11l_opy_.create_context(target)
        instance = TestFramework.bstack11111111l1_opy_.get(ctx.id, None)
        if instance and instance.bstack1llllllll1l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1lll1l1l1_opy_(reverse=True) -> List[bstack1llll1lllll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack11111111l1_opy_.values(),
            ),
            key=lambda t: t.bstack11111l1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111111111l_opy_(ctx: bstack11111lll1l_opy_, reverse=True) -> List[bstack1llll1lllll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack11111111l1_opy_.values(),
            ),
            key=lambda t: t.bstack11111l1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l111l_opy_(instance: bstack1llll1lllll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllll1lll_opy_(instance: bstack1llll1lllll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111111ll11_opy_(instance: bstack1llll1lllll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11ll111_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤᔨ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111l1l1ll_opy_(instance: bstack1llll1lllll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11ll111_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡲࡹࡸࡩࡦࡵࡀࡿࢂࠨᔩ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l11111llll_opy_(instance: bstack1lllll1l11l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11ll111_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᔪ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack111111lll1_opy_(target, strict)
        return TestFramework.bstack1llllll1lll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack111111lll1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111l1l111_opy_(instance: bstack1llll1lllll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11l11ll1l_opy_(instance: bstack1llll1lllll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11llll1l1_opy_(bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_]):
        return bstack11ll111_opy_ (u"ࠣ࠼ࠥᔫ").join((bstack1lllll1l11l_opy_(bstack11111ll1l1_opy_[0]).name, bstack1ll1lll1ll1_opy_(bstack11111ll1l1_opy_[1]).name))
    @staticmethod
    def bstack1ll11llll1l_opy_(bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_], callback: Callable):
        bstack1l11lll11l1_opy_ = TestFramework.bstack1l11llll1l1_opy_(bstack11111ll1l1_opy_)
        TestFramework.logger.debug(bstack11ll111_opy_ (u"ࠤࡶࡩࡹࡥࡨࡰࡱ࡮ࡣࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡩࡱࡲ࡯ࡤࡸࡥࡨ࡫ࡶࡸࡷࡿ࡟࡬ࡧࡼࡁࢀࢃࠢᔬ").format(bstack1l11lll11l1_opy_))
        if not bstack1l11lll11l1_opy_ in TestFramework.bstack1l1111l11l1_opy_:
            TestFramework.bstack1l1111l11l1_opy_[bstack1l11lll11l1_opy_] = []
        TestFramework.bstack1l1111l11l1_opy_[bstack1l11lll11l1_opy_].append(callback)
    @staticmethod
    def bstack1ll1111llll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡵ࡫ࡱࡷࠧᔭ"):
            return klass.__qualname__
        return module + bstack11ll111_opy_ (u"ࠦ࠳ࠨᔮ") + klass.__qualname__
    @staticmethod
    def bstack1ll1111l11l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}