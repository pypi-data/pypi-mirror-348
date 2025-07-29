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
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1llllll1ll1_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lllll1lll1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11l11lll11_opy_
from bstack_utils.helper import bstack1l1ll1ll1l1_opy_
import threading
import os
import urllib.parse
class bstack1lll1111lll_opy_(bstack1lll1l1111l_opy_):
    def __init__(self, bstack1lll1l11ll1_opy_):
        super().__init__()
        bstack1lllll1lll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack111111l1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1ll11111l_opy_)
        bstack1lllll1lll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack111111l1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1lll11l_opy_)
        bstack1lllll1lll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack11111ll111_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1llllll_opy_)
        bstack1lllll1lll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack11111ll1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1ll1lll_opy_)
        bstack1lllll1lll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack111111l1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1lllll1_opy_)
        bstack1lllll1lll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.QUIT, bstack1llllll1l1l_opy_.PRE), self.on_close)
        self.bstack1lll1l11ll1_opy_ = bstack1lll1l11ll1_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll11111l_opy_(
        self,
        f: bstack1lllll1lll1_opy_,
        bstack1l1ll111111_opy_: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠦࡱࡧࡵ࡯ࡥ࡫ࠦ቏"):
            return
        if not bstack1l1ll1ll1l1_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡱࡧࡵ࡯ࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤቐ"))
            return
        def wrapped(bstack1l1ll111111_opy_, launch, *args, **kwargs):
            response = self.bstack1l1l1ll1l1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll111_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬቑ"): True}).encode(bstack11ll111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨቒ")))
            if response is not None and response.capabilities:
                if not bstack1l1ll1ll1l1_opy_():
                    browser = launch(bstack1l1ll111111_opy_)
                    return browser
                bstack1l1l1llll1l_opy_ = json.loads(response.capabilities.decode(bstack11ll111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቓ")))
                if not bstack1l1l1llll1l_opy_: # empty caps bstack1l1ll1111l1_opy_ bstack1l1l1llll11_opy_ bstack1l1ll111l1l_opy_ bstack1lll1ll1l1l_opy_ or error in processing
                    return
                bstack1l1ll111l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1llll1l_opy_))
                f.bstack111111ll11_opy_(instance, bstack1lllll1lll1_opy_.bstack1l1l1lll111_opy_, bstack1l1ll111l11_opy_)
                f.bstack111111ll11_opy_(instance, bstack1lllll1lll1_opy_.bstack1l1ll1111ll_opy_, bstack1l1l1llll1l_opy_)
                browser = bstack1l1ll111111_opy_.connect(bstack1l1ll111l11_opy_)
                return browser
        return wrapped
    def bstack1l1l1llllll_opy_(
        self,
        f: bstack1lllll1lll1_opy_,
        Connection: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠤࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠦቔ"):
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡧ࡭ࡸࡶࡡࡵࡥ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤቕ"))
            return
        if not bstack1l1ll1ll1l1_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11ll111_opy_ (u"ࠫࡵࡧࡲࡢ࡯ࡶࠫቖ"), {}).get(bstack11ll111_opy_ (u"ࠬࡨࡳࡑࡣࡵࡥࡲࡹࠧ቗")):
                    bstack1l1l1lll1l1_opy_ = args[0][bstack11ll111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨቘ")][bstack11ll111_opy_ (u"ࠢࡣࡵࡓࡥࡷࡧ࡭ࡴࠤ቙")]
                    session_id = bstack1l1l1lll1l1_opy_.get(bstack11ll111_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡋࡧࠦቚ"))
                    f.bstack111111ll11_opy_(instance, bstack1lllll1lll1_opy_.bstack1l1l1ll1ll1_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧቛ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l1lllll1_opy_(
        self,
        f: bstack1lllll1lll1_opy_,
        bstack1l1ll111111_opy_: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦቜ"):
            return
        if not bstack1l1ll1ll1l1_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤቝ"))
            return
        def wrapped(bstack1l1ll111111_opy_, connect, *args, **kwargs):
            response = self.bstack1l1l1ll1l1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack11ll111_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ቞"): True}).encode(bstack11ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ቟")))
            if response is not None and response.capabilities:
                bstack1l1l1llll1l_opy_ = json.loads(response.capabilities.decode(bstack11ll111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨበ")))
                if not bstack1l1l1llll1l_opy_:
                    return
                bstack1l1ll111l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1l1llll1l_opy_))
                if bstack1l1l1llll1l_opy_.get(bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧቡ")):
                    browser = bstack1l1ll111111_opy_.bstack1l1ll111ll1_opy_(bstack1l1ll111l11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1ll111l11_opy_
                    return connect(bstack1l1ll111111_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l1lll11l_opy_(
        self,
        f: bstack1lllll1lll1_opy_,
        bstack1ll111lll1l_opy_: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦቢ"):
            return
        if not bstack1l1ll1ll1l1_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡱࡩࡼࡥࡰࡢࡩࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤባ"))
            return
        def wrapped(bstack1ll111lll1l_opy_, bstack1l1l1lll1ll_opy_, *args, **kwargs):
            contexts = bstack1ll111lll1l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack11ll111_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤቤ") in page.url:
                                    return page
                    else:
                        return bstack1l1l1lll1ll_opy_(bstack1ll111lll1l_opy_)
        return wrapped
    def bstack1l1l1ll1l1l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11ll111_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥብ") + str(req) + bstack11ll111_opy_ (u"ࠨࠢቦ"))
        try:
            r = self.bstack1lll11111ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥቧ") + str(r.success) + bstack11ll111_opy_ (u"ࠣࠤቨ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢቩ") + str(e) + bstack11ll111_opy_ (u"ࠥࠦቪ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1ll1lll_opy_(
        self,
        f: bstack1lllll1lll1_opy_,
        Connection: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠦࡤࡹࡥ࡯ࡦࡢࡱࡪࡹࡳࡢࡩࡨࡣࡹࡵ࡟ࡴࡧࡵࡺࡪࡸࠢቫ"):
            return
        if not bstack1l1ll1ll1l1_opy_():
            return
        def wrapped(Connection, bstack1l1ll111lll_opy_, *args, **kwargs):
            return bstack1l1ll111lll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lllll1lll1_opy_,
        bstack1l1ll111111_opy_: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࠦቬ"):
            return
        if not bstack1l1ll1ll1l1_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡬ࡰࡵࡨࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤቭ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped