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
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack11111lll1l_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack111111l11l_opy_:
    bstack1l11111lll1_opy_ = bstack11ll111_opy_ (u"ࠧࡨࡥ࡯ࡥ࡫ࡱࡦࡸ࡫ࠣᔯ")
    context: bstack11111lll1l_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack11111lll1l_opy_):
        self.context = context
        self.data = dict({bstack111111l11l_opy_.bstack1l11111lll1_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᔰ"), bstack11ll111_opy_ (u"ࠧ࠱ࠩᔱ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1llllllll1l_opy_(self, target: object):
        return bstack111111l11l_opy_.create_context(target) == self.context
    def bstack1ll11l11111_opy_(self, context: bstack11111lll1l_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1l1lll1l1l_opy_(self, key: str, value: timedelta):
        self.data[bstack111111l11l_opy_.bstack1l11111lll1_opy_][key] += value
    def bstack1lll111l1l1_opy_(self) -> dict:
        return self.data[bstack111111l11l_opy_.bstack1l11111lll1_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack11111lll1l_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )