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
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1llllll1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll1ll1ll_opy_(bstack1lll1l1111l_opy_):
    bstack1ll1l1llll1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1llll1llll1_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack11111ll1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll11l1l11l_opy_)
    def is_enabled(self) -> bool:
        return True
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
        hub_url = f.hub_url(driver)
        if f.bstack1ll11l1lll1_opy_(hub_url):
            if not bstack1llll1ll1ll_opy_.bstack1ll1l1llll1_opy_:
                self.logger.warning(bstack11ll111_opy_ (u"ࠤ࡯ࡳࡨࡧ࡬ࠡࡵࡨࡰ࡫࠳ࡨࡦࡣ࡯ࠤ࡫ࡲ࡯ࡸࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡪࡰࡩࡶࡦࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࠥᆉ") + str(hub_url) + bstack11ll111_opy_ (u"ࠥࠦᆊ"))
                bstack1llll1ll1ll_opy_.bstack1ll1l1llll1_opy_ = True
            return
        bstack1ll1l11l1ll_opy_ = f.bstack1ll1l1111l1_opy_(*args)
        bstack1ll11l11lll_opy_ = f.bstack1ll11l1l1l1_opy_(*args)
        if bstack1ll1l11l1ll_opy_ and bstack1ll1l11l1ll_opy_.lower() == bstack11ll111_opy_ (u"ࠦ࡫࡯࡮ࡥࡧ࡯ࡩࡲ࡫࡮ࡵࠤᆋ") and bstack1ll11l11lll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11l11lll_opy_.get(bstack11ll111_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦᆌ"), None), bstack1ll11l11lll_opy_.get(bstack11ll111_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᆍ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11ll111_opy_ (u"ࠢࡼࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࡽ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡺࡹࡩ࡯ࡩࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡴࡸࠠࡢࡴࡪࡷ࠳ࡼࡡ࡭ࡷࡨࡁࠧᆎ") + str(locator_value) + bstack11ll111_opy_ (u"ࠣࠤᆏ"))
                return
            def bstack1lllllllll1_opy_(driver, bstack1ll11l11ll1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11l11ll1_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11l1ll1l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11ll111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᆐ") + str(locator_value) + bstack11ll111_opy_ (u"ࠥࠦᆑ"))
                    else:
                        self.logger.warning(bstack11ll111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢᆒ") + str(response) + bstack11ll111_opy_ (u"ࠧࠨᆓ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11l1l111_opy_(
                        driver, bstack1ll11l11ll1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1lllllllll1_opy_.__name__ = bstack1ll1l11l1ll_opy_
            return bstack1lllllllll1_opy_
    def __1ll11l1l111_opy_(
        self,
        driver,
        bstack1ll11l11ll1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11l1ll1l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡶࡵ࡭࡬࡭ࡥࡳࡧࡧ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࠨᆔ") + str(locator_value) + bstack11ll111_opy_ (u"ࠢࠣᆕ"))
                bstack1ll11l1l1ll_opy_ = self.bstack1ll11l1ll11_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡨࡦࡣ࡯࡭ࡳ࡭࡟ࡳࡧࡶࡹࡱࡺ࠽ࠣᆖ") + str(bstack1ll11l1l1ll_opy_) + bstack11ll111_opy_ (u"ࠤࠥᆗ"))
                if bstack1ll11l1l1ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11ll111_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤᆘ"): bstack1ll11l1l1ll_opy_.locator_type,
                            bstack11ll111_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᆙ"): bstack1ll11l1l1ll_opy_.locator_value,
                        }
                    )
                    return bstack1ll11l11ll1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡏ࡟ࡅࡇࡅ࡙ࡌࠨᆚ"), False):
                    self.logger.info(bstack1ll1llll11l_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠮࡯࡬ࡷࡸ࡯࡮ࡨ࠼ࠣࡷࡱ࡫ࡥࡱࠪ࠶࠴࠮ࠦ࡬ࡦࡶࡷ࡭ࡳ࡭ࠠࡺࡱࡸࠤ࡮ࡴࡳࡱࡧࡦࡸࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠦ࡬ࡰࡩࡶࠦᆛ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡰࡲ࠱ࡸࡩࡲࡪࡲࡷ࠾ࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡴࡺࡲࡨࢁࠥࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࢃࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠿ࠥᆜ") + str(response) + bstack11ll111_opy_ (u"ࠣࠤᆝ"))
        except Exception as err:
            self.logger.warning(bstack11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰࡬ࡪࡧ࡬ࡪࡰࡪ࠱ࡷ࡫ࡳࡶ࡮ࡷ࠾ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨᆞ") + str(err) + bstack11ll111_opy_ (u"ࠥࠦᆟ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11l1llll_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1ll11l1ll1l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11ll111_opy_ (u"ࠦ࠵ࠨᆠ"),
    ):
        self.bstack1ll11ll1ll1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11ll111_opy_ (u"ࠧࠨᆡ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1lll11111ll_opy_.AISelfHealStep(req)
            self.logger.info(bstack11ll111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᆢ") + str(r) + bstack11ll111_opy_ (u"ࠢࠣᆣ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᆤ") + str(e) + bstack11ll111_opy_ (u"ࠤࠥᆥ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11ll1111_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1ll11l1ll11_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11ll111_opy_ (u"ࠥ࠴ࠧᆦ")):
        self.bstack1ll11ll1ll1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1lll11111ll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11ll111_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᆧ") + str(r) + bstack11ll111_opy_ (u"ࠧࠨᆨ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᆩ") + str(e) + bstack11ll111_opy_ (u"ࠢࠣᆪ"))
            traceback.print_exc()
            raise e