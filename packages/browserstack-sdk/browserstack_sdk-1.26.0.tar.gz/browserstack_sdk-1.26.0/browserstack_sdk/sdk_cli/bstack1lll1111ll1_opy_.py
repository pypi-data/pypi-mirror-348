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
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1llllll1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11l11lll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
class bstack1llll1111ll_opy_(bstack1lll1l1111l_opy_):
    bstack1l1l111lll1_opy_ = bstack11ll111_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣዃ")
    bstack1l1l111ll11_opy_ = bstack11ll111_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥዄ")
    bstack1l1l11ll111_opy_ = bstack11ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥዅ")
    def __init__(self, bstack1lll11lll11_opy_):
        super().__init__()
        bstack1llll1llll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack111111l1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1l1l1l11111_opy_)
        bstack1llll1llll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack11111ll1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll11l1l11l_opy_)
        bstack1llll1llll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack11111ll1ll_opy_, bstack1llllll1l1l_opy_.POST), self.bstack1l1l11l11ll_opy_)
        bstack1llll1llll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack11111ll1ll_opy_, bstack1llllll1l1l_opy_.POST), self.bstack1l1l111llll_opy_)
        bstack1llll1llll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.QUIT, bstack1llllll1l1l_opy_.POST), self.bstack1l1l111l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l11111_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨ዆"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11ll111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ዇")), str):
                    url = kwargs.get(bstack11ll111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤወ"))
                else:
                    url = kwargs.get(bstack11ll111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥዉ"))._client_config.remote_server_addr
            except Exception as e:
                url = bstack11ll111_opy_ (u"ࠨࠩዊ")
                self.logger.error(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢዋ").format(e))
            self.bstack1l1l11lllll_opy_(instance, url, f, kwargs)
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀ࡬࠮ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾ࠼ࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዌ") + str(kwargs) + bstack11ll111_opy_ (u"ࠦࠧው"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11l1l11l_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1llllll1lll_opy_(instance, bstack1llll1111ll_opy_.bstack1l1l111lll1_opy_, False):
            return
        if not f.bstack11111l111l_opy_(instance, bstack1llll1llll1_opy_.bstack1ll1l1l1l1l_opy_):
            return
        platform_index = f.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1ll1l1l1l1l_opy_)
        if f.bstack1ll1l1lllll_opy_(method_name, *args) and len(args) > 1:
            bstack11ll1lll1l_opy_ = datetime.now()
            hub_url = bstack1llll1llll1_opy_.hub_url(driver)
            self.logger.warning(bstack11ll111_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢዎ") + str(hub_url) + bstack11ll111_opy_ (u"ࠨࠢዏ"))
            bstack1l1l11l1l11_opy_ = args[1][bstack11ll111_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨዐ")] if isinstance(args[1], dict) and bstack11ll111_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢዑ") in args[1] else None
            bstack1l1l11l11l1_opy_ = bstack11ll111_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢዒ")
            if isinstance(bstack1l1l11l1l11_opy_, dict):
                bstack11ll1lll1l_opy_ = datetime.now()
                r = self.bstack1l1l11l111l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣዓ"), datetime.now() - bstack11ll1lll1l_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11ll111_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨዔ") + str(r) + bstack11ll111_opy_ (u"ࠧࠨዕ"))
                        return
                    if r.hub_url:
                        f.bstack1l1l1l111l1_opy_(instance, driver, r.hub_url)
                        f.bstack111111ll11_opy_(instance, bstack1llll1111ll_opy_.bstack1l1l111lll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧዖ"), e)
    def bstack1l1l11l11ll_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1llll1llll1_opy_.session_id(driver)
            if session_id:
                bstack1l1l111l11l_opy_ = bstack11ll111_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤ዗").format(session_id)
                bstack1llll11l1ll_opy_.mark(bstack1l1l111l11l_opy_)
    def bstack1l1l111llll_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllll1lll_opy_(instance, bstack1llll1111ll_opy_.bstack1l1l111ll11_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1llll1llll1_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧዘ") + str(hub_url) + bstack11ll111_opy_ (u"ࠤࠥዙ"))
            return
        framework_session_id = bstack1llll1llll1_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨዚ") + str(framework_session_id) + bstack11ll111_opy_ (u"ࠦࠧዛ"))
            return
        if bstack1llll1llll1_opy_.bstack1l1l11llll1_opy_(*args) == bstack1llll1llll1_opy_.bstack1l1l11l1ll1_opy_:
            bstack1l1l111l111_opy_ = bstack11ll111_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧዜ").format(framework_session_id)
            bstack1l1l111l11l_opy_ = bstack11ll111_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣዝ").format(framework_session_id)
            bstack1llll11l1ll_opy_.end(
                label=bstack11ll111_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥዞ"),
                start=bstack1l1l111l11l_opy_,
                end=bstack1l1l111l111_opy_,
                status=True,
                failure=None
            )
            bstack11ll1lll1l_opy_ = datetime.now()
            r = self.bstack1l1l11lll1l_opy_(
                ref,
                f.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1ll1l1l1l1l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢዟ"), datetime.now() - bstack11ll1lll1l_opy_)
            f.bstack111111ll11_opy_(instance, bstack1llll1111ll_opy_.bstack1l1l111ll11_opy_, r.success)
    def bstack1l1l111l1ll_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllll1lll_opy_(instance, bstack1llll1111ll_opy_.bstack1l1l11ll111_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1llll1llll1_opy_.session_id(driver)
        hub_url = bstack1llll1llll1_opy_.hub_url(driver)
        bstack11ll1lll1l_opy_ = datetime.now()
        r = self.bstack1l1l1111lll_opy_(
            ref,
            f.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1ll1l1l1l1l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢዠ"), datetime.now() - bstack11ll1lll1l_opy_)
        f.bstack111111ll11_opy_(instance, bstack1llll1111ll_opy_.bstack1l1l11ll111_opy_, r.success)
    @measure(event_name=EVENTS.bstack11ll11111l_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1l1l1ll1l1l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣዡ") + str(req) + bstack11ll111_opy_ (u"ࠦࠧዢ"))
        try:
            r = self.bstack1lll11111ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣዣ") + str(r.success) + bstack11ll111_opy_ (u"ࠨࠢዤ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧዥ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤዦ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11ll1ll_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1l1l11l111l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll11ll1ll1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack11ll111_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦዧ") + str(req) + bstack11ll111_opy_ (u"ࠥࠦየ"))
        try:
            r = self.bstack1lll11111ll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢዩ") + str(r.success) + bstack11ll111_opy_ (u"ࠧࠨዪ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦያ") + str(e) + bstack11ll111_opy_ (u"ࠢࠣዬ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11l1l1l_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1l1l11lll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11ll1ll1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵ࠼ࠣࠦይ") + str(req) + bstack11ll111_opy_ (u"ࠤࠥዮ"))
        try:
            r = self.bstack1lll11111ll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧዯ") + str(r) + bstack11ll111_opy_ (u"ࠦࠧደ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥዱ") + str(e) + bstack11ll111_opy_ (u"ࠨࠢዲ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11l1lll_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1l1l1111lll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11ll1ll1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11ll111_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤዳ") + str(req) + bstack11ll111_opy_ (u"ࠣࠤዴ"))
        try:
            r = self.bstack1lll11111ll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦድ") + str(r) + bstack11ll111_opy_ (u"ࠥࠦዶ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤዷ") + str(e) + bstack11ll111_opy_ (u"ࠧࠨዸ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l1l_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1l1l11lllll_opy_(self, instance: bstack1llllll1ll1_opy_, url: str, f: bstack1llll1llll1_opy_, kwargs):
        bstack1l1l1l1111l_opy_ = version.parse(f.framework_version)
        bstack1l1l111ll1l_opy_ = kwargs.get(bstack11ll111_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢዹ"))
        bstack1l1l11l1111_opy_ = kwargs.get(bstack11ll111_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢዺ"))
        bstack1l1l1llll1l_opy_ = {}
        bstack1l1l11ll11l_opy_ = {}
        bstack1l1l11ll1l1_opy_ = None
        bstack1l1l111l1l1_opy_ = {}
        if bstack1l1l11l1111_opy_ is not None or bstack1l1l111ll1l_opy_ is not None: # check top level caps
            if bstack1l1l11l1111_opy_ is not None:
                bstack1l1l111l1l1_opy_[bstack11ll111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨዻ")] = bstack1l1l11l1111_opy_
            if bstack1l1l111ll1l_opy_ is not None and callable(getattr(bstack1l1l111ll1l_opy_, bstack11ll111_opy_ (u"ࠤࡷࡳࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዼ"))):
                bstack1l1l111l1l1_opy_[bstack11ll111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࡣࡦࡹ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ዽ")] = bstack1l1l111ll1l_opy_.to_capabilities()
        response = self.bstack1l1l1ll1l1l_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l1l111l1l1_opy_).encode(bstack11ll111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥዾ")))
        if response is not None and response.capabilities:
            bstack1l1l1llll1l_opy_ = json.loads(response.capabilities.decode(bstack11ll111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦዿ")))
            if not bstack1l1l1llll1l_opy_: # empty caps bstack1l1ll1111l1_opy_ bstack1l1l1llll11_opy_ bstack1l1ll111l1l_opy_ bstack1lll1ll1l1l_opy_ or error in processing
                return
            bstack1l1l11ll1l1_opy_ = f.bstack1lll1lll111_opy_[bstack11ll111_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥጀ")](bstack1l1l1llll1l_opy_)
        if bstack1l1l111ll1l_opy_ is not None and bstack1l1l1l1111l_opy_ >= version.parse(bstack11ll111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ጁ")):
            bstack1l1l11ll11l_opy_ = None
        if (
                not bstack1l1l111ll1l_opy_ and not bstack1l1l11l1111_opy_
        ) or (
                bstack1l1l1l1111l_opy_ < version.parse(bstack11ll111_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧጂ"))
        ):
            bstack1l1l11ll11l_opy_ = {}
            bstack1l1l11ll11l_opy_.update(bstack1l1l1llll1l_opy_)
        self.logger.info(bstack11l11lll11_opy_)
        if os.environ.get(bstack11ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧጃ")).lower().__eq__(bstack11ll111_opy_ (u"ࠥࡸࡷࡻࡥࠣጄ")):
            kwargs.update(
                {
                    bstack11ll111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢጅ"): f.bstack1l1l11lll11_opy_,
                }
            )
        if bstack1l1l1l1111l_opy_ >= version.parse(bstack11ll111_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬጆ")):
            if bstack1l1l11l1111_opy_ is not None:
                del kwargs[bstack11ll111_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጇ")]
            kwargs.update(
                {
                    bstack11ll111_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣገ"): bstack1l1l11ll1l1_opy_,
                    bstack11ll111_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧጉ"): True,
                    bstack11ll111_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤጊ"): None,
                }
            )
        elif bstack1l1l1l1111l_opy_ >= version.parse(bstack11ll111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩጋ")):
            kwargs.update(
                {
                    bstack11ll111_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦጌ"): bstack1l1l11ll11l_opy_,
                    bstack11ll111_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨግ"): bstack1l1l11ll1l1_opy_,
                    bstack11ll111_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥጎ"): True,
                    bstack11ll111_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢጏ"): None,
                }
            )
        elif bstack1l1l1l1111l_opy_ >= version.parse(bstack11ll111_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨጐ")):
            kwargs.update(
                {
                    bstack11ll111_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ጑"): bstack1l1l11ll11l_opy_,
                    bstack11ll111_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢጒ"): True,
                    bstack11ll111_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦጓ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11ll111_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧጔ"): bstack1l1l11ll11l_opy_,
                    bstack11ll111_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥጕ"): True,
                    bstack11ll111_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢ጖"): None,
                }
            )