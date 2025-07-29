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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lllll1l11l_opy_,
    bstack1llll1lllll_opy_,
    bstack1ll1lll1ll1_opy_,
    bstack1l11l1l11ll_opy_,
    bstack1lll1l11111_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1ll111l1ll1_opy_
from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l11l1l_opy_ import bstack1111l1111l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lllll1l1ll_opy_ import bstack1lll11ll1ll_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11ll11ll11_opy_
bstack1l1ll1lllll_opy_ = bstack1ll111l1ll1_opy_()
bstack1l111lll111_opy_ = 1.0
bstack1ll111l1111_opy_ = bstack11ll111_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᐭ")
bstack1l1111llll1_opy_ = bstack11ll111_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᐮ")
bstack1l1111lll11_opy_ = bstack11ll111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᐯ")
bstack1l1111ll1ll_opy_ = bstack11ll111_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᐰ")
bstack1l1111lllll_opy_ = bstack11ll111_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᐱ")
_1ll111l1lll_opy_ = set()
class bstack1llll1l1ll1_opy_(TestFramework):
    bstack1l111l11l11_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᐲ")
    bstack1l11l11l1l1_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᐳ")
    bstack1l111l1111l_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᐴ")
    bstack1l11l1llll1_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᐵ")
    bstack1l11l1l1lll_opy_ = bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᐶ")
    bstack1l11l1l1l11_opy_: bool
    bstack1111l11l1l_opy_: bstack1111l1111l_opy_  = None
    bstack1lll11111ll_opy_ = None
    bstack1l11l111ll1_opy_ = [
        bstack1lllll1l11l_opy_.BEFORE_ALL,
        bstack1lllll1l11l_opy_.AFTER_ALL,
        bstack1lllll1l11l_opy_.BEFORE_EACH,
        bstack1lllll1l11l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1ll1ll111ll_opy_: List[str]=[bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᐷ")],
        bstack1111l11l1l_opy_: bstack1111l1111l_opy_=None,
        bstack1lll11111ll_opy_=None
    ):
        super().__init__(bstack1ll1ll111ll_opy_, bstack1l111lllll1_opy_, bstack1111l11l1l_opy_)
        self.bstack1l11l1l1l11_opy_ = any(bstack11ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᐸ") in item.lower() for item in bstack1ll1ll111ll_opy_)
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
        if test_framework_state == bstack1lllll1l11l_opy_.TEST or test_framework_state in bstack1llll1l1ll1_opy_.bstack1l11l111ll1_opy_:
            bstack1l11l1ll1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lllll1l11l_opy_.NONE:
            self.logger.warning(bstack11ll111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᐹ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠧࠨᐺ"))
            return
        if not self.bstack1l11l1l1l11_opy_:
            self.logger.warning(bstack11ll111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᐻ") + str(str(self.bstack1ll1ll111ll_opy_)) + bstack11ll111_opy_ (u"ࠢࠣᐼ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11ll111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᐽ") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥᐾ"))
            return
        instance = self.__1l11l1lllll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᐿ") + str(args) + bstack11ll111_opy_ (u"ࠦࠧᑀ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1llll1l1ll1_opy_.bstack1l11l111ll1_opy_ and test_hook_state == bstack1ll1lll1ll1_opy_.PRE:
                bstack1ll1l111ll1_opy_ = bstack1llll11l1ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1l1ll111l_opy_.value)
                name = str(EVENTS.bstack1l1ll111l_opy_.name)+bstack11ll111_opy_ (u"ࠧࡀࠢᑁ")+str(test_framework_state.name)
                TestFramework.bstack1l111l1l111_opy_(instance, name, bstack1ll1l111ll1_opy_)
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᑂ").format(e))
        try:
            if not TestFramework.bstack11111l111l_opy_(instance, TestFramework.bstack1l11ll11lll_opy_) and test_hook_state == bstack1ll1lll1ll1_opy_.PRE:
                test = bstack1llll1l1ll1_opy_.__1l11ll11l11_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᑃ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠣࠤᑄ"))
            if test_framework_state == bstack1lllll1l11l_opy_.TEST:
                if test_hook_state == bstack1ll1lll1ll1_opy_.PRE and not TestFramework.bstack11111l111l_opy_(instance, TestFramework.bstack1l1lll1l1ll_opy_):
                    TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1l1lll1l1ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll111_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᑅ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠥࠦᑆ"))
                elif test_hook_state == bstack1ll1lll1ll1_opy_.POST and not TestFramework.bstack11111l111l_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_):
                    TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᑇ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠧࠨᑈ"))
            elif test_framework_state == bstack1lllll1l11l_opy_.LOG and test_hook_state == bstack1ll1lll1ll1_opy_.POST:
                bstack1llll1l1ll1_opy_.__1l11l111lll_opy_(instance, *args)
            elif test_framework_state == bstack1lllll1l11l_opy_.LOG_REPORT and test_hook_state == bstack1ll1lll1ll1_opy_.POST:
                self.__1l11ll1111l_opy_(instance, *args)
                self.__1l11l111l1l_opy_(instance)
            elif test_framework_state in bstack1llll1l1ll1_opy_.bstack1l11l111ll1_opy_:
                self.__1l111ll1lll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᑉ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠢࠣᑊ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111l1llll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1llll1l1ll1_opy_.bstack1l11l111ll1_opy_ and test_hook_state == bstack1ll1lll1ll1_opy_.POST:
                name = str(EVENTS.bstack1l1ll111l_opy_.name)+bstack11ll111_opy_ (u"ࠣ࠼ࠥᑋ")+str(test_framework_state.name)
                bstack1ll1l111ll1_opy_ = TestFramework.bstack1l11l11ll1l_opy_(instance, name)
                bstack1llll11l1ll_opy_.end(EVENTS.bstack1l1ll111l_opy_.value, bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᑌ"), bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᑍ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᑎ").format(e))
    def bstack1ll1111lll1_opy_(self):
        return self.bstack1l11l1l1l11_opy_
    def __1l11l11l111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11ll111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᑏ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll1111l11l_opy_(rep, [bstack11ll111_opy_ (u"ࠨࡷࡩࡧࡱࠦᑐ"), bstack11ll111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᑑ"), bstack11ll111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᑒ"), bstack11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᑓ"), bstack11ll111_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᑔ"), bstack11ll111_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᑕ")])
        return None
    def __1l11ll1111l_opy_(self, instance: bstack1llll1lllll_opy_, *args):
        result = self.__1l11l11l111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l1l11l_opy_ = None
        if result.get(bstack11ll111_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑖ"), None) == bstack11ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᑗ") and len(args) > 1 and getattr(args[1], bstack11ll111_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᑘ"), None) is not None:
            failure = [{bstack11ll111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᑙ"): [args[1].excinfo.exconly(), result.get(bstack11ll111_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᑚ"), None)]}]
            bstack1111l1l11l_opy_ = bstack11ll111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᑛ") if bstack11ll111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᑜ") in getattr(args[1].excinfo, bstack11ll111_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᑝ"), bstack11ll111_opy_ (u"ࠨࠢᑞ")) else bstack11ll111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᑟ")
        bstack1l11ll11ll1_opy_ = result.get(bstack11ll111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑠ"), TestFramework.bstack1l11l11l1ll_opy_)
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
            target = None # bstack1l11lll1111_opy_ bstack1l111ll1ll1_opy_ this to be bstack11ll111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᑡ")
            if test_framework_state == bstack1lllll1l11l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111lll11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lllll1l11l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11ll111_opy_ (u"ࠥࡲࡴࡪࡥࠣᑢ"), None), bstack11ll111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑣ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11ll111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑤ"), None):
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
        bstack1l111ll1l11_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, bstack1llll1l1ll1_opy_.bstack1l11l11l1l1_opy_, {})
        if not key in bstack1l111ll1l11_opy_:
            bstack1l111ll1l11_opy_[key] = []
        bstack1l111l111l1_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, bstack1llll1l1ll1_opy_.bstack1l111l1111l_opy_, {})
        if not key in bstack1l111l111l1_opy_:
            bstack1l111l111l1_opy_[key] = []
        bstack1l111lll1l1_opy_ = {
            bstack1llll1l1ll1_opy_.bstack1l11l11l1l1_opy_: bstack1l111ll1l11_opy_,
            bstack1llll1l1ll1_opy_.bstack1l111l1111l_opy_: bstack1l111l111l1_opy_,
        }
        if test_hook_state == bstack1ll1lll1ll1_opy_.PRE:
            hook = {
                bstack11ll111_opy_ (u"ࠨ࡫ࡦࡻࠥᑥ"): key,
                TestFramework.bstack1l111l11lll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll111ll_opy_: TestFramework.bstack1l111l1ll11_opy_,
                TestFramework.bstack1l11l1l11l1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111ll1l1l_opy_: [],
                TestFramework.bstack1l11ll1lll1_opy_: args[1] if len(args) > 1 else bstack11ll111_opy_ (u"ࠧࠨᑦ"),
                TestFramework.bstack1l111l111ll_opy_: bstack1lll11ll1ll_opy_.bstack1l11l11l11l_opy_()
            }
            bstack1l111ll1l11_opy_[key].append(hook)
            bstack1l111lll1l1_opy_[bstack1llll1l1ll1_opy_.bstack1l11l1llll1_opy_] = key
        elif test_hook_state == bstack1ll1lll1ll1_opy_.POST:
            bstack1l111ll1111_opy_ = bstack1l111ll1l11_opy_.get(key, [])
            hook = bstack1l111ll1111_opy_.pop() if bstack1l111ll1111_opy_ else None
            if hook:
                result = self.__1l11l11l111_opy_(*args)
                if result:
                    bstack1l111lll1ll_opy_ = result.get(bstack11ll111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑧ"), TestFramework.bstack1l111l1ll11_opy_)
                    if bstack1l111lll1ll_opy_ != TestFramework.bstack1l111l1ll11_opy_:
                        hook[TestFramework.bstack1l11ll111ll_opy_] = bstack1l111lll1ll_opy_
                hook[TestFramework.bstack1l111ll11l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l111ll_opy_]= bstack1lll11ll1ll_opy_.bstack1l11l11l11l_opy_()
                self.bstack1l11ll11l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1ll111_opy_, [])
                if logs: self.bstack1l1lll1l111_opy_(instance, logs)
                bstack1l111l111l1_opy_[key].append(hook)
                bstack1l111lll1l1_opy_[bstack1llll1l1ll1_opy_.bstack1l11l1l1lll_opy_] = key
        TestFramework.bstack1l111l1l1ll_opy_(instance, bstack1l111lll1l1_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᑨ") + str(bstack1l111l111l1_opy_) + bstack11ll111_opy_ (u"ࠥࠦᑩ"))
    def __1l11l1ll11l_opy_(
        self,
        context: bstack1l11l1l11ll_opy_,
        test_framework_state: bstack1lllll1l11l_opy_,
        test_hook_state: bstack1ll1lll1ll1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll1111l11l_opy_(args[0], [bstack11ll111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑪ"), bstack11ll111_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᑫ"), bstack11ll111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᑬ"), bstack11ll111_opy_ (u"ࠢࡪࡦࡶࠦᑭ"), bstack11ll111_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᑮ"), bstack11ll111_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᑯ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᑰ")) else fixturedef.get(bstack11ll111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑱ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11ll111_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᑲ")) else None
        node = request.node if hasattr(request, bstack11ll111_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᑳ")) else None
        target = request.node.nodeid if hasattr(node, bstack11ll111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑴ")) else None
        baseid = fixturedef.get(bstack11ll111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᑵ"), None) or bstack11ll111_opy_ (u"ࠤࠥᑶ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11ll111_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᑷ")):
            target = bstack1llll1l1ll1_opy_.__1l111llll11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11ll111_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᑸ")) else None
            if target and not TestFramework.bstack111111lll1_opy_(target):
                self.__1l111lll11l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᑹ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠨࠢᑺ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11ll111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᑻ") + str(target) + bstack11ll111_opy_ (u"ࠣࠤᑼ"))
            return None
        instance = TestFramework.bstack111111lll1_opy_(target)
        if not instance:
            self.logger.warning(bstack11ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᑽ") + str(target) + bstack11ll111_opy_ (u"ࠥࠦᑾ"))
            return None
        bstack1l11ll1ll11_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, bstack1llll1l1ll1_opy_.bstack1l111l11l11_opy_, {})
        if os.getenv(bstack11ll111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᑿ"), bstack11ll111_opy_ (u"ࠧ࠷ࠢᒀ")) == bstack11ll111_opy_ (u"ࠨ࠱ࠣᒁ"):
            bstack1l111l1lll1_opy_ = bstack11ll111_opy_ (u"ࠢ࠻ࠤᒂ").join((scope, fixturename))
            bstack1l111l11ll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111llll1l_opy_ = {
                bstack11ll111_opy_ (u"ࠣ࡭ࡨࡽࠧᒃ"): bstack1l111l1lll1_opy_,
                bstack11ll111_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᒄ"): bstack1llll1l1ll1_opy_.__1l111l11111_opy_(request.node),
                bstack11ll111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᒅ"): fixturedef,
                bstack11ll111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᒆ"): scope,
                bstack11ll111_opy_ (u"ࠧࡺࡹࡱࡧࠥᒇ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lll1ll1_opy_.POST and callable(getattr(args[-1], bstack11ll111_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᒈ"), None)):
                    bstack1l111llll1l_opy_[bstack11ll111_opy_ (u"ࠢࡵࡻࡳࡩࠧᒉ")] = TestFramework.bstack1ll1111llll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lll1ll1_opy_.PRE:
                bstack1l111llll1l_opy_[bstack11ll111_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᒊ")] = uuid4().__str__()
                bstack1l111llll1l_opy_[bstack1llll1l1ll1_opy_.bstack1l11l1l11l1_opy_] = bstack1l111l11ll1_opy_
            elif test_hook_state == bstack1ll1lll1ll1_opy_.POST:
                bstack1l111llll1l_opy_[bstack1llll1l1ll1_opy_.bstack1l111ll11l1_opy_] = bstack1l111l11ll1_opy_
            if bstack1l111l1lll1_opy_ in bstack1l11ll1ll11_opy_:
                bstack1l11ll1ll11_opy_[bstack1l111l1lll1_opy_].update(bstack1l111llll1l_opy_)
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᒋ") + str(bstack1l11ll1ll11_opy_[bstack1l111l1lll1_opy_]) + bstack11ll111_opy_ (u"ࠥࠦᒌ"))
            else:
                bstack1l11ll1ll11_opy_[bstack1l111l1lll1_opy_] = bstack1l111llll1l_opy_
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᒍ") + str(len(bstack1l11ll1ll11_opy_)) + bstack11ll111_opy_ (u"ࠧࠨᒎ"))
        TestFramework.bstack111111ll11_opy_(instance, bstack1llll1l1ll1_opy_.bstack1l111l11l11_opy_, bstack1l11ll1ll11_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᒏ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠢࠣᒐ"))
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
            bstack1llll1l1ll1_opy_.bstack1l111l11l11_opy_: {},
            bstack1llll1l1ll1_opy_.bstack1l111l1111l_opy_: {},
            bstack1llll1l1ll1_opy_.bstack1l11l11l1l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111111ll11_opy_(ob, TestFramework.bstack1l111ll111l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111111ll11_opy_(ob, TestFramework.bstack1ll1l1l1l1l_opy_, context.platform_index)
        TestFramework.bstack11111111l1_opy_[ctx.id] = ob
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᒑ") + str(TestFramework.bstack11111111l1_opy_.keys()) + bstack11ll111_opy_ (u"ࠤࠥᒒ"))
        return ob
    def bstack1l1ll1ll1ll_opy_(self, instance: bstack1llll1lllll_opy_, bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_]):
        bstack1l111llllll_opy_ = (
            bstack1llll1l1ll1_opy_.bstack1l11l1llll1_opy_
            if bstack11111ll1l1_opy_[1] == bstack1ll1lll1ll1_opy_.PRE
            else bstack1llll1l1ll1_opy_.bstack1l11l1l1lll_opy_
        )
        hook = bstack1llll1l1ll1_opy_.bstack1l11l1ll1ll_opy_(instance, bstack1l111llllll_opy_)
        entries = hook.get(TestFramework.bstack1l111ll1l1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_, []))
        return entries
    def bstack1l1ll1l1lll_opy_(self, instance: bstack1llll1lllll_opy_, bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_]):
        bstack1l111llllll_opy_ = (
            bstack1llll1l1ll1_opy_.bstack1l11l1llll1_opy_
            if bstack11111ll1l1_opy_[1] == bstack1ll1lll1ll1_opy_.PRE
            else bstack1llll1l1ll1_opy_.bstack1l11l1l1lll_opy_
        )
        bstack1llll1l1ll1_opy_.bstack1l11l1l1111_opy_(instance, bstack1l111llllll_opy_)
        TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_, []).clear()
    def bstack1l11ll11l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᒓ")
        global _1ll111l1lll_opy_
        platform_index = os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᒔ")]
        bstack1l1lll1lll1_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1ll111l1111_opy_ + str(platform_index)), bstack1l1111ll1ll_opy_)
        if not os.path.exists(bstack1l1lll1lll1_opy_) or not os.path.isdir(bstack1l1lll1lll1_opy_):
            self.logger.info(bstack11ll111_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥᒕ").format(bstack1l1lll1lll1_opy_))
            return
        logs = hook.get(bstack11ll111_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᒖ"), [])
        with os.scandir(bstack1l1lll1lll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111l1lll_opy_:
                    self.logger.info(bstack11ll111_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᒗ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11ll111_opy_ (u"ࠣࠤᒘ")
                    log_entry = bstack1lll1l11111_opy_(
                        kind=bstack11ll111_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᒙ"),
                        message=bstack11ll111_opy_ (u"ࠥࠦᒚ"),
                        level=bstack11ll111_opy_ (u"ࠦࠧᒛ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll11111_opy_=entry.stat().st_size,
                        bstack1ll1111111l_opy_=bstack11ll111_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᒜ"),
                        bstack1l1l1ll_opy_=os.path.abspath(entry.path),
                        bstack1l11ll1l11l_opy_=hook.get(TestFramework.bstack1l111l11lll_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111l1lll_opy_.add(abs_path)
        platform_index = os.environ[bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᒝ")]
        bstack1l11l1lll1l_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1ll111l1111_opy_ + str(platform_index)), bstack1l1111ll1ll_opy_, bstack1l1111lllll_opy_)
        if not os.path.exists(bstack1l11l1lll1l_opy_) or not os.path.isdir(bstack1l11l1lll1l_opy_):
            self.logger.info(bstack11ll111_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᒞ").format(bstack1l11l1lll1l_opy_))
        else:
            self.logger.info(bstack11ll111_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᒟ").format(bstack1l11l1lll1l_opy_))
            with os.scandir(bstack1l11l1lll1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111l1lll_opy_:
                        self.logger.info(bstack11ll111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᒠ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11ll111_opy_ (u"ࠥࠦᒡ")
                        log_entry = bstack1lll1l11111_opy_(
                            kind=bstack11ll111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᒢ"),
                            message=bstack11ll111_opy_ (u"ࠧࠨᒣ"),
                            level=bstack11ll111_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᒤ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll11111_opy_=entry.stat().st_size,
                            bstack1ll1111111l_opy_=bstack11ll111_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᒥ"),
                            bstack1l1l1ll_opy_=os.path.abspath(entry.path),
                            bstack1l1ll1l1l1l_opy_=hook.get(TestFramework.bstack1l111l11lll_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111l1lll_opy_.add(abs_path)
        hook[bstack11ll111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᒦ")] = logs
    def bstack1l1lll1l111_opy_(
        self,
        bstack1l1llll11ll_opy_: bstack1llll1lllll_opy_,
        entries: List[bstack1lll1l11111_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᒧ"))
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
            log_entry.message = entry.message.encode(bstack11ll111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᒨ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11ll111_opy_ (u"ࠦࠧᒩ")
            if entry.kind == bstack11ll111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᒪ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll11111_opy_
                log_entry.file_path = entry.bstack1l1l1ll_opy_
        def bstack1l1lll111ll_opy_():
            bstack11ll1lll1l_opy_ = datetime.now()
            try:
                self.bstack1lll11111ll_opy_.LogCreatedEvent(req)
                bstack1l1llll11ll_opy_.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᒫ"), datetime.now() - bstack11ll1lll1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᒬ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l11l1l_opy_.enqueue(bstack1l1lll111ll_opy_)
    def __1l11l111l1l_opy_(self, instance) -> None:
        bstack11ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᒭ")
        bstack1l111lll1l1_opy_ = {bstack11ll111_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᒮ"): bstack1lll11ll1ll_opy_.bstack1l11l11l11l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l111l1l1ll_opy_(instance, bstack1l111lll1l1_opy_)
    @staticmethod
    def bstack1l11l1ll1ll_opy_(instance: bstack1llll1lllll_opy_, bstack1l111llllll_opy_: str):
        bstack1l11ll1l1l1_opy_ = (
            bstack1llll1l1ll1_opy_.bstack1l111l1111l_opy_
            if bstack1l111llllll_opy_ == bstack1llll1l1ll1_opy_.bstack1l11l1l1lll_opy_
            else bstack1llll1l1ll1_opy_.bstack1l11l11l1l1_opy_
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
        hook = bstack1llll1l1ll1_opy_.bstack1l11l1ll1ll_opy_(instance, bstack1l111llllll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111ll1l1l_opy_, []).clear()
    @staticmethod
    def __1l11l111lll_opy_(instance: bstack1llll1lllll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11ll111_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᒯ"), None)):
            return
        if os.getenv(bstack11ll111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᒰ"), bstack11ll111_opy_ (u"ࠧ࠷ࠢᒱ")) != bstack11ll111_opy_ (u"ࠨ࠱ࠣᒲ"):
            bstack1llll1l1ll1_opy_.logger.warning(bstack11ll111_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᒳ"))
            return
        bstack1l111ll11ll_opy_ = {
            bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᒴ"): (bstack1llll1l1ll1_opy_.bstack1l11l1llll1_opy_, bstack1llll1l1ll1_opy_.bstack1l11l11l1l1_opy_),
            bstack11ll111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᒵ"): (bstack1llll1l1ll1_opy_.bstack1l11l1l1lll_opy_, bstack1llll1l1ll1_opy_.bstack1l111l1111l_opy_),
        }
        for when in (bstack11ll111_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᒶ"), bstack11ll111_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᒷ"), bstack11ll111_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᒸ")):
            bstack1l11ll1l111_opy_ = args[1].get_records(when)
            if not bstack1l11ll1l111_opy_:
                continue
            records = [
                bstack1lll1l11111_opy_(
                    kind=TestFramework.bstack1l1lll1l11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11ll111_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᒹ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11ll111_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᒺ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll1l111_opy_
                if isinstance(getattr(r, bstack11ll111_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᒻ"), None), str) and r.message.strip()
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
    def __1l11ll11l11_opy_(test) -> Dict[str, Any]:
        bstack11llll1l11_opy_ = bstack1llll1l1ll1_opy_.__1l111llll11_opy_(test.location) if hasattr(test, bstack11ll111_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᒼ")) else getattr(test, bstack11ll111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᒽ"), None)
        test_name = test.name if hasattr(test, bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᒾ")) else None
        bstack1l11l11ll11_opy_ = test.fspath.strpath if hasattr(test, bstack11ll111_opy_ (u"ࠧ࡬ࡳࡱࡣࡷ࡬ࠧᒿ")) and test.fspath else None
        if not bstack11llll1l11_opy_ or not test_name or not bstack1l11l11ll11_opy_:
            return None
        code = None
        if hasattr(test, bstack11ll111_opy_ (u"ࠨ࡯ࡣ࡬ࠥᓀ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l1111ll1l1_opy_ = []
        try:
            bstack1l1111ll1l1_opy_ = bstack11ll11ll11_opy_.bstack111ll1lll1_opy_(test)
        except:
            bstack1llll1l1ll1_opy_.logger.warning(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸ࠲ࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡲࡦࡵࡲࡰࡻ࡫ࡤࠡ࡫ࡱࠤࡈࡒࡉࠣᓁ"))
        return {
            TestFramework.bstack1ll1l11l1l1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll11lll_opy_: bstack11llll1l11_opy_,
            TestFramework.bstack1ll1l1111ll_opy_: test_name,
            TestFramework.bstack1l1ll1l1l11_opy_: getattr(test, bstack11ll111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᓂ"), None),
            TestFramework.bstack1l11ll111l1_opy_: bstack1l11l11ll11_opy_,
            TestFramework.bstack1l11l1111ll_opy_: bstack1llll1l1ll1_opy_.__1l111l11111_opy_(test),
            TestFramework.bstack1l11ll1l1ll_opy_: code,
            TestFramework.bstack1l1l1ll111l_opy_: TestFramework.bstack1l11l11l1ll_opy_,
            TestFramework.bstack1l1l1111ll1_opy_: bstack11llll1l11_opy_,
            TestFramework.bstack1l1111lll1l_opy_: bstack1l1111ll1l1_opy_
        }
    @staticmethod
    def __1l111l11111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11ll111_opy_ (u"ࠤࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠢᓃ"), [])
            markers.extend([getattr(m, bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᓄ"), None) for m in own_markers if getattr(m, bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᓅ"), None)])
            current = getattr(current, bstack11ll111_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᓆ"), None)
        return markers
    @staticmethod
    def __1l111llll11_opy_(location):
        return bstack11ll111_opy_ (u"ࠨ࠺࠻ࠤᓇ").join(filter(lambda x: isinstance(x, str), location))