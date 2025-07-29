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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack111111l11l_opy_, bstack11111lll1l_opy_
import os
import threading
class bstack1llllll1l1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11ll111_opy_ (u"ࠨࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧအ").format(self.name)
class bstack11111l1l1l_opy_(Enum):
    NONE = 0
    bstack111111l1ll_opy_ = 1
    bstack11111ll111_opy_ = 3
    bstack11111ll1ll_opy_ = 4
    bstack11111lll11_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11ll111_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢဢ").format(self.name)
class bstack1llllll1ll1_opy_(bstack111111l11l_opy_):
    framework_name: str
    framework_version: str
    state: bstack11111l1l1l_opy_
    previous_state: bstack11111l1l1l_opy_
    bstack11111l1ll1_opy_: datetime
    bstack1llllllll11_opy_: datetime
    def __init__(
        self,
        context: bstack11111lll1l_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack11111l1l1l_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack11111l1l1l_opy_.NONE
        self.bstack11111l1ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llllllll11_opy_ = datetime.now(tz=timezone.utc)
    def bstack111111ll11_opy_(self, bstack1111111l11_opy_: bstack11111l1l1l_opy_):
        bstack111111l1l1_opy_ = bstack11111l1l1l_opy_(bstack1111111l11_opy_).name
        if not bstack111111l1l1_opy_:
            return False
        if bstack1111111l11_opy_ == self.state:
            return False
        if self.state == bstack11111l1l1l_opy_.bstack11111ll111_opy_: # bstack111111ll1l_opy_ bstack111111l111_opy_ for bstack11111l1lll_opy_ in bstack1111l11111_opy_, it bstack1111111lll_opy_ bstack1111111ll1_opy_ bstack1lllllll1ll_opy_ times bstack111111llll_opy_ a new state
            return True
        if (
            bstack1111111l11_opy_ == bstack11111l1l1l_opy_.NONE
            or (self.state != bstack11111l1l1l_opy_.NONE and bstack1111111l11_opy_ == bstack11111l1l1l_opy_.bstack111111l1ll_opy_)
            or (self.state < bstack11111l1l1l_opy_.bstack111111l1ll_opy_ and bstack1111111l11_opy_ == bstack11111l1l1l_opy_.bstack11111ll1ll_opy_)
            or (self.state < bstack11111l1l1l_opy_.bstack111111l1ll_opy_ and bstack1111111l11_opy_ == bstack11111l1l1l_opy_.QUIT)
        ):
            raise ValueError(bstack11ll111_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢࡶࡸࡦࡺࡥࠡࡶࡵࡥࡳࡹࡩࡵ࡫ࡲࡲ࠿ࠦࠢဣ") + str(self.state) + bstack11ll111_opy_ (u"ࠤࠣࡁࡃࠦࠢဤ") + str(bstack1111111l11_opy_))
        self.previous_state = self.state
        self.state = bstack1111111l11_opy_
        self.bstack1llllllll11_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1lllllll11l_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack11111111l1_opy_: Dict[str, bstack1llllll1ll1_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack11111l11ll_opy_(self, instance: bstack1llllll1ll1_opy_, method_name: str, bstack1llllll11ll_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack11111111ll_opy_(
        self, method_name, previous_state: bstack11111l1l1l_opy_, *args, **kwargs
    ) -> bstack11111l1l1l_opy_:
        return
    @abc.abstractmethod
    def bstack11111lllll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack11111l1111_opy_(self, bstack11111llll1_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack11111llll1_opy_:
                bstack1111111111_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1111111111_opy_):
                    self.logger.warning(bstack11ll111_opy_ (u"ࠥࡹࡳࡶࡡࡵࡥ࡫ࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࠣဥ") + str(method_name) + bstack11ll111_opy_ (u"ࠦࠧဦ"))
                    continue
                bstack1lllllll111_opy_ = self.bstack11111111ll_opy_(
                    method_name, previous_state=bstack11111l1l1l_opy_.NONE
                )
                bstack1111111l1l_opy_ = self.bstack11111ll11l_opy_(
                    method_name,
                    (bstack1lllllll111_opy_ if bstack1lllllll111_opy_ else bstack11111l1l1l_opy_.NONE),
                    bstack1111111111_opy_,
                )
                if not callable(bstack1111111l1l_opy_):
                    self.logger.warning(bstack11ll111_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠥࡴ࡯ࡵࠢࡳࡥࡹࡩࡨࡦࡦ࠽ࠤࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࠭ࢁࡳࡦ࡮ࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࡀࠠࠣဧ") + str(self.framework_version) + bstack11ll111_opy_ (u"ࠨࠩࠣဨ"))
                    continue
                setattr(clazz, method_name, bstack1111111l1l_opy_)
    def bstack11111ll11l_opy_(
        self,
        method_name: str,
        bstack1lllllll111_opy_: bstack11111l1l1l_opy_,
        bstack1111111111_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack11ll1lll1l_opy_ = datetime.now()
            (bstack1lllllll111_opy_,) = wrapped.__vars__
            bstack1lllllll111_opy_ = (
                bstack1lllllll111_opy_
                if bstack1lllllll111_opy_ and bstack1lllllll111_opy_ != bstack11111l1l1l_opy_.NONE
                else self.bstack11111111ll_opy_(method_name, previous_state=bstack1lllllll111_opy_, *args, **kwargs)
            )
            if bstack1lllllll111_opy_ == bstack11111l1l1l_opy_.bstack111111l1ll_opy_:
                ctx = bstack111111l11l_opy_.create_context(self.bstack1llllllllll_opy_(target))
                if not self.bstack1llllll1l11_opy_() or ctx.id not in bstack1lllllll11l_opy_.bstack11111111l1_opy_:
                    bstack1lllllll11l_opy_.bstack11111111l1_opy_[ctx.id] = bstack1llllll1ll1_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1lllllll111_opy_
                    )
                self.logger.debug(bstack11ll111_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡥࡵࡩࡦࡺࡥࡥ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡩࡴࡹ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣဩ") + str(bstack1lllllll11l_opy_.bstack11111111l1_opy_.keys()) + bstack11ll111_opy_ (u"ࠣࠤဪ"))
            else:
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣ࡭ࡳࡼ࡯࡬ࡧࡧ࠾ࠥࢁࡴࡢࡴࡪࡩࡹ࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦါ") + str(bstack1lllllll11l_opy_.bstack11111111l1_opy_.keys()) + bstack11ll111_opy_ (u"ࠥࠦာ"))
            instance = bstack1lllllll11l_opy_.bstack111111lll1_opy_(self.bstack1llllllllll_opy_(target))
            if bstack1lllllll111_opy_ == bstack11111l1l1l_opy_.NONE or not instance:
                ctx = bstack111111l11l_opy_.create_context(self.bstack1llllllllll_opy_(target))
                self.logger.warning(bstack11ll111_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥࡻ࡮ࡵࡴࡤࡧࡰ࡫ࡤ࠻ࠢࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡥࡷࡼࡂࢁࡣࡵࡺࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣိ") + str(bstack1lllllll11l_opy_.bstack11111111l1_opy_.keys()) + bstack11ll111_opy_ (u"ࠧࠨီ"))
                return bstack1111111111_opy_(target, *args, **kwargs)
            bstack1lllllllll1_opy_ = self.bstack11111lllll_opy_(
                target,
                (instance, method_name),
                (bstack1lllllll111_opy_, bstack1llllll1l1l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack111111ll11_opy_(bstack1lllllll111_opy_):
                self.logger.debug(bstack11ll111_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡪࡪࠠࡴࡶࡤࡸࡪ࠳ࡴࡳࡣࡱࡷ࡮ࡺࡩࡰࡰ࠽ࠤࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡱࡴࡨࡺ࡮ࡵࡵࡴࡡࡶࡸࡦࡺࡥࡾࠢࡀࡂࠥࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡵࡷࡥࡹ࡫ࡽࠡࠪࡾࡸࡾࡶࡥࠩࡶࡤࡶ࡬࡫ࡴࠪࡿ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡿࡦࡸࡧࡴࡿࠬࠤࡠࠨု") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠢ࡞ࠤူ"))
            result = (
                bstack1lllllllll1_opy_(target, bstack1111111111_opy_, *args, **kwargs)
                if callable(bstack1lllllllll1_opy_)
                else bstack1111111111_opy_(target, *args, **kwargs)
            )
            bstack11111l11l1_opy_ = self.bstack11111lllll_opy_(
                target,
                (instance, method_name),
                (bstack1lllllll111_opy_, bstack1llllll1l1l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack11111l11ll_opy_(instance, method_name, datetime.now() - bstack11ll1lll1l_opy_, *args, **kwargs)
            return bstack11111l11l1_opy_ if bstack11111l11l1_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1lllllll111_opy_,)
        return wrapped
    @staticmethod
    def bstack111111lll1_opy_(target: object, strict=True):
        ctx = bstack111111l11l_opy_.create_context(target)
        instance = bstack1lllllll11l_opy_.bstack11111111l1_opy_.get(ctx.id, None)
        if instance and instance.bstack1llllllll1l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack111111111l_opy_(
        ctx: bstack11111lll1l_opy_, state: bstack11111l1l1l_opy_, reverse=True
    ) -> List[bstack1llllll1ll1_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1lllllll11l_opy_.bstack11111111l1_opy_.values(),
            ),
            key=lambda t: t.bstack11111l1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l111l_opy_(instance: bstack1llllll1ll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllll1lll_opy_(instance: bstack1llllll1ll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111111ll11_opy_(instance: bstack1llllll1ll1_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1lllllll11l_opy_.logger.debug(bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣ࡯ࡪࡿ࠽ࡼ࡭ࡨࡽࢂࠦࡶࡢ࡮ࡸࡩࡂࠨေ") + str(value) + bstack11ll111_opy_ (u"ࠤࠥဲ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1lllllll11l_opy_.bstack111111lll1_opy_(target, strict)
        return bstack1lllllll11l_opy_.bstack1llllll1lll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1lllllll11l_opy_.bstack111111lll1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1llllll1l11_opy_(self):
        return self.framework_name == bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧဳ")
    def bstack1llllllllll_opy_(self, target):
        return target if not self.bstack1llllll1l11_opy_() else self.bstack1llllll11l1_opy_()
    @staticmethod
    def bstack1llllll11l1_opy_():
        return str(os.getpid()) + str(threading.get_ident())