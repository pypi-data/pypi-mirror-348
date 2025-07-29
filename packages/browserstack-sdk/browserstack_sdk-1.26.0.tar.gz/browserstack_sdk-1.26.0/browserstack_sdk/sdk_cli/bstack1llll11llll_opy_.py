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
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import bstack1llllll1ll1_opy_, bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll1l11l_opy_, bstack1llll1lllll_opy_, bstack1ll1lll1ll1_opy_, bstack1lll1l11111_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1ll1ll1l1_opy_, bstack1ll111l1ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1llllll11_opy_ = [bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆼ"), bstack11ll111_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᆽ"), bstack11ll111_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨᆾ"), bstack11ll111_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࠣᆿ"), bstack11ll111_opy_ (u"ࠣࡲࡤࡸ࡭ࠨᇀ")]
bstack1l1ll1lllll_opy_ = bstack1ll111l1ll1_opy_()
bstack1ll111l1111_opy_ = bstack11ll111_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᇁ")
bstack1ll11111ll1_opy_ = {
    bstack11ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡍࡹ࡫࡭ࠣᇂ"): bstack1l1llllll11_opy_,
    bstack11ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡕࡧࡣ࡬ࡣࡪࡩࠧᇃ"): bstack1l1llllll11_opy_,
    bstack11ll111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡓ࡯ࡥࡷ࡯ࡩࠧᇄ"): bstack1l1llllll11_opy_,
    bstack11ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡃ࡭ࡣࡶࡷࠧᇅ"): bstack1l1llllll11_opy_,
    bstack11ll111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡇࡷࡱࡧࡹ࡯࡯࡯ࠤᇆ"): bstack1l1llllll11_opy_
    + [
        bstack11ll111_opy_ (u"ࠣࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡱࡥࡲ࡫ࠢᇇ"),
        bstack11ll111_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᇈ"),
        bstack11ll111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨ࡭ࡳ࡬࡯ࠣᇉ"),
        bstack11ll111_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᇊ"),
        bstack11ll111_opy_ (u"ࠧࡩࡡ࡭࡮ࡶࡴࡪࡩࠢᇋ"),
        bstack11ll111_opy_ (u"ࠨࡣࡢ࡮࡯ࡳࡧࡰࠢᇌ"),
        bstack11ll111_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨᇍ"),
        bstack11ll111_opy_ (u"ࠣࡵࡷࡳࡵࠨᇎ"),
        bstack11ll111_opy_ (u"ࠤࡧࡹࡷࡧࡴࡪࡱࡱࠦᇏ"),
        bstack11ll111_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᇐ"),
    ],
    bstack11ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡩ࡯࠰ࡖࡩࡸࡹࡩࡰࡰࠥᇑ"): [bstack11ll111_opy_ (u"ࠧࡹࡴࡢࡴࡷࡴࡦࡺࡨࠣᇒ"), bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡷ࡫ࡧࡩ࡭ࡧࡧࠦᇓ"), bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡸࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠣᇔ"), bstack11ll111_opy_ (u"ࠣ࡫ࡷࡩࡲࡹࠢᇕ")],
    bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡦࡳࡳ࡬ࡩࡨ࠰ࡆࡳࡳ࡬ࡩࡨࠤᇖ"): [bstack11ll111_opy_ (u"ࠥ࡭ࡳࡼ࡯ࡤࡣࡷ࡭ࡴࡴ࡟ࡱࡣࡵࡥࡲࡹࠢᇗ"), bstack11ll111_opy_ (u"ࠦࡦࡸࡧࡴࠤᇘ")],
    bstack11ll111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡇ࡫ࡻࡸࡺࡸࡥࡅࡧࡩࠦᇙ"): [bstack11ll111_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᇚ"), bstack11ll111_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᇛ"), bstack11ll111_opy_ (u"ࠣࡨࡸࡲࡨࠨᇜ"), bstack11ll111_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᇝ"), bstack11ll111_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᇞ"), bstack11ll111_opy_ (u"ࠦ࡮ࡪࡳࠣᇟ")],
    bstack11ll111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡔࡷࡥࡖࡪࡷࡵࡦࡵࡷࠦᇠ"): [bstack11ll111_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᇡ"), bstack11ll111_opy_ (u"ࠢࡱࡣࡵࡥࡲࠨᇢ"), bstack11ll111_opy_ (u"ࠣࡲࡤࡶࡦࡳ࡟ࡪࡰࡧࡩࡽࠨᇣ")],
    bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡵࡹࡳࡴࡥࡳ࠰ࡆࡥࡱࡲࡉ࡯ࡨࡲࠦᇤ"): [bstack11ll111_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᇥ"), bstack11ll111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࠦᇦ")],
    bstack11ll111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡏࡱࡧࡩࡐ࡫ࡹࡸࡱࡵࡨࡸࠨᇧ"): [bstack11ll111_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᇨ"), bstack11ll111_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᇩ")],
    bstack11ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡑࡦࡸ࡫ࠣᇪ"): [bstack11ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇫ"), bstack11ll111_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᇬ"), bstack11ll111_opy_ (u"ࠦࡰࡽࡡࡳࡩࡶࠦᇭ")],
}
_1ll111l1lll_opy_ = set()
class bstack1lll1ll1lll_opy_(bstack1lll1l1111l_opy_):
    bstack1l1lllll11l_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࠧᇮ")
    bstack1l1llll1lll_opy_ = bstack11ll111_opy_ (u"ࠨࡉࡏࡈࡒࠦᇯ")
    bstack1ll1111l111_opy_ = bstack11ll111_opy_ (u"ࠢࡆࡔࡕࡓࡗࠨᇰ")
    bstack1l1lll11l11_opy_: Callable
    bstack1l1ll1lll1l_opy_: Callable
    def __init__(self, bstack1llll1l1l11_opy_, bstack1lll1l11ll1_opy_):
        super().__init__()
        self.bstack1ll1l1l11ll_opy_ = bstack1lll1l11ll1_opy_
        if os.getenv(bstack11ll111_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡐ࠳࠴࡝ࠧᇱ"), bstack11ll111_opy_ (u"ࠤ࠴ࠦᇲ")) != bstack11ll111_opy_ (u"ࠥ࠵ࠧᇳ") or not self.is_enabled():
            self.logger.warning(bstack11ll111_opy_ (u"ࠦࠧᇴ") + str(self.__class__.__name__) + bstack11ll111_opy_ (u"ࠧࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠣᇵ"))
            return
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.POST), self.bstack1ll1l111lll_opy_)
        for event in bstack1lllll1l11l_opy_:
            for state in bstack1ll1lll1ll1_opy_:
                TestFramework.bstack1ll11llll1l_opy_((event, state), self.bstack1l1lllllll1_opy_)
        bstack1llll1l1l11_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack11111ll1ll_opy_, bstack1llllll1l1l_opy_.POST), self.bstack1l1ll1lll11_opy_)
        self.bstack1l1lll11l11_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1lllll1ll_opy_(bstack1lll1ll1lll_opy_.bstack1l1llll1lll_opy_, self.bstack1l1lll11l11_opy_)
        self.bstack1l1ll1lll1l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1lllll1ll_opy_(bstack1lll1ll1lll_opy_.bstack1ll1111l111_opy_, self.bstack1l1ll1lll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lllllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1ll1111lll1_opy_() and instance:
            bstack1l1lll11ll1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack11111ll1l1_opy_
            if test_framework_state == bstack1lllll1l11l_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lllll1l11l_opy_.LOG:
                bstack11ll1lll1l_opy_ = datetime.now()
                entries = f.bstack1l1ll1ll1ll_opy_(instance, bstack11111ll1l1_opy_)
                if entries:
                    self.bstack1l1lll1l111_opy_(instance, entries)
                    instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࠨᇶ"), datetime.now() - bstack11ll1lll1l_opy_)
                    f.bstack1l1ll1l1lll_opy_(instance, bstack11111ll1l1_opy_)
                instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᇷ"), datetime.now() - bstack1l1lll11ll1_opy_)
                return # bstack1l1llll111l_opy_ not send this event with the bstack1l1lll11l1l_opy_ bstack1l1llllll1l_opy_
            elif (
                test_framework_state == bstack1lllll1l11l_opy_.TEST
                and test_hook_state == bstack1ll1lll1ll1_opy_.POST
                and not f.bstack11111l111l_opy_(instance, TestFramework.bstack1ll11111l11_opy_)
            ):
                self.logger.warning(bstack11ll111_opy_ (u"ࠣࡦࡵࡳࡵࡶࡩ࡯ࡩࠣࡨࡺ࡫ࠠࡵࡱࠣࡰࡦࡩ࡫ࠡࡱࡩࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࠨᇸ") + str(TestFramework.bstack11111l111l_opy_(instance, TestFramework.bstack1ll11111l11_opy_)) + bstack11ll111_opy_ (u"ࠤࠥᇹ"))
                f.bstack111111ll11_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1lllll11l_opy_, True)
                return # bstack1l1llll111l_opy_ not send this event bstack1l1lll1llll_opy_ bstack1l1lllll111_opy_
            elif (
                f.bstack1llllll1lll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1l1lllll11l_opy_, False)
                and test_framework_state == bstack1lllll1l11l_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1lll1ll1_opy_.POST
                and f.bstack11111l111l_opy_(instance, TestFramework.bstack1ll11111l11_opy_)
            ):
                self.logger.warning(bstack11ll111_opy_ (u"ࠥ࡭ࡳࡰࡥࡤࡶ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲࡙ࡋࡓࡕ࠮ࠣࡘࡪࡹࡴࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡔࡔ࡙ࡔࠡࠤᇺ") + str(TestFramework.bstack11111l111l_opy_(instance, TestFramework.bstack1ll11111l11_opy_)) + bstack11ll111_opy_ (u"ࠦࠧᇻ"))
                self.bstack1l1lllllll1_opy_(f, instance, (bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.POST), *args, **kwargs)
            bstack11ll1lll1l_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1ll1ll11l_opy_ = sorted(
                filter(lambda x: x.get(bstack11ll111_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᇼ"), None), data.pop(bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᇽ"), {}).values()),
                key=lambda x: x[bstack11ll111_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᇾ")],
            )
            if bstack1llll11lll1_opy_.bstack1ll111111ll_opy_ in data:
                data.pop(bstack1llll11lll1_opy_.bstack1ll111111ll_opy_)
            data.update({bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᇿ"): bstack1l1ll1ll11l_opy_})
            instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢሀ"), datetime.now() - bstack11ll1lll1l_opy_)
            bstack11ll1lll1l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1llll1l11_opy_)
            instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨሁ"), datetime.now() - bstack11ll1lll1l_opy_)
            self.bstack1l1llllll1l_opy_(instance, bstack11111ll1l1_opy_, event_json=event_json)
            instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢሂ"), datetime.now() - bstack1l1lll11ll1_opy_)
    def bstack1ll1l111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
        bstack1ll1l111ll1_opy_ = bstack1llll11l1ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack11l1ll1l_opy_.value)
        self.bstack1ll1l1l11ll_opy_.bstack1ll111ll111_opy_(instance, f, bstack11111ll1l1_opy_, *args, **kwargs)
        bstack1llll11l1ll_opy_.end(EVENTS.bstack11l1ll1l_opy_.value, bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧሃ"), bstack1ll1l111ll1_opy_ + bstack11ll111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦሄ"), status=True, failure=None, test_name=None)
    def bstack1ll1l111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1l1l11ll_opy_.bstack1ll11111111_opy_(instance, f, bstack11111ll1l1_opy_, *args, **kwargs)
        self.bstack1l1lll11lll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1llll1l1l_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1l1lll11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠥ࡭ࡒࡑࡅࠣࡧࡦࡲ࡬࠻ࠢࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠥህ"))
            return
        bstack11ll1lll1l_opy_ = datetime.now()
        try:
            r = self.bstack1lll11111ll_opy_.TestSessionEvent(req)
            instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡩࡻ࡫࡮ࡵࠤሆ"), datetime.now() - bstack11ll1lll1l_opy_)
            f.bstack111111ll11_opy_(instance, self.bstack1ll1l1l11ll_opy_.bstack1ll111l1l1l_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11ll111_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦሇ") + str(r) + bstack11ll111_opy_ (u"ࠥࠦለ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤሉ") + str(e) + bstack11ll111_opy_ (u"ࠧࠨሊ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll1lll11_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        _driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        _1ll11111l1l_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1llll1llll1_opy_.bstack1ll1l1lll1l_opy_(method_name):
            return
        if f.bstack1ll1l1111l1_opy_(*args) == bstack1llll1llll1_opy_.bstack1l1lll1ll1l_opy_:
            bstack1l1lll11ll1_opy_ = datetime.now()
            screenshot = result.get(bstack11ll111_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧላ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11ll111_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥ࡯࡭ࡢࡩࡨࠤࡧࡧࡳࡦ࠸࠷ࠤࡸࡺࡲࠣሌ"))
                return
            bstack1l1llll11ll_opy_ = self.bstack1l1lll1111l_opy_(instance)
            if bstack1l1llll11ll_opy_:
                entry = bstack1lll1l11111_opy_(TestFramework.bstack1ll111111l1_opy_, screenshot)
                self.bstack1l1lll1l111_opy_(bstack1l1llll11ll_opy_, [entry])
                instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡧࡻࡩࡨࡻࡴࡦࠤል"), datetime.now() - bstack1l1lll11ll1_opy_)
            else:
                self.logger.warning(bstack11ll111_opy_ (u"ࠤࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶࡨࡷࡹࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷ࡬࡮ࡹࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡼࡧࡳࠡࡶࡤ࡯ࡪࡴࠠࡣࡻࠣࡨࡷ࡯ࡶࡦࡴࡀࠤࢀࢃࠢሎ").format(instance.ref()))
        event = {}
        bstack1l1llll11ll_opy_ = self.bstack1l1lll1111l_opy_(instance)
        if bstack1l1llll11ll_opy_:
            self.bstack1l1llll1111_opy_(event, bstack1l1llll11ll_opy_)
            if event.get(bstack11ll111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣሏ")):
                self.bstack1l1lll1l111_opy_(bstack1l1llll11ll_opy_, event[bstack11ll111_opy_ (u"ࠦࡱࡵࡧࡴࠤሐ")])
            else:
                self.logger.info(bstack11ll111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡱࡵࡧࡴࠢࡩࡳࡷࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡩࡻ࡫࡮ࡵࠤሑ"))
    @measure(event_name=EVENTS.bstack1ll111l1l11_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1l1lll1l111_opy_(
        self,
        bstack1l1llll11ll_opy_: bstack1llll1lllll_opy_,
        entries: List[bstack1lll1l11111_opy_],
    ):
        self.bstack1ll11ll1ll1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1lll_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1ll1l1l1l1l_opy_)
        req.execution_context.hash = str(bstack1l1llll11ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llll11ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llll11ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1lll_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1ll1l1ll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1lll_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1ll1111ll1l_opy_)
            log_entry.uuid = TestFramework.bstack1llllll1lll_opy_(bstack1l1llll11ll_opy_, TestFramework.bstack1ll1l11l1l1_opy_)
            log_entry.test_framework_state = bstack1l1llll11ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧሒ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11ll111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤሓ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll11111_opy_
                log_entry.file_path = entry.bstack1l1l1ll_opy_
        def bstack1l1lll111ll_opy_():
            bstack11ll1lll1l_opy_ = datetime.now()
            try:
                self.bstack1lll11111ll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1ll111111l1_opy_:
                    bstack1l1llll11ll_opy_.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧሔ"), datetime.now() - bstack11ll1lll1l_opy_)
                elif entry.kind == TestFramework.bstack1l1llll11l1_opy_:
                    bstack1l1llll11ll_opy_.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨሕ"), datetime.now() - bstack11ll1lll1l_opy_)
                else:
                    bstack1l1llll11ll_opy_.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡰࡴ࡭ࠢሖ"), datetime.now() - bstack11ll1lll1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤሗ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l11l1l_opy_.enqueue(bstack1l1lll111ll_opy_)
    @measure(event_name=EVENTS.bstack1ll111l11l1_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1l1llllll1l_opy_(
        self,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        event_json=None,
    ):
        self.bstack1ll11ll1ll1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1l1l1l_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1ll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
        req.test_framework_state = bstack11111ll1l1_opy_[0].name
        req.test_hook_state = bstack11111ll1l1_opy_[1].name
        started_at = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1lll1l1ll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1llll1l11_opy_)).encode(bstack11ll111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦመ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1lll111ll_opy_():
            bstack11ll1lll1l_opy_ = datetime.now()
            try:
                self.bstack1lll11111ll_opy_.TestFrameworkEvent(req)
                instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡩࡻ࡫࡮ࡵࠤሙ"), datetime.now() - bstack11ll1lll1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧሚ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l11l1l_opy_.enqueue(bstack1l1lll111ll_opy_)
    def bstack1l1lll1111l_opy_(self, instance: bstack1llllll1ll1_opy_):
        bstack1l1lll111l1_opy_ = TestFramework.bstack111111111l_opy_(instance.context)
        for t in bstack1l1lll111l1_opy_:
            bstack1l1lll1ll11_opy_ = TestFramework.bstack1llllll1lll_opy_(t, bstack1llll11lll1_opy_.bstack1ll111111ll_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll1ll11_opy_):
                return t
    def bstack1l1ll1ll111_opy_(self, message):
        self.bstack1l1lll11l11_opy_(message + bstack11ll111_opy_ (u"ࠣ࡞ࡱࠦማ"))
    def log_error(self, message):
        self.bstack1l1ll1lll1l_opy_(message + bstack11ll111_opy_ (u"ࠤ࡟ࡲࠧሜ"))
    def bstack1l1lllll1ll_opy_(self, level, original_func):
        def bstack1ll111l111l_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1lll111l1_opy_ = TestFramework.bstack1l1lll1l1l1_opy_()
            if not bstack1l1lll111l1_opy_:
                return return_value
            bstack1l1llll11ll_opy_ = next(
                (
                    instance
                    for instance in bstack1l1lll111l1_opy_
                    if TestFramework.bstack11111l111l_opy_(instance, TestFramework.bstack1ll1l11l1l1_opy_)
                ),
                None,
            )
            if not bstack1l1llll11ll_opy_:
                return
            entry = bstack1lll1l11111_opy_(TestFramework.bstack1l1lll1l11l_opy_, message, level)
            self.bstack1l1lll1l111_opy_(bstack1l1llll11ll_opy_, [entry])
            return return_value
        return bstack1ll111l111l_opy_
    def bstack1l1llll1111_opy_(self, event: dict, instance=None) -> None:
        global _1ll111l1lll_opy_
        levels = [bstack11ll111_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨም"), bstack11ll111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣሞ")]
        bstack1ll11111lll_opy_ = bstack11ll111_opy_ (u"ࠧࠨሟ")
        if instance is not None:
            try:
                bstack1ll11111lll_opy_ = TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l11l1l1_opy_)
            except Exception as e:
                self.logger.warning(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡶ࡫ࡧࠤ࡫ࡸ࡯࡮ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦሠ").format(e))
        bstack1l1lllll1l1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧሡ")]
                bstack1l1lll1lll1_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1ll111l1111_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1lll1lll1_opy_):
                    self.logger.info(bstack11ll111_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡳࡵࡴࠡࡲࡵࡩࡸ࡫࡮ࡵࠢࡩࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡘࡪࡹࡴࠡࡣࡱࡨࠥࡈࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠣሢ").format(bstack1l1lll1lll1_opy_))
                file_names = os.listdir(bstack1l1lll1lll1_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1lll1lll1_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1ll111l1lll_opy_:
                        self.logger.info(bstack11ll111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢሣ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1llllllll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1llllllll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11ll111_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨሤ"):
                                entry = bstack1lll1l11111_opy_(
                                    kind=bstack11ll111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨሥ"),
                                    message=bstack11ll111_opy_ (u"ࠧࠨሦ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1lll11111_opy_=file_size,
                                    bstack1ll1111111l_opy_=bstack11ll111_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨሧ"),
                                    bstack1l1l1ll_opy_=os.path.abspath(file_path),
                                    bstack1l1l11111_opy_=bstack1ll11111lll_opy_
                                )
                            elif level == bstack11ll111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦረ"):
                                entry = bstack1lll1l11111_opy_(
                                    kind=bstack11ll111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥሩ"),
                                    message=bstack11ll111_opy_ (u"ࠤࠥሪ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1lll11111_opy_=file_size,
                                    bstack1ll1111111l_opy_=bstack11ll111_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥራ"),
                                    bstack1l1l1ll_opy_=os.path.abspath(file_path),
                                    bstack1l1ll1l1l1l_opy_=bstack1ll11111lll_opy_
                                )
                            bstack1l1lllll1l1_opy_.append(entry)
                            _1ll111l1lll_opy_.add(abs_path)
                        except Exception as bstack1ll1111l1ll_opy_:
                            self.logger.error(bstack11ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠢሬ").format(bstack1ll1111l1ll_opy_))
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠣር").format(e))
        event[bstack11ll111_opy_ (u"ࠨ࡬ࡰࡩࡶࠦሮ")] = bstack1l1lllll1l1_opy_
class bstack1l1llll1l11_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1ll1llll1_opy_ = set()
        kwargs[bstack11ll111_opy_ (u"ࠢࡴ࡭࡬ࡴࡰ࡫ࡹࡴࠤሯ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1ll111l11ll_opy_(obj, self.bstack1l1ll1llll1_opy_)
def bstack1l1ll1l1ll1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1ll111l11ll_opy_(obj, bstack1l1ll1llll1_opy_=None, max_depth=3):
    if bstack1l1ll1llll1_opy_ is None:
        bstack1l1ll1llll1_opy_ = set()
    if id(obj) in bstack1l1ll1llll1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1ll1llll1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1llll1ll1_opy_ = TestFramework.bstack1ll1111llll_opy_(obj)
    bstack1ll1111ll11_opy_ = next((k.lower() in bstack1l1llll1ll1_opy_.lower() for k in bstack1ll11111ll1_opy_.keys()), None)
    if bstack1ll1111ll11_opy_:
        obj = TestFramework.bstack1ll1111l11l_opy_(obj, bstack1ll11111ll1_opy_[bstack1ll1111ll11_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11ll111_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦሰ")):
            keys = getattr(obj, bstack11ll111_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧሱ"), [])
        elif hasattr(obj, bstack11ll111_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧሲ")):
            keys = getattr(obj, bstack11ll111_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨሳ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11ll111_opy_ (u"ࠧࡥࠢሴ"))}
        if not obj and bstack1l1llll1ll1_opy_ == bstack11ll111_opy_ (u"ࠨࡰࡢࡶ࡫ࡰ࡮ࡨ࠮ࡑࡱࡶ࡭ࡽࡖࡡࡵࡪࠥስ"):
            obj = {bstack11ll111_opy_ (u"ࠢࡱࡣࡷ࡬ࠧሶ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1ll1l1ll1_opy_(key) or str(key).startswith(bstack11ll111_opy_ (u"ࠣࡡࠥሷ")):
            continue
        if value is not None and bstack1l1ll1l1ll1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1ll111l11ll_opy_(value, bstack1l1ll1llll1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1ll111l11ll_opy_(o, bstack1l1ll1llll1_opy_, max_depth) for o in value]))
    return result or None