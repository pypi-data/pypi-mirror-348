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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import (
    bstack11111l1l1l_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lllllll11l_opy_,
    bstack1llllll1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_, bstack1llll1lllll_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1llll11111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lllll1lll1_opy_
from bstack_utils.helper import bstack1ll1ll11111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
import grpc
import traceback
import json
class bstack1ll1lll1lll_opy_(bstack1lll1l1111l_opy_):
    bstack1ll1l1llll1_opy_ = False
    bstack1ll1l1l1lll_opy_ = bstack11ll111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵࠦᄈ")
    bstack1ll1l11l111_opy_ = bstack11ll111_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥᄉ")
    bstack1ll1l11ll1l_opy_ = bstack11ll111_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹࠨᄊ")
    bstack1ll11ll11ll_opy_ = bstack11ll111_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡷࡤࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢᄋ")
    bstack1ll1l11ll11_opy_ = bstack11ll111_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢ࡬ࡦࡹ࡟ࡶࡴ࡯ࠦᄌ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1llll1l1l11_opy_, bstack1lll1l11ll1_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll1l1l11ll_opy_ = bstack1lll1l11ll1_opy_
        bstack1llll1l1l11_opy_.bstack1ll11llll1l_opy_((bstack11111l1l1l_opy_.bstack11111ll1ll_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll11llll11_opy_)
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll11llll1l_opy_((bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.POST), self.bstack1ll1l111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11lll11l_opy_(instance, args)
        test_framework = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1ll1l1_opy_)
        if bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᄍ") in instance.bstack1ll1ll111ll_opy_:
            platform_index = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1l1l1l_opy_)
            self.accessibility = self.bstack1ll1ll11l1l_opy_(tags, self.config[bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᄎ")][platform_index])
        else:
            capabilities = self.bstack1ll1l1l11ll_opy_.bstack1ll1l1l11l1_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᄏ") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣᄐ"))
                return
            self.accessibility = self.bstack1ll1ll11l1l_opy_(tags, capabilities)
        if self.bstack1ll1l1l11ll_opy_.pages and self.bstack1ll1l1l11ll_opy_.pages.values():
            bstack1ll1l1l1ll1_opy_ = list(self.bstack1ll1l1l11ll_opy_.pages.values())
            if bstack1ll1l1l1ll1_opy_ and isinstance(bstack1ll1l1l1ll1_opy_[0], (list, tuple)) and bstack1ll1l1l1ll1_opy_[0]:
                bstack1ll11ll1l11_opy_ = bstack1ll1l1l1ll1_opy_[0][0]
                if callable(bstack1ll11ll1l11_opy_):
                    page = bstack1ll11ll1l11_opy_()
                    def bstack1ll1l11l_opy_():
                        self.get_accessibility_results(page, bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᄑ"))
                    def bstack1ll1l1ll11l_opy_():
                        self.get_accessibility_results_summary(page, bstack11ll111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᄒ"))
                    setattr(page, bstack11ll111_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡸࠨᄓ"), bstack1ll1l11l_opy_)
                    setattr(page, bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡒࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨᄔ"), bstack1ll1l1ll11l_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠧࡹࡨࡰࡷ࡯ࡨࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡹࡥࡱࡻࡥ࠾ࠤᄕ") + str(self.accessibility) + bstack11ll111_opy_ (u"ࠨࠢᄖ"))
    def bstack1ll11llll11_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        driver: object,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        bstack11111ll1l1_opy_: Tuple[bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack11ll1lll1l_opy_ = datetime.now()
            self.bstack1ll1l1l111l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᄗ"), datetime.now() - bstack11ll1lll1l_opy_)
            if (
                not f.bstack1ll1l1lll1l_opy_(method_name)
                or f.bstack1ll1l1l1l11_opy_(method_name, *args)
                or f.bstack1ll1l11111l_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llllll1lll_opy_(instance, bstack1ll1lll1lll_opy_.bstack1ll1l11ll1l_opy_, False):
                if not bstack1ll1lll1lll_opy_.bstack1ll1l1llll1_opy_:
                    self.logger.warning(bstack11ll111_opy_ (u"ࠣ࡝ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦᄘ") + str(f.platform_index) + bstack11ll111_opy_ (u"ࠤࡠࠤࡦ࠷࠱ࡺࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡪࡤࡺࡪࠦ࡮ࡰࡶࠣࡦࡪ࡫࡮ࠡࡵࡨࡸࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᄙ"))
                    bstack1ll1lll1lll_opy_.bstack1ll1l1llll1_opy_ = True
                return
            bstack1ll1ll11lll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1ll11lll_opy_:
                platform_index = f.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1ll1l1l1l1l_opy_, 0)
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᄚ") + str(f.framework_name) + bstack11ll111_opy_ (u"ࠦࠧᄛ"))
                return
            bstack1ll1l11l1ll_opy_ = f.bstack1ll1l1111l1_opy_(*args)
            if not bstack1ll1l11l1ll_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࠢᄜ") + str(method_name) + bstack11ll111_opy_ (u"ࠨࠢᄝ"))
                return
            bstack1ll11lll1ll_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1ll1lll1lll_opy_.bstack1ll1l11ll11_opy_, False)
            if bstack1ll1l11l1ll_opy_ == bstack11ll111_opy_ (u"ࠢࡨࡧࡷࠦᄞ") and not bstack1ll11lll1ll_opy_:
                f.bstack111111ll11_opy_(instance, bstack1ll1lll1lll_opy_.bstack1ll1l11ll11_opy_, True)
                bstack1ll11lll1ll_opy_ = True
            if not bstack1ll11lll1ll_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠣࡰࡲࠤ࡚ࡘࡌࠡ࡮ࡲࡥࡩ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᄟ") + str(bstack1ll1l11l1ll_opy_) + bstack11ll111_opy_ (u"ࠤࠥᄠ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1l11l1ll_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᄡ") + str(bstack1ll1l11l1ll_opy_) + bstack11ll111_opy_ (u"ࠦࠧᄢ"))
                return
            self.logger.info(bstack11ll111_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡸࡩࡲࡪࡲࡷࡷࡤࡺ࡯ࡠࡴࡸࡲ࠮ࢃࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᄣ") + str(bstack1ll1l11l1ll_opy_) + bstack11ll111_opy_ (u"ࠨࠢᄤ"))
            scripts = [(s, bstack1ll1ll11lll_opy_[s]) for s in scripts_to_run if s in bstack1ll1ll11lll_opy_]
            for script_name, bstack1ll1l1l1111_opy_ in scripts:
                try:
                    bstack11ll1lll1l_opy_ = datetime.now()
                    if script_name == bstack11ll111_opy_ (u"ࠢࡴࡥࡤࡲࠧᄥ"):
                        result = self.perform_scan(driver, method=bstack1ll1l11l1ll_opy_, framework_name=f.framework_name)
                    instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࠢᄦ") + script_name, datetime.now() - bstack11ll1lll1l_opy_)
                    if isinstance(result, dict) and not result.get(bstack11ll111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᄧ"), True):
                        self.logger.warning(bstack11ll111_opy_ (u"ࠥࡷࡰ࡯ࡰࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡷ࡫࡭ࡢ࡫ࡱ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺࡳ࠻ࠢࠥᄨ") + str(result) + bstack11ll111_opy_ (u"ࠦࠧᄩ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺ࠽ࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃࠠࡦࡴࡵࡳࡷࡃࠢᄪ") + str(e) + bstack11ll111_opy_ (u"ࠨࠢᄫ"))
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡪࡸࡲࡰࡴࡀࠦᄬ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤᄭ"))
    def bstack1ll1l111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll1lllll_opy_,
        bstack11111ll1l1_opy_: Tuple[bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11lll11l_opy_(instance, args)
        capabilities = self.bstack1ll1l1l11ll_opy_.bstack1ll1l1l11l1_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll1ll11l1l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᄮ"))
            return
        driver = self.bstack1ll1l1l11ll_opy_.bstack1ll11ll111l_opy_(f, instance, bstack11111ll1l1_opy_, *args, **kwargs)
        test_name = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l1111ll_opy_)
        if not test_name:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣᄯ"))
            return
        test_uuid = f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll1l11l1l1_opy_)
        if not test_uuid:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤᄰ"))
            return
        if isinstance(self.bstack1ll1l1l11ll_opy_, bstack1llll11111l_opy_):
            framework_name = bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᄱ")
        else:
            framework_name = bstack11ll111_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᄲ")
        self.bstack1l1l111ll_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll1l111ll1_opy_ = bstack1llll11l1ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1l11l1l1ll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࠣᄳ"))
            return
        bstack11ll1lll1l_opy_ = datetime.now()
        bstack1ll1l1l1111_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll111_opy_ (u"ࠣࡵࡦࡥࡳࠨᄴ"), None)
        if not bstack1ll1l1l1111_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡩࡡ࡯ࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᄵ") + str(framework_name) + bstack11ll111_opy_ (u"ࠥࠤࠧᄶ"))
            return
        instance = bstack1lllllll11l_opy_.bstack111111lll1_opy_(driver)
        if instance:
            if not bstack1lllllll11l_opy_.bstack1llllll1lll_opy_(instance, bstack1ll1lll1lll_opy_.bstack1ll11ll11ll_opy_, False):
                bstack1lllllll11l_opy_.bstack111111ll11_opy_(instance, bstack1ll1lll1lll_opy_.bstack1ll11ll11ll_opy_, True)
            else:
                self.logger.info(bstack11ll111_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡮ࠡࡲࡵࡳ࡬ࡸࡥࡴࡵࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣᄷ") + str(method) + bstack11ll111_opy_ (u"ࠧࠨᄸ"))
                return
        self.logger.info(bstack11ll111_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦᄹ") + str(method) + bstack11ll111_opy_ (u"ࠢࠣᄺ"))
        if framework_name == bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᄻ"):
            result = self.bstack1ll1l1l11ll_opy_.bstack1ll1l1ll1ll_opy_(driver, bstack1ll1l1l1111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1l1111_opy_, {bstack11ll111_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᄼ"): method if method else bstack11ll111_opy_ (u"ࠥࠦᄽ")})
        bstack1llll11l1ll_opy_.end(EVENTS.bstack1l11l1l1ll_opy_.value, bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᄾ"), bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᄿ"), True, None, command=method)
        if instance:
            bstack1lllllll11l_opy_.bstack111111ll11_opy_(instance, bstack1ll1lll1lll_opy_.bstack1ll11ll11ll_opy_, False)
            instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾ࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰࠥᅀ"), datetime.now() - bstack11ll1lll1l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1llllllll1_opy_, stage=STAGE.bstack111lllll_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᅁ"))
            return
        bstack1ll1l1l1111_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll111_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧᅂ"), None)
        if not bstack1ll1l1l1111_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᅃ") + str(framework_name) + bstack11ll111_opy_ (u"ࠥࠦᅄ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11ll1lll1l_opy_ = datetime.now()
        if framework_name == bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᅅ"):
            result = self.bstack1ll1l1l11ll_opy_.bstack1ll1l1ll1ll_opy_(driver, bstack1ll1l1l1111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1l1111_opy_)
        instance = bstack1lllllll11l_opy_.bstack111111lll1_opy_(driver)
        if instance:
            instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࠣᅆ"), datetime.now() - bstack11ll1lll1l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l1ll11_opy_, stage=STAGE.bstack111lllll_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᅇ"))
            return
        bstack1ll1l1l1111_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll111_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᅈ"), None)
        if not bstack1ll1l1l1111_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᅉ") + str(framework_name) + bstack11ll111_opy_ (u"ࠤࠥᅊ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11ll1lll1l_opy_ = datetime.now()
        if framework_name == bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᅋ"):
            result = self.bstack1ll1l1l11ll_opy_.bstack1ll1l1ll1ll_opy_(driver, bstack1ll1l1l1111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1l1111_opy_)
        instance = bstack1lllllll11l_opy_.bstack111111lll1_opy_(driver)
        if instance:
            instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹࠣᅌ"), datetime.now() - bstack11ll1lll1l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1ll111l1_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1ll11lllll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll11ll1ll1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll11111ll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᅍ") + str(r) + bstack11ll111_opy_ (u"ࠨࠢᅎ"))
            else:
                self.bstack1ll11ll1l1l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᅏ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤᅐ"))
            traceback.print_exc()
            raise e
    def bstack1ll11ll1l1l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤ࡯ࡳࡦࡪ࡟ࡤࡱࡱࡪ࡮࡭࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤᅑ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll11lll1l1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1l1l1lll_opy_ and command.module == self.bstack1ll1l11l111_opy_:
                        if command.method and not command.method in bstack1ll11lll1l1_opy_:
                            bstack1ll11lll1l1_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll11lll1l1_opy_[command.method]:
                            bstack1ll11lll1l1_opy_[command.method][command.name] = list()
                        bstack1ll11lll1l1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll11lll1l1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1l1l111l_opy_(
        self,
        f: bstack1llll1llll1_opy_,
        exec: Tuple[bstack1llllll1ll1_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll1l1l11ll_opy_, bstack1llll11111l_opy_) and method_name != bstack11ll111_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᅒ"):
            return
        if bstack1lllllll11l_opy_.bstack11111l111l_opy_(instance, bstack1ll1lll1lll_opy_.bstack1ll1l11ll1l_opy_):
            return
        if not f.bstack1ll11llllll_opy_(instance):
            if not bstack1ll1lll1lll_opy_.bstack1ll1l1llll1_opy_:
                self.logger.warning(bstack11ll111_opy_ (u"ࠦࡦ࠷࠱ࡺࠢࡩࡰࡴࡽࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦ࡮ࡰࡰ࠰ࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠣᅓ"))
                bstack1ll1lll1lll_opy_.bstack1ll1l1llll1_opy_ = True
            return
        if f.bstack1ll1l1lllll_opy_(method_name, *args):
            bstack1ll1ll11ll1_opy_ = False
            desired_capabilities = f.bstack1ll1l11lll1_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11lll111_opy_(instance)
                platform_index = f.bstack1llllll1lll_opy_(instance, bstack1llll1llll1_opy_.bstack1ll1l1l1l1l_opy_, 0)
                bstack1ll1l111l11_opy_ = datetime.now()
                r = self.bstack1ll11lllll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᅔ"), datetime.now() - bstack1ll1l111l11_opy_)
                bstack1ll1ll11ll1_opy_ = r.success
            else:
                self.logger.error(bstack11ll111_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡥࡧࡶ࡭ࡷ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠽ࠣᅕ") + str(desired_capabilities) + bstack11ll111_opy_ (u"ࠢࠣᅖ"))
            f.bstack111111ll11_opy_(instance, bstack1ll1lll1lll_opy_.bstack1ll1l11ll1l_opy_, bstack1ll1ll11ll1_opy_)
    def bstack11ll1l11ll_opy_(self, test_tags):
        bstack1ll11lllll1_opy_ = self.config.get(bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᅗ"))
        if not bstack1ll11lllll1_opy_:
            return True
        try:
            include_tags = bstack1ll11lllll1_opy_[bstack11ll111_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᅘ")] if bstack11ll111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᅙ") in bstack1ll11lllll1_opy_ and isinstance(bstack1ll11lllll1_opy_[bstack11ll111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᅚ")], list) else []
            exclude_tags = bstack1ll11lllll1_opy_[bstack11ll111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᅛ")] if bstack11ll111_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᅜ") in bstack1ll11lllll1_opy_ and isinstance(bstack1ll11lllll1_opy_[bstack11ll111_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᅝ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᅞ") + str(error))
        return False
    def bstack11l1ll1l11_opy_(self, caps):
        try:
            bstack1ll1l1lll11_opy_ = caps.get(bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᅟ"), {}).get(bstack11ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᅠ"), caps.get(bstack11ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᅡ"), bstack11ll111_opy_ (u"ࠬ࠭ᅢ")))
            if bstack1ll1l1lll11_opy_:
                self.logger.warning(bstack11ll111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᅣ"))
                return False
            browser = caps.get(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᅤ"), bstack11ll111_opy_ (u"ࠨࠩᅥ")).lower()
            if browser != bstack11ll111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᅦ"):
                self.logger.warning(bstack11ll111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᅧ"))
                return False
            browser_version = caps.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᅨ"))
            if browser_version and browser_version != bstack11ll111_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᅩ") and int(browser_version.split(bstack11ll111_opy_ (u"࠭࠮ࠨᅪ"))[0]) <= 98:
                self.logger.warning(bstack11ll111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠻࠲ࠧᅫ"))
                return False
            bstack1ll1l11llll_opy_ = caps.get(bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᅬ"), {}).get(bstack11ll111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᅭ"))
            if bstack1ll1l11llll_opy_ and bstack11ll111_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᅮ") in bstack1ll1l11llll_opy_.get(bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡴࠩᅯ"), []):
                self.logger.warning(bstack11ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᅰ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᅱ") + str(error))
            return False
    def bstack1ll1l11l11l_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll1ll11l11_opy_ = {
            bstack11ll111_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᅲ"): test_uuid,
        }
        bstack1ll11ll1lll_opy_ = {}
        if result.success:
            bstack1ll11ll1lll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll1ll11111_opy_(bstack1ll1ll11l11_opy_, bstack1ll11ll1lll_opy_)
    def bstack1l1l111ll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll1l111ll1_opy_ = None
        try:
            self.bstack1ll11ll1ll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11ll111_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣᅳ")
            req.script_name = bstack11ll111_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢᅴ")
            r = self.bstack1lll11111ll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥࡪࡲࡪࡸࡨࡶࠥ࡫ࡸࡦࡥࡸࡸࡪࠦࡰࡢࡴࡤࡱࡸࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᅵ") + str(r.error) + bstack11ll111_opy_ (u"ࠦࠧᅶ"))
            else:
                bstack1ll1ll11l11_opy_ = self.bstack1ll1l11l11l_opy_(test_uuid, r)
                bstack1ll1l1l1111_opy_ = r.script
            self.logger.debug(bstack11ll111_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨᅷ") + str(bstack1ll1ll11l11_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll1l1l1111_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᅸ") + str(framework_name) + bstack11ll111_opy_ (u"ࠢࠡࠤᅹ"))
                return
            bstack1ll1l111ll1_opy_ = bstack1llll11l1ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1ll1l1ll111_opy_.value)
            self.bstack1ll1ll1111l_opy_(driver, bstack1ll1l1l1111_opy_, bstack1ll1ll11l11_opy_, framework_name)
            self.logger.info(bstack11ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᅺ"))
            bstack1llll11l1ll_opy_.end(EVENTS.bstack1ll1l1ll111_opy_.value, bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᅻ"), bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᅼ"), True, None, command=bstack11ll111_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᅽ"),test_name=name)
        except Exception as bstack1ll11ll11l1_opy_:
            self.logger.error(bstack11ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᅾ") + bstack11ll111_opy_ (u"ࠨࡳࡵࡴࠫࡴࡦࡺࡨࠪࠤᅿ") + bstack11ll111_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᆀ") + str(bstack1ll11ll11l1_opy_))
            bstack1llll11l1ll_opy_.end(EVENTS.bstack1ll1l1ll111_opy_.value, bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᆁ"), bstack1ll1l111ll1_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᆂ"), False, bstack1ll11ll11l1_opy_, command=bstack11ll111_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᆃ"),test_name=name)
    def bstack1ll1ll1111l_opy_(self, driver, bstack1ll1l1l1111_opy_, bstack1ll1ll11l11_opy_, framework_name):
        if framework_name == bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᆄ"):
            self.bstack1ll1l1l11ll_opy_.bstack1ll1l1ll1ll_opy_(driver, bstack1ll1l1l1111_opy_, bstack1ll1ll11l11_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1l1l1111_opy_, bstack1ll1ll11l11_opy_))
    def _1ll11lll11l_opy_(self, instance: bstack1llll1lllll_opy_, args: Tuple) -> list:
        bstack11ll111_opy_ (u"ࠧࠨࠢࡆࡺࡷࡶࡦࡩࡴࠡࡶࡤ࡫ࡸࠦࡢࡢࡵࡨࡨࠥࡵ࡮ࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࠢࠣࠤᆅ")
        if bstack11ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᆆ") in instance.bstack1ll1ll111ll_opy_:
            return args[2].tags if hasattr(args[2], bstack11ll111_opy_ (u"ࠧࡵࡣࡪࡷࠬᆇ")) else []
        if hasattr(args[0], bstack11ll111_opy_ (u"ࠨࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸ࠭ᆈ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll1ll11l1l_opy_(self, tags, capabilities):
        return self.bstack11ll1l11ll_opy_(tags) and self.bstack11l1ll1l11_opy_(capabilities)