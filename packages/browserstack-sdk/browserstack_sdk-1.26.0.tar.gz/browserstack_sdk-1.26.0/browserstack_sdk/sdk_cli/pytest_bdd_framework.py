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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack111111l11l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1l11l_opy_ import bstack1l11l1ll1l1_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lllll1l11l_opy_,
    bstack1llll1lllll_opy_,
    bstack1ll1lll1ll1_opy_,
    bstack1l11l1l11ll_opy_,
    bstack1lll1l11111_opy_,
)
import traceback
from bstack_utils.helper import bstack1ll111l1ll1_opy_
from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lllll1l1ll_opy_ import bstack1lll11ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l1l_opy_ import bstack1111l1111l_opy_
bstack1l1ll1lllll_opy_ = bstack1ll111l1ll1_opy_()
bstack1ll111l1111_opy_ = bstack11ll111_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣ፹")
bstack1l111l1l11l_opy_ = bstack11ll111_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧ፺")
bstack1l11l11llll_opy_ = bstack11ll111_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ፻")
bstack1l111lll111_opy_ = 1.0
_1ll111l1lll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l111l11l11_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦ፼")
    bstack1l11l11l1l1_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥ፽")
    bstack1l111l1111l_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧ፾")
    bstack1l11l1llll1_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤ፿")
    bstack1l11l1l1lll_opy_ = bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᎀ")
    bstack1l11l1l1l11_opy_: bool
    bstack1111l11l1l_opy_: bstack1111l1111l_opy_  = None
    bstack1l11l111ll1_opy_ = [
        bstack1lllll1l11l_opy_.BEFORE_ALL,
        bstack1lllll1l11l_opy_.AFTER_ALL,
        bstack1lllll1l11l_opy_.BEFORE_EACH,
        bstack1lllll1l11l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1ll1ll111ll_opy_: List[str]=[bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᎁ")],
        bstack1111l11l1l_opy_: bstack1111l1111l_opy_ = None,
        bstack1lll11111ll_opy_=None
    ):
        super().__init__(bstack1ll1ll111ll_opy_, bstack1l111lllll1_opy_, bstack1111l11l1l_opy_)
        self.bstack1l11l1l1l11_opy_ = any(bstack11ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᎂ") in item.lower() for item in bstack1ll1ll111ll_opy_)
        self.bstack1lll11111ll_opy_ = bstack1lll11111ll_opy_
    def track_event(
        self,
        context: bstack1l11l1l11ll_opy_,
        test_framework_state: bstack1lllll1l11l_opy_,
        test_hook_state: bstack1ll1lll1ll1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lllll1l11l_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l11l111ll1_opy_:
            bstack1l11l1ll1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lllll1l11l_opy_.NONE:
            self.logger.warning(bstack11ll111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᎃ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠧࠨᎄ"))
            return
        if not self.bstack1l11l1l1l11_opy_:
            self.logger.warning(bstack11ll111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᎅ") + str(str(self.bstack1ll1ll111ll_opy_)) + bstack11ll111_opy_ (u"ࠢࠣᎆ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11ll111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᎇ") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥᎈ"))
            return
        instance = self.__1l11l1lllll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᎉ") + str(args) + bstack11ll111_opy_ (u"ࠦࠧᎊ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l111ll1_opy_ and test_hook_state == bstack1ll1lll1ll1_opy_.PRE:
                bstack1ll1l111ll1_opy_ = bstack1llll11l1ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1l1ll111l_opy_.value)
                name = str(EVENTS.bstack1l1ll111l_opy_.name)+bstack11ll111_opy_ (u"ࠧࡀࠢᎋ")+str(test_framework_state.name)
                TestFramework.bstack1l111l1l111_opy_(instance, name, bstack1ll1l111ll1_opy_)
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᎌ").format(e))
        try:
            if test_framework_state == bstack1lllll1l11l_opy_.TEST:
                if not TestFramework.bstack11111l111l_opy_(instance, TestFramework.bstack1l11ll11lll_opy_) and test_hook_state == bstack1ll1lll1ll1_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11ll11l11_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᎍ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠣࠤᎎ"))
                if test_hook_state == bstack1ll1lll1ll1_opy_.PRE and not TestFramework.bstack11111l111l_opy_(instance, TestFramework.bstack1l1lll1l1ll_opy_):
                    TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1l1lll1l1ll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l111l11l1l_opy_(instance, args)
                    self.logger.debug(bstack11ll111_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᎏ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠥࠦ᎐"))
                elif test_hook_state == bstack1ll1lll1ll1_opy_.POST and not TestFramework.bstack11111l111l_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_):
                    TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ᎑") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠧࠨ᎒"))
            elif test_framework_state == bstack1lllll1l11l_opy_.STEP:
                if test_hook_state == bstack1ll1lll1ll1_opy_.PRE:
                    PytestBDDFramework.__1l11ll11111_opy_(instance, args)
                elif test_hook_state == bstack1ll1lll1ll1_opy_.POST:
                    PytestBDDFramework.__1l11l11lll1_opy_(instance, args)
            elif test_framework_state == bstack1lllll1l11l_opy_.LOG and test_hook_state == bstack1ll1lll1ll1_opy_.POST:
                PytestBDDFramework.__1l11l111lll_opy_(instance, *args)
            elif test_framework_state == bstack1lllll1l11l_opy_.LOG_REPORT and test_hook_state == bstack1ll1lll1ll1_opy_.POST:
                self.__1l11ll1111l_opy_(instance, *args)
                self.__1l11l111l1l_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l11l111ll1_opy_:
                self.__1l111ll1lll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢ᎓") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠢࠣ᎔"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111l1llll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l111ll1_opy_ and test_hook_state == bstack1ll1lll1ll1_opy_.POST:
                name = str(EVENTS.bstack1l1ll111l_opy_.name)+bstack11ll111_opy_ (u"ࠣ࠼ࠥ᎕")+str(test_framework_state.name)
                bstack1ll1l111ll1_opy_ = TestFramework.bstack1l11l11ll1l_opy_(instance, name)
                bstack1llll11l1ll_opy_.end(EVENTS.bstack1l1ll111l_opy_.value, bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᎖"), bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᎗"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ᎘").format(e))
    def bstack1ll1111lll1_opy_(self):
        return self.bstack1l11l1l1l11_opy_
    def __1l11l11l111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11ll111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤ᎙"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll1111l11l_opy_(rep, [bstack11ll111_opy_ (u"ࠨࡷࡩࡧࡱࠦ᎚"), bstack11ll111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣ᎛"), bstack11ll111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ᎜"), bstack11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ᎝"), bstack11ll111_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦ᎞"), bstack11ll111_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥ᎟")])
        return None
    def __1l11ll1111l_opy_(self, instance: bstack1llll1lllll_opy_, *args):
        result = self.__1l11l11l111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l1l11l_opy_ = None
        if result.get(bstack11ll111_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᎠ"), None) == bstack11ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᎡ") and len(args) > 1 and getattr(args[1], bstack11ll111_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᎢ"), None) is not None:
            failure = [{bstack11ll111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᎣ"): [args[1].excinfo.exconly(), result.get(bstack11ll111_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᎤ"), None)]}]
            bstack1111l1l11l_opy_ = bstack11ll111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᎥ") if bstack11ll111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᎦ") in getattr(args[1].excinfo, bstack11ll111_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᎧ"), bstack11ll111_opy_ (u"ࠨࠢᎨ")) else bstack11ll111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᎩ")
        bstack1l11ll11ll1_opy_ = result.get(bstack11ll111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᎪ"), TestFramework.bstack1l11l11l1ll_opy_)
        if bstack1l11ll11ll1_opy_ != TestFramework.bstack1l11l11l1ll_opy_:
            TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1ll11111l11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l111l1l1ll_opy_(instance, {
            TestFramework.bstack1l1l1ll11l1_opy_: failure,
            TestFramework.bstack1l11l11111l_opy_: bstack1111l1l11l_opy_,
            TestFramework.bstack1l1l1ll111l_opy_: bstack1l11ll11ll1_opy_,
        })
    def __1l11l1lllll_opy_(
        self,
        context: bstack1l11l1l11ll_opy_,
        test_framework_state: bstack1lllll1l11l_opy_,
        test_hook_state: bstack1ll1lll1ll1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lllll1l11l_opy_.SETUP_FIXTURE:
            instance = self.__1l11l1ll11l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11lll1111_opy_ bstack1l111ll1ll1_opy_ this to be bstack11ll111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᎫ")
            if test_framework_state == bstack1lllll1l11l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111lll11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lllll1l11l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11ll111_opy_ (u"ࠥࡲࡴࡪࡥࠣᎬ"), None), bstack11ll111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᎭ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11ll111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᎮ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11ll111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᎯ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack111111lll1_opy_(target) if target else None
        return instance
    def __1l111ll1lll_opy_(
        self,
        instance: bstack1llll1lllll_opy_,
        test_framework_state: bstack1lllll1l11l_opy_,
        test_hook_state: bstack1ll1lll1ll1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111ll1l11_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, PytestBDDFramework.bstack1l11l11l1l1_opy_, {})
        if not key in bstack1l111ll1l11_opy_:
            bstack1l111ll1l11_opy_[key] = []
        bstack1l111l111l1_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, PytestBDDFramework.bstack1l111l1111l_opy_, {})
        if not key in bstack1l111l111l1_opy_:
            bstack1l111l111l1_opy_[key] = []
        bstack1l111lll1l1_opy_ = {
            PytestBDDFramework.bstack1l11l11l1l1_opy_: bstack1l111ll1l11_opy_,
            PytestBDDFramework.bstack1l111l1111l_opy_: bstack1l111l111l1_opy_,
        }
        if test_hook_state == bstack1ll1lll1ll1_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11ll111_opy_ (u"ࠢ࡬ࡧࡼࠦᎰ"): key,
                TestFramework.bstack1l111l11lll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll111ll_opy_: TestFramework.bstack1l111l1ll11_opy_,
                TestFramework.bstack1l11l1l11l1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111ll1l1l_opy_: [],
                TestFramework.bstack1l11ll1lll1_opy_: hook_name,
                TestFramework.bstack1l111l111ll_opy_: bstack1lll11ll1ll_opy_.bstack1l11l11l11l_opy_()
            }
            bstack1l111ll1l11_opy_[key].append(hook)
            bstack1l111lll1l1_opy_[PytestBDDFramework.bstack1l11l1llll1_opy_] = key
        elif test_hook_state == bstack1ll1lll1ll1_opy_.POST:
            bstack1l111ll1111_opy_ = bstack1l111ll1l11_opy_.get(key, [])
            hook = bstack1l111ll1111_opy_.pop() if bstack1l111ll1111_opy_ else None
            if hook:
                result = self.__1l11l11l111_opy_(*args)
                if result:
                    bstack1l111lll1ll_opy_ = result.get(bstack11ll111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᎱ"), TestFramework.bstack1l111l1ll11_opy_)
                    if bstack1l111lll1ll_opy_ != TestFramework.bstack1l111l1ll11_opy_:
                        hook[TestFramework.bstack1l11ll111ll_opy_] = bstack1l111lll1ll_opy_
                hook[TestFramework.bstack1l111ll11l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l111ll_opy_] = bstack1lll11ll1ll_opy_.bstack1l11l11l11l_opy_()
                self.bstack1l11ll11l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1ll111_opy_, [])
                self.bstack1l1lll1l111_opy_(instance, logs)
                bstack1l111l111l1_opy_[key].append(hook)
                bstack1l111lll1l1_opy_[PytestBDDFramework.bstack1l11l1l1lll_opy_] = key
        TestFramework.bstack1l111l1l1ll_opy_(instance, bstack1l111lll1l1_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᎲ") + str(bstack1l111l111l1_opy_) + bstack11ll111_opy_ (u"ࠥࠦᎳ"))
    def __1l11l1ll11l_opy_(
        self,
        context: bstack1l11l1l11ll_opy_,
        test_framework_state: bstack1lllll1l11l_opy_,
        test_hook_state: bstack1ll1lll1ll1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll1111l11l_opy_(args[0], [bstack11ll111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᎴ"), bstack11ll111_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᎵ"), bstack11ll111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᎶ"), bstack11ll111_opy_ (u"ࠢࡪࡦࡶࠦᎷ"), bstack11ll111_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᎸ"), bstack11ll111_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᎹ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᎺ")) else fixturedef.get(bstack11ll111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᎻ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11ll111_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᎼ")) else None
        node = request.node if hasattr(request, bstack11ll111_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᎽ")) else None
        target = request.node.nodeid if hasattr(node, bstack11ll111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᎾ")) else None
        baseid = fixturedef.get(bstack11ll111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᎿ"), None) or bstack11ll111_opy_ (u"ࠤࠥᏀ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11ll111_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᏁ")):
            target = PytestBDDFramework.__1l111llll11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11ll111_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᏂ")) else None
            if target and not TestFramework.bstack111111lll1_opy_(target):
                self.__1l111lll11l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᏃ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠨࠢᏄ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11ll111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᏅ") + str(target) + bstack11ll111_opy_ (u"ࠣࠤᏆ"))
            return None
        instance = TestFramework.bstack111111lll1_opy_(target)
        if not instance:
            self.logger.warning(bstack11ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᏇ") + str(target) + bstack11ll111_opy_ (u"ࠥࠦᏈ"))
            return None
        bstack1l11ll1ll11_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, PytestBDDFramework.bstack1l111l11l11_opy_, {})
        if os.getenv(bstack11ll111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᏉ"), bstack11ll111_opy_ (u"ࠧ࠷ࠢᏊ")) == bstack11ll111_opy_ (u"ࠨ࠱ࠣᏋ"):
            bstack1l111l1lll1_opy_ = bstack11ll111_opy_ (u"ࠢ࠻ࠤᏌ").join((scope, fixturename))
            bstack1l111l11ll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111llll1l_opy_ = {
                bstack11ll111_opy_ (u"ࠣ࡭ࡨࡽࠧᏍ"): bstack1l111l1lll1_opy_,
                bstack11ll111_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᏎ"): PytestBDDFramework.__1l111l11111_opy_(request.node, scenario),
                bstack11ll111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᏏ"): fixturedef,
                bstack11ll111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᏐ"): scope,
                bstack11ll111_opy_ (u"ࠧࡺࡹࡱࡧࠥᏑ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lll1ll1_opy_.POST and callable(getattr(args[-1], bstack11ll111_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᏒ"), None)):
                    bstack1l111llll1l_opy_[bstack11ll111_opy_ (u"ࠢࡵࡻࡳࡩࠧᏓ")] = TestFramework.bstack1ll1111llll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lll1ll1_opy_.PRE:
                bstack1l111llll1l_opy_[bstack11ll111_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᏔ")] = uuid4().__str__()
                bstack1l111llll1l_opy_[PytestBDDFramework.bstack1l11l1l11l1_opy_] = bstack1l111l11ll1_opy_
            elif test_hook_state == bstack1ll1lll1ll1_opy_.POST:
                bstack1l111llll1l_opy_[PytestBDDFramework.bstack1l111ll11l1_opy_] = bstack1l111l11ll1_opy_
            if bstack1l111l1lll1_opy_ in bstack1l11ll1ll11_opy_:
                bstack1l11ll1ll11_opy_[bstack1l111l1lll1_opy_].update(bstack1l111llll1l_opy_)
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᏕ") + str(bstack1l11ll1ll11_opy_[bstack1l111l1lll1_opy_]) + bstack11ll111_opy_ (u"ࠥࠦᏖ"))
            else:
                bstack1l11ll1ll11_opy_[bstack1l111l1lll1_opy_] = bstack1l111llll1l_opy_
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᏗ") + str(len(bstack1l11ll1ll11_opy_)) + bstack11ll111_opy_ (u"ࠧࠨᏘ"))
        TestFramework.bstack111111ll11_opy_(instance, PytestBDDFramework.bstack1l111l11l11_opy_, bstack1l11ll1ll11_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᏙ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠢࠣᏚ"))
        return instance
    def __1l111lll11l_opy_(
        self,
        context: bstack1l11l1l11ll_opy_,
        test_framework_state: bstack1lllll1l11l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack111111l11l_opy_.create_context(target)
        ob = bstack1llll1lllll_opy_(ctx, self.bstack1ll1ll111ll_opy_, self.bstack1l111lllll1_opy_, test_framework_state)
        TestFramework.bstack1l111l1l1ll_opy_(ob, {
            TestFramework.bstack1ll1l1ll1l1_opy_: context.test_framework_name,
            TestFramework.bstack1ll1111ll1l_opy_: context.test_framework_version,
            TestFramework.bstack1l11ll1ll1l_opy_: [],
            PytestBDDFramework.bstack1l111l11l11_opy_: {},
            PytestBDDFramework.bstack1l111l1111l_opy_: {},
            PytestBDDFramework.bstack1l11l11l1l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111111ll11_opy_(ob, TestFramework.bstack1l111ll111l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111111ll11_opy_(ob, TestFramework.bstack1ll1l1l1l1l_opy_, context.platform_index)
        TestFramework.bstack11111111l1_opy_[ctx.id] = ob
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᏛ") + str(TestFramework.bstack11111111l1_opy_.keys()) + bstack11ll111_opy_ (u"ࠤࠥᏜ"))
        return ob
    @staticmethod
    def __1l111l11l1l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭Ꮭ"): id(step),
                bstack11ll111_opy_ (u"ࠫࡹ࡫ࡸࡵࠩᏞ"): step.name,
                bstack11ll111_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭Ꮯ"): step.keyword,
            })
        meta = {
            bstack11ll111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧᏠ"): {
                bstack11ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᏡ"): feature.name,
                bstack11ll111_opy_ (u"ࠨࡲࡤࡸ࡭࠭Ꮲ"): feature.filename,
                bstack11ll111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᏣ"): feature.description
            },
            bstack11ll111_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬᏤ"): {
                bstack11ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᏥ"): scenario.name
            },
            bstack11ll111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏦ"): steps,
            bstack11ll111_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨᏧ"): PytestBDDFramework.__1l11l1l1ll1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111l1ll1l_opy_: meta
            }
        )
    def bstack1l11ll11l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᏨ")
        global _1ll111l1lll_opy_
        platform_index = os.environ[bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᏩ")]
        bstack1l1lll1lll1_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1ll111l1111_opy_ + str(platform_index)), bstack1l111l1l11l_opy_)
        if not os.path.exists(bstack1l1lll1lll1_opy_) or not os.path.isdir(bstack1l1lll1lll1_opy_):
            return
        logs = hook.get(bstack11ll111_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᏪ"), [])
        with os.scandir(bstack1l1lll1lll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111l1lll_opy_:
                    self.logger.info(bstack11ll111_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᏫ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11ll111_opy_ (u"ࠦࠧᏬ")
                    log_entry = bstack1lll1l11111_opy_(
                        kind=bstack11ll111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᏭ"),
                        message=bstack11ll111_opy_ (u"ࠨࠢᏮ"),
                        level=bstack11ll111_opy_ (u"ࠢࠣᏯ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll11111_opy_=entry.stat().st_size,
                        bstack1ll1111111l_opy_=bstack11ll111_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᏰ"),
                        bstack1l1l1ll_opy_=os.path.abspath(entry.path),
                        bstack1l11ll1l11l_opy_=hook.get(TestFramework.bstack1l111l11lll_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111l1lll_opy_.add(abs_path)
        platform_index = os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᏱ")]
        bstack1l11l1lll1l_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1ll111l1111_opy_ + str(platform_index)), bstack1l111l1l11l_opy_, bstack1l11l11llll_opy_)
        if not os.path.exists(bstack1l11l1lll1l_opy_) or not os.path.isdir(bstack1l11l1lll1l_opy_):
            self.logger.info(bstack11ll111_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᏲ").format(bstack1l11l1lll1l_opy_))
        else:
            self.logger.info(bstack11ll111_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᏳ").format(bstack1l11l1lll1l_opy_))
            with os.scandir(bstack1l11l1lll1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111l1lll_opy_:
                        self.logger.info(bstack11ll111_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᏴ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11ll111_opy_ (u"ࠨࠢᏵ")
                        log_entry = bstack1lll1l11111_opy_(
                            kind=bstack11ll111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ᏶"),
                            message=bstack11ll111_opy_ (u"ࠣࠤ᏷"),
                            level=bstack11ll111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᏸ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll11111_opy_=entry.stat().st_size,
                            bstack1ll1111111l_opy_=bstack11ll111_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᏹ"),
                            bstack1l1l1ll_opy_=os.path.abspath(entry.path),
                            bstack1l1ll1l1l1l_opy_=hook.get(TestFramework.bstack1l111l11lll_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111l1lll_opy_.add(abs_path)
        hook[bstack11ll111_opy_ (u"ࠦࡱࡵࡧࡴࠤᏺ")] = logs
    def bstack1l1lll1l111_opy_(
        self,
        bstack1l1llll11ll_opy_: bstack1llll1lllll_opy_,
        entries: List[bstack1lll1l11111_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᏻ"))
        req.platform_index = TestFramework.bstack1llllll1lll_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1ll1l1l1l1l_opy_)
        req.execution_context.hash = str(bstack1l1llll11ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llll11ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llll11ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1lll_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1ll1l1ll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1lll_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1ll1111ll1l_opy_)
            log_entry.uuid = entry.bstack1l11ll1l11l_opy_
            log_entry.test_framework_state = bstack1l1llll11ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᏼ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11ll111_opy_ (u"ࠢࠣᏽ")
            if entry.kind == bstack11ll111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᏾"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll11111_opy_
                log_entry.file_path = entry.bstack1l1l1ll_opy_
        def bstack1l1lll111ll_opy_():
            bstack11ll1lll1l_opy_ = datetime.now()
            try:
                self.bstack1lll11111ll_opy_.LogCreatedEvent(req)
                bstack1l1llll11ll_opy_.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨ᏿"), datetime.now() - bstack11ll1lll1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤ᐀").format(str(e)))
                traceback.print_exc()
        self.bstack1111l11l1l_opy_.enqueue(bstack1l1lll111ll_opy_)
    def __1l11l111l1l_opy_(self, instance) -> None:
        bstack11ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᐁ")
        bstack1l111lll1l1_opy_ = {bstack11ll111_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᐂ"): bstack1lll11ll1ll_opy_.bstack1l11l11l11l_opy_()}
        TestFramework.bstack1l111l1l1ll_opy_(instance, bstack1l111lll1l1_opy_)
    @staticmethod
    def __1l11ll11111_opy_(instance, args):
        request, bstack1l11l1lll11_opy_ = args
        bstack1l11lll111l_opy_ = id(bstack1l11l1lll11_opy_)
        bstack1l111l1l1l1_opy_ = instance.data[TestFramework.bstack1l111l1ll1l_opy_]
        step = next(filter(lambda st: st[bstack11ll111_opy_ (u"࠭ࡩࡥࠩᐃ")] == bstack1l11lll111l_opy_, bstack1l111l1l1l1_opy_[bstack11ll111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐄ")]), None)
        step.update({
            bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᐅ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l111l1l1l1_opy_[bstack11ll111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐆ")]) if st[bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ᐇ")] == step[bstack11ll111_opy_ (u"ࠫ࡮ࡪࠧᐈ")]), None)
        if index is not None:
            bstack1l111l1l1l1_opy_[bstack11ll111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐉ")][index] = step
        instance.data[TestFramework.bstack1l111l1ll1l_opy_] = bstack1l111l1l1l1_opy_
    @staticmethod
    def __1l11l11lll1_opy_(instance, args):
        bstack11ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡭࡫࡮ࠡ࡮ࡨࡲࠥࡧࡲࡨࡵࠣ࡭ࡸࠦ࠲࠭ࠢ࡬ࡸࠥࡹࡩࡨࡰ࡬ࡪ࡮࡫ࡳࠡࡶ࡫ࡩࡷ࡫ࠠࡪࡵࠣࡲࡴࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠰ࠤࡠࡸࡥࡲࡷࡨࡷࡹ࠲ࠠࡴࡶࡨࡴࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠹ࠠࡵࡪࡨࡲࠥࡺࡨࡦࠢ࡯ࡥࡸࡺࠠࡷࡣ࡯ࡹࡪࠦࡩࡴࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᐊ")
        bstack1l11l1111l1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11l1lll11_opy_ = args[1]
        bstack1l11lll111l_opy_ = id(bstack1l11l1lll11_opy_)
        bstack1l111l1l1l1_opy_ = instance.data[TestFramework.bstack1l111l1ll1l_opy_]
        step = None
        if bstack1l11lll111l_opy_ is not None and bstack1l111l1l1l1_opy_.get(bstack11ll111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐋ")):
            step = next(filter(lambda st: st[bstack11ll111_opy_ (u"ࠨ࡫ࡧࠫᐌ")] == bstack1l11lll111l_opy_, bstack1l111l1l1l1_opy_[bstack11ll111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐍ")]), None)
            step.update({
                bstack11ll111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᐎ"): bstack1l11l1111l1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11ll111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᐏ"): bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᐐ"),
                bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᐑ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11ll111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᐒ"): bstack11ll111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᐓ"),
                })
        index = next((i for i, st in enumerate(bstack1l111l1l1l1_opy_[bstack11ll111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐔ")]) if st[bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ᐕ")] == step[bstack11ll111_opy_ (u"ࠫ࡮ࡪࠧᐖ")]), None)
        if index is not None:
            bstack1l111l1l1l1_opy_[bstack11ll111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐗ")][index] = step
        instance.data[TestFramework.bstack1l111l1ll1l_opy_] = bstack1l111l1l1l1_opy_
    @staticmethod
    def __1l11l1l1ll1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11ll111_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᐘ")):
                examples = list(node.callspec.params[bstack11ll111_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᐙ")].values())
            return examples
        except:
            return []
    def bstack1l1ll1ll1ll_opy_(self, instance: bstack1llll1lllll_opy_, bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_]):
        bstack1l111llllll_opy_ = (
            PytestBDDFramework.bstack1l11l1llll1_opy_
            if bstack11111ll1l1_opy_[1] == bstack1ll1lll1ll1_opy_.PRE
            else PytestBDDFramework.bstack1l11l1l1lll_opy_
        )
        hook = PytestBDDFramework.bstack1l11l1ll1ll_opy_(instance, bstack1l111llllll_opy_)
        entries = hook.get(TestFramework.bstack1l111ll1l1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_, []))
        return entries
    def bstack1l1ll1l1lll_opy_(self, instance: bstack1llll1lllll_opy_, bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_]):
        bstack1l111llllll_opy_ = (
            PytestBDDFramework.bstack1l11l1llll1_opy_
            if bstack11111ll1l1_opy_[1] == bstack1ll1lll1ll1_opy_.PRE
            else PytestBDDFramework.bstack1l11l1l1lll_opy_
        )
        PytestBDDFramework.bstack1l11l1l1111_opy_(instance, bstack1l111llllll_opy_)
        TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_, []).clear()
    @staticmethod
    def bstack1l11l1ll1ll_opy_(instance: bstack1llll1lllll_opy_, bstack1l111llllll_opy_: str):
        bstack1l11ll1l1l1_opy_ = (
            PytestBDDFramework.bstack1l111l1111l_opy_
            if bstack1l111llllll_opy_ == PytestBDDFramework.bstack1l11l1l1lll_opy_
            else PytestBDDFramework.bstack1l11l11l1l1_opy_
        )
        bstack1l11l111l11_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, bstack1l111llllll_opy_, None)
        bstack1l11l111111_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, bstack1l11ll1l1l1_opy_, None) if bstack1l11l111l11_opy_ else None
        return (
            bstack1l11l111111_opy_[bstack1l11l111l11_opy_][-1]
            if isinstance(bstack1l11l111111_opy_, dict) and len(bstack1l11l111111_opy_.get(bstack1l11l111l11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11l1l1111_opy_(instance: bstack1llll1lllll_opy_, bstack1l111llllll_opy_: str):
        hook = PytestBDDFramework.bstack1l11l1ll1ll_opy_(instance, bstack1l111llllll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111ll1l1l_opy_, []).clear()
    @staticmethod
    def __1l11l111lll_opy_(instance: bstack1llll1lllll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11ll111_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᐚ"), None)):
            return
        if os.getenv(bstack11ll111_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᐛ"), bstack11ll111_opy_ (u"ࠥ࠵ࠧᐜ")) != bstack11ll111_opy_ (u"ࠦ࠶ࠨᐝ"):
            PytestBDDFramework.logger.warning(bstack11ll111_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᐞ"))
            return
        bstack1l111ll11ll_opy_ = {
            bstack11ll111_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᐟ"): (PytestBDDFramework.bstack1l11l1llll1_opy_, PytestBDDFramework.bstack1l11l11l1l1_opy_),
            bstack11ll111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᐠ"): (PytestBDDFramework.bstack1l11l1l1lll_opy_, PytestBDDFramework.bstack1l111l1111l_opy_),
        }
        for when in (bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᐡ"), bstack11ll111_opy_ (u"ࠤࡦࡥࡱࡲࠢᐢ"), bstack11ll111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᐣ")):
            bstack1l11ll1l111_opy_ = args[1].get_records(when)
            if not bstack1l11ll1l111_opy_:
                continue
            records = [
                bstack1lll1l11111_opy_(
                    kind=TestFramework.bstack1l1lll1l11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11ll111_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᐤ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11ll111_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᐥ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll1l111_opy_
                if isinstance(getattr(r, bstack11ll111_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᐦ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l1l1l1l_opy_, bstack1l11ll1l1l1_opy_ = bstack1l111ll11ll_opy_.get(when, (None, None))
            bstack1l11ll1llll_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, bstack1l11l1l1l1l_opy_, None) if bstack1l11l1l1l1l_opy_ else None
            bstack1l11l111111_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, bstack1l11ll1l1l1_opy_, None) if bstack1l11ll1llll_opy_ else None
            if isinstance(bstack1l11l111111_opy_, dict) and len(bstack1l11l111111_opy_.get(bstack1l11ll1llll_opy_, [])) > 0:
                hook = bstack1l11l111111_opy_[bstack1l11ll1llll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l111ll1l1l_opy_ in hook:
                    hook[TestFramework.bstack1l111ll1l1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11ll11l11_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11llll1l11_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11l1l111l_opy_(request.node, scenario)
        bstack1l11l11ll11_opy_ = feature.filename
        if not bstack11llll1l11_opy_ or not test_name or not bstack1l11l11ll11_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1l11l1l1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll11lll_opy_: bstack11llll1l11_opy_,
            TestFramework.bstack1ll1l1111ll_opy_: test_name,
            TestFramework.bstack1l1ll1l1l11_opy_: bstack11llll1l11_opy_,
            TestFramework.bstack1l11ll111l1_opy_: bstack1l11l11ll11_opy_,
            TestFramework.bstack1l11l1111ll_opy_: PytestBDDFramework.__1l111l11111_opy_(feature, scenario),
            TestFramework.bstack1l11ll1l1ll_opy_: code,
            TestFramework.bstack1l1l1ll111l_opy_: TestFramework.bstack1l11l11l1ll_opy_,
            TestFramework.bstack1l1l1111ll1_opy_: test_name
        }
    @staticmethod
    def __1l11l1l111l_opy_(node, scenario):
        if hasattr(node, bstack11ll111_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᐧ")):
            parts = node.nodeid.rsplit(bstack11ll111_opy_ (u"ࠣ࡝ࠥᐨ"))
            params = parts[-1]
            return bstack11ll111_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᐩ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111l11111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11ll111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᐪ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11ll111_opy_ (u"ࠫࡹࡧࡧࡴࠩᐫ")) else [])
    @staticmethod
    def __1l111llll11_opy_(location):
        return bstack11ll111_opy_ (u"ࠧࡀ࠺ࠣᐬ").join(filter(lambda x: isinstance(x, str), location))