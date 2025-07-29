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
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111l11l1l_opy_ import bstack1111l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1ll1lll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1llll1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1l11lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111ll1_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1111lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1llll11111l_opy_
from browserstack_sdk.sdk_cli.bstack1llll11llll_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll1_opy_ import bstack1l1lllll1_opy_, bstack1l111l11_opy_, bstack1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lll1lll1ll_opy_ import bstack1llll1l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import bstack1lllllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lllll1lll1_opy_
from bstack_utils.helper import Notset, bstack1ll1lll1l11_opy_, get_cli_dir, bstack1lll1l1l11l_opy_, bstack1ll1l1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1lllll1l1ll_opy_ import bstack1lll11ll1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1l11l_opy_ import bstack11l1llllll_opy_
from bstack_utils.helper import Notset, bstack1ll1lll1l11_opy_, get_cli_dir, bstack1lll1l1l11l_opy_, bstack1ll1l1lll_opy_, bstack11ll111ll1_opy_, bstack1l111ll1l_opy_, bstack1l1111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll1l11l_opy_, bstack1llll1lllll_opy_, bstack1ll1lll1ll1_opy_, bstack1lll1l11111_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import bstack1llllll1ll1_opy_, bstack11111l1l1l_opy_, bstack1llllll1l1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1l1ll11l_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1l1lll1_opy_, bstack1ll1l111_opy_
logger = bstack1l1l1ll11l_opy_.get_logger(__name__, bstack1l1l1ll11l_opy_.bstack1ll1lll11ll_opy_())
def bstack1lll1l1lll1_opy_(bs_config):
    bstack1llll111111_opy_ = None
    bstack1lll11l1l11_opy_ = None
    try:
        bstack1lll11l1l11_opy_ = get_cli_dir()
        bstack1llll111111_opy_ = bstack1lll1l1l11l_opy_(bstack1lll11l1l11_opy_)
        bstack1lll1l1ll11_opy_ = bstack1ll1lll1l11_opy_(bstack1llll111111_opy_, bstack1lll11l1l11_opy_, bs_config)
        bstack1llll111111_opy_ = bstack1lll1l1ll11_opy_ if bstack1lll1l1ll11_opy_ else bstack1llll111111_opy_
        if not bstack1llll111111_opy_:
            raise ValueError(bstack11ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠣဴ"))
    except Exception as ex:
        logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡲࡡࡵࡧࡶࡸࠥࡨࡩ࡯ࡣࡵࡽࠥࢁࡽࠣဵ").format(ex))
        bstack1llll111111_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠤံ"))
        if bstack1llll111111_opy_:
            logger.debug(bstack11ll111_opy_ (u"ࠢࡇࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠥ࡬ࡲࡰ࡯ࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠻့ࠢࠥ") + str(bstack1llll111111_opy_) + bstack11ll111_opy_ (u"ࠣࠤး"))
        else:
            logger.debug(bstack11ll111_opy_ (u"ࠤࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠻ࠡࡵࡨࡸࡺࡶࠠ࡮ࡣࡼࠤࡧ࡫ࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲္ࠧ"))
    return bstack1llll111111_opy_, bstack1lll11l1l11_opy_
bstack1llll1ll111_opy_ = bstack11ll111_opy_ (u"ࠥ࠽࠾࠿࠹်ࠣ")
bstack1lll1l11l11_opy_ = bstack11ll111_opy_ (u"ࠦࡷ࡫ࡡࡥࡻࠥျ")
bstack1lll1l111ll_opy_ = bstack11ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤြ")
bstack1lll111llll_opy_ = bstack11ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡌࡊࡕࡗࡉࡓࡥࡁࡅࡆࡕࠦွ")
bstack11ll1ll1ll_opy_ = bstack11ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠥှ")
bstack1llll1l11l1_opy_ = re.compile(bstack11ll111_opy_ (u"ࡳࠤࠫࡃ࡮࠯࠮ࠫࠪࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡽࡄࡖ࠭࠳࠰ࠢဿ"))
bstack1lll1ll1ll1_opy_ = bstack11ll111_opy_ (u"ࠤࡧࡩࡻ࡫࡬ࡰࡲࡰࡩࡳࡺࠢ၀")
bstack1lll1ll11ll_opy_ = [
    bstack1l111l11_opy_.bstack1l1ll1ll_opy_,
    bstack1l111l11_opy_.CONNECT,
    bstack1l111l11_opy_.bstack1ll1lll1ll_opy_,
]
class SDKCLI:
    _1lll11lllll_opy_ = None
    process: Union[None, Any]
    bstack1lll1ll11l1_opy_: bool
    bstack1lllll1l111_opy_: bool
    bstack1lllll111ll_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lll1l1llll_opy_: Union[None, grpc.Channel]
    bstack1lllll1111l_opy_: str
    test_framework: TestFramework
    bstack1lllllll1l1_opy_: bstack1lllllll11l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1llll1l1111_opy_: bstack1lll1ll1lll_opy_
    accessibility: bstack1ll1lll1lll_opy_
    bstack1lll1l11l_opy_: bstack11l1llllll_opy_
    ai: bstack1llll1ll1ll_opy_
    bstack1lllll1l1l1_opy_: bstack1lll1l11lll_opy_
    bstack1ll1lll1l1l_opy_: List[bstack1lll1l1111l_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll1llllll1_opy_: Any
    bstack1llll11l11l_opy_: Dict[str, timedelta]
    bstack1ll1lllll1l_opy_: str
    bstack1111l11l1l_opy_: bstack1111l1111l_opy_
    def __new__(cls):
        if not cls._1lll11lllll_opy_:
            cls._1lll11lllll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lll11lllll_opy_
    def __init__(self):
        self.process = None
        self.bstack1lll1ll11l1_opy_ = False
        self.bstack1lll1l1llll_opy_ = None
        self.bstack1lll11111ll_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1lll111llll_opy_, None)
        self.bstack1llllll1111_opy_ = os.environ.get(bstack1lll1l111ll_opy_, bstack11ll111_opy_ (u"ࠥࠦ၁")) == bstack11ll111_opy_ (u"ࠦࠧ၂")
        self.bstack1lllll1l111_opy_ = False
        self.bstack1lllll111ll_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll1llllll1_opy_ = None
        self.test_framework = None
        self.bstack1lllllll1l1_opy_ = None
        self.bstack1lllll1111l_opy_=bstack11ll111_opy_ (u"ࠧࠨ၃")
        self.session_framework = None
        self.logger = bstack1l1l1ll11l_opy_.get_logger(self.__class__.__name__, bstack1l1l1ll11l_opy_.bstack1ll1lll11ll_opy_())
        self.bstack1llll11l11l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111l11l1l_opy_ = bstack1111l1111l_opy_()
        self.bstack1llll1l1l11_opy_ = None
        self.bstack1lll1l11ll1_opy_ = None
        self.bstack1llll1l1111_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1lll1l1l_opy_ = []
    def bstack111l11lll_opy_(self):
        return os.environ.get(bstack11ll1ll1ll_opy_).lower().__eq__(bstack11ll111_opy_ (u"ࠨࡴࡳࡷࡨࠦ၄"))
    def is_enabled(self, config):
        if bstack11ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ၅") in config and str(config[bstack11ll111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ၆")]).lower() != bstack11ll111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ၇"):
            return False
        bstack1lll11ll1l1_opy_ = [bstack11ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥ၈"), bstack11ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ၉")]
        bstack1lllll111l1_opy_ = config.get(bstack11ll111_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣ၊")) in bstack1lll11ll1l1_opy_ or os.environ.get(bstack11ll111_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧ။")) in bstack1lll11ll1l1_opy_
        os.environ[bstack11ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥ၌")] = str(bstack1lllll111l1_opy_) # bstack1ll1lllllll_opy_ bstack1llll1ll1l1_opy_ VAR to bstack1ll1lll111l_opy_ is binary running
        return bstack1lllll111l1_opy_
    def bstack11ll111l1_opy_(self):
        for event in bstack1lll1ll11ll_opy_:
            bstack1l1lllll1_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1l1lllll1_opy_.logger.debug(bstack11ll111_opy_ (u"ࠣࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠠ࠾ࡀࠣࡿࡦࡸࡧࡴࡿࠣࠦ၍") + str(kwargs) + bstack11ll111_opy_ (u"ࠤࠥ၎"))
            )
        bstack1l1lllll1_opy_.register(bstack1l111l11_opy_.bstack1l1ll1ll_opy_, self.__1lll11l1l1l_opy_)
        bstack1l1lllll1_opy_.register(bstack1l111l11_opy_.CONNECT, self.__1ll1lll1111_opy_)
        bstack1l1lllll1_opy_.register(bstack1l111l11_opy_.bstack1ll1lll1ll_opy_, self.__1lll111l111_opy_)
        bstack1l1lllll1_opy_.register(bstack1l111l11_opy_.bstack11lllll1l1_opy_, self.__1llll1lll1l_opy_)
    def bstack111l111l1_opy_(self):
        return not self.bstack1llllll1111_opy_ and os.environ.get(bstack1lll1l111ll_opy_, bstack11ll111_opy_ (u"ࠥࠦ၏")) != bstack11ll111_opy_ (u"ࠦࠧၐ")
    def is_running(self):
        if self.bstack1llllll1111_opy_:
            return self.bstack1lll1ll11l1_opy_
        else:
            return bool(self.bstack1lll1l1llll_opy_)
    def bstack1lllll11l1l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1lll1l1l_opy_) and cli.is_running()
    def __1llll111l11_opy_(self, bstack1lll111111l_opy_=10):
        if self.bstack1lll11111ll_opy_:
            return
        bstack11ll1lll1l_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1lll111llll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11ll111_opy_ (u"ࠧࡡࠢၑ") + str(id(self)) + bstack11ll111_opy_ (u"ࠨ࡝ࠡࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡱ࡫ࠧၒ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11ll111_opy_ (u"ࠢࡨࡴࡳࡧ࠳࡫࡮ࡢࡤ࡯ࡩࡤ࡮ࡴࡵࡲࡢࡴࡷࡵࡸࡺࠤၓ"), 0), (bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨ࠴ࡥ࡯ࡣࡥࡰࡪࡥࡨࡵࡶࡳࡷࡤࡶࡲࡰࡺࡼࠦၔ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll111111l_opy_)
        self.bstack1lll1l1llll_opy_ = channel
        self.bstack1lll11111ll_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lll1l1llll_opy_)
        self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡤࡱࡱࡲࡪࡩࡴࠣၕ"), datetime.now() - bstack11ll1lll1l_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1lll111llll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨ࠿ࠦࡩࡴࡡࡦ࡬࡮ࡲࡤࡠࡲࡵࡳࡨ࡫ࡳࡴ࠿ࠥၖ") + str(self.bstack111l111l1_opy_()) + bstack11ll111_opy_ (u"ࠦࠧၗ"))
    def __1lll111l111_opy_(self, event_name):
        if self.bstack111l111l1_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡳࡵࡱࡳࡴ࡮ࡴࡧࠡࡅࡏࡍࠧၘ"))
        self.__1lllll1ll1l_opy_()
    def __1llll1lll1l_opy_(self, event_name, bstack1llll1lll11_opy_ = None, bstack11lll11lll_opy_=1):
        if bstack11lll11lll_opy_ == 1:
            self.logger.error(bstack11ll111_opy_ (u"ࠨࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠨၙ"))
        bstack1lll1lll1l1_opy_ = Path(bstack1ll1llll11l_opy_ (u"ࠢࡼࡵࡨࡰ࡫࠴ࡣ࡭࡫ࡢࡨ࡮ࡸࡽ࠰ࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࡵ࠱࡮ࡸࡵ࡮ࠣၚ"))
        if self.bstack1lll11l1l11_opy_ and bstack1lll1lll1l1_opy_.exists():
            with open(bstack1lll1lll1l1_opy_, bstack11ll111_opy_ (u"ࠨࡴࠪၛ"), encoding=bstack11ll111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨၜ")) as fp:
                data = json.load(fp)
                try:
                    bstack11ll111ll1_opy_(bstack11ll111_opy_ (u"ࠪࡔࡔ࡙ࡔࠨၝ"), bstack1l111ll1l_opy_(bstack1111111ll_opy_), data, {
                        bstack11ll111_opy_ (u"ࠫࡦࡻࡴࡩࠩၞ"): (self.config[bstack11ll111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧၟ")], self.config[bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩၠ")])
                    })
                except Exception as e:
                    logger.debug(bstack1ll1l111_opy_.format(str(e)))
            bstack1lll1lll1l1_opy_.unlink()
        sys.exit(bstack11lll11lll_opy_)
    @measure(event_name=EVENTS.bstack1lll111ll11_opy_, stage=STAGE.bstack111lllll_opy_)
    def __1lll11l1l1l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1l1l11llll_opy_ import bstack1llll11l1ll_opy_
        self.bstack1lllll1111l_opy_, self.bstack1lll11l1l11_opy_ = bstack1lll1l1lll1_opy_(data.bs_config)
        os.environ[bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡗࡓࡋࡗࡅࡇࡒࡅࡠࡆࡌࡖࠬၡ")] = self.bstack1lll11l1l11_opy_
        if not self.bstack1lllll1111l_opy_ or not self.bstack1lll11l1l11_opy_:
            raise ValueError(bstack11ll111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠢၢ"))
        if self.bstack111l111l1_opy_():
            self.__1ll1lll1111_opy_(event_name, bstack1ll1ll1l_opy_())
            return
        try:
            bstack1llll11l1ll_opy_.end(EVENTS.bstack1ll111l1l_opy_.value, EVENTS.bstack1ll111l1l_opy_.value + bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤၣ"), EVENTS.bstack1ll111l1l_opy_.value + bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣၤ"), status=True, failure=None, test_name=None)
            logger.debug(bstack11ll111_opy_ (u"ࠦࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡓࡅࡍࠣࡗࡪࡺࡵࡱ࠰ࠥၥ"))
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡻࡾࠤၦ").format(e))
        start = datetime.now()
        is_started = self.__1lll1l1l1ll_opy_()
        self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠨࡳࡱࡣࡺࡲࡤࡺࡩ࡮ࡧࠥၧ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1llll111l11_opy_()
            self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨၨ"), datetime.now() - start)
            start = datetime.now()
            self.__1lllll11ll1_opy_(data)
            self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨၩ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll1111l1l_opy_, stage=STAGE.bstack111lllll_opy_)
    def __1ll1lll1111_opy_(self, event_name: str, data: bstack1ll1ll1l_opy_):
        if not self.bstack111l111l1_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࡀࠠ࡯ࡱࡷࠤࡦࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨၪ"))
            return
        bin_session_id = os.environ.get(bstack1lll1l111ll_opy_)
        start = datetime.now()
        self.__1llll111l11_opy_()
        self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤၫ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11ll111_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠠࡵࡱࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡉࡌࡊࠢࠥၬ") + str(bin_session_id) + bstack11ll111_opy_ (u"ࠧࠨၭ"))
        start = datetime.now()
        self.__1lll11ll111_opy_()
        self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦၮ"), datetime.now() - start)
    def __1llll1l1lll_opy_(self):
        if not self.bstack1lll11111ll_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡤࡣࡱࡲࡴࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡱࡴࡪࡵ࡭ࡧࡶࠦၯ"))
            return
        bstack1lll11ll11l_opy_ = {
            bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧၰ"): (bstack1lll1111lll_opy_, bstack1llll11111l_opy_, bstack1lllll1lll1_opy_),
            bstack11ll111_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦၱ"): (bstack1llll1111ll_opy_, bstack1llll11lll1_opy_, bstack1llll1llll1_opy_),
        }
        if not self.bstack1llll1l1l11_opy_ and self.session_framework in bstack1lll11ll11l_opy_:
            bstack1lll111l1ll_opy_, bstack1lll11l1lll_opy_, bstack1llll11ll1l_opy_ = bstack1lll11ll11l_opy_[self.session_framework]
            bstack1lll1llll1l_opy_ = bstack1lll11l1lll_opy_()
            self.bstack1lll1l11ll1_opy_ = bstack1lll1llll1l_opy_
            self.bstack1llll1l1l11_opy_ = bstack1llll11ll1l_opy_
            self.bstack1ll1lll1l1l_opy_.append(bstack1lll1llll1l_opy_)
            self.bstack1ll1lll1l1l_opy_.append(bstack1lll111l1ll_opy_(self.bstack1lll1l11ll1_opy_))
        if not self.bstack1llll1l1111_opy_ and self.config_observability and self.config_observability.success: # bstack1lll1ll1l1l_opy_
            self.bstack1llll1l1111_opy_ = bstack1lll1ll1lll_opy_(self.bstack1llll1l1l11_opy_, self.bstack1lll1l11ll1_opy_) # bstack1lllll11lll_opy_
            self.bstack1ll1lll1l1l_opy_.append(self.bstack1llll1l1111_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll1lll1lll_opy_(self.bstack1llll1l1l11_opy_, self.bstack1lll1l11ll1_opy_)
            self.bstack1ll1lll1l1l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11ll111_opy_ (u"ࠥࡷࡪࡲࡦࡉࡧࡤࡰࠧၲ"), False) == True:
            self.ai = bstack1llll1ll1ll_opy_()
            self.bstack1ll1lll1l1l_opy_.append(self.ai)
        if not self.percy and self.bstack1ll1llllll1_opy_ and self.bstack1ll1llllll1_opy_.success:
            self.percy = bstack1lll1l11lll_opy_(self.bstack1ll1llllll1_opy_)
            self.bstack1ll1lll1l1l_opy_.append(self.percy)
        for mod in self.bstack1ll1lll1l1l_opy_:
            if not mod.bstack1lll11l111l_opy_():
                mod.configure(self.bstack1lll11111ll_opy_, self.config, self.cli_bin_session_id, self.bstack1111l11l1l_opy_)
    def __1lll111ll1l_opy_(self):
        for mod in self.bstack1ll1lll1l1l_opy_:
            if mod.bstack1lll11l111l_opy_():
                mod.configure(self.bstack1lll11111ll_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1llll1l111l_opy_, stage=STAGE.bstack111lllll_opy_)
    def __1lllll11ll1_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lllll1l111_opy_:
            return
        self.__1llll11l111_opy_(data)
        bstack11ll1lll1l_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11ll111_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦၳ")
        req.sdk_language = bstack11ll111_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧၴ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1llll1l11l1_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡛ࠣၵ") + str(id(self)) + bstack11ll111_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨၶ"))
            r = self.bstack1lll11111ll_opy_.StartBinSession(req)
            self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥၷ"), datetime.now() - bstack11ll1lll1l_opy_)
            os.environ[bstack1lll1l111ll_opy_] = r.bin_session_id
            self.__1ll1lllll11_opy_(r)
            self.__1llll1l1lll_opy_()
            self.bstack1111l11l1l_opy_.start()
            self.bstack1lllll1l111_opy_ = True
            self.logger.debug(bstack11ll111_opy_ (u"ࠤ࡞ࠦၸ") + str(id(self)) + bstack11ll111_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣၹ"))
        except grpc.bstack1ll1llll1l1_opy_ as bstack1lllll1llll_opy_:
            self.logger.error(bstack11ll111_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨၺ") + str(bstack1lllll1llll_opy_) + bstack11ll111_opy_ (u"ࠧࠨၻ"))
            traceback.print_exc()
            raise bstack1lllll1llll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥၼ") + str(e) + bstack11ll111_opy_ (u"ࠢࠣၽ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1llll11ll11_opy_, stage=STAGE.bstack111lllll_opy_)
    def __1lll11ll111_opy_(self):
        if not self.bstack111l111l1_opy_() or not self.cli_bin_session_id or self.bstack1lllll111ll_opy_:
            return
        bstack11ll1lll1l_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨၾ"), bstack11ll111_opy_ (u"ࠩ࠳ࠫၿ")))
        try:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡟ࠧႀ") + str(id(self)) + bstack11ll111_opy_ (u"ࠦࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨႁ"))
            r = self.bstack1lll11111ll_opy_.ConnectBinSession(req)
            self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤႂ"), datetime.now() - bstack11ll1lll1l_opy_)
            self.__1ll1lllll11_opy_(r)
            self.__1llll1l1lll_opy_()
            self.bstack1111l11l1l_opy_.start()
            self.bstack1lllll111ll_opy_ = True
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡛ࠣႃ") + str(id(self)) + bstack11ll111_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠨႄ"))
        except grpc.bstack1ll1llll1l1_opy_ as bstack1lllll1llll_opy_:
            self.logger.error(bstack11ll111_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥႅ") + str(bstack1lllll1llll_opy_) + bstack11ll111_opy_ (u"ࠤࠥႆ"))
            traceback.print_exc()
            raise bstack1lllll1llll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢႇ") + str(e) + bstack11ll111_opy_ (u"ࠦࠧႈ"))
            traceback.print_exc()
            raise e
    def __1ll1lllll11_opy_(self, r):
        self.bstack1lll1ll1111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11ll111_opy_ (u"ࠧࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦႉ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11ll111_opy_ (u"ࠨࡥ࡮ࡲࡷࡽࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡯ࡶࡰࡧࠦႊ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕ࡫ࡲࡤࡻࠣ࡭ࡸࠦࡳࡦࡰࡷࠤࡴࡴ࡬ࡺࠢࡤࡷࠥࡶࡡࡳࡶࠣࡳ࡫ࠦࡴࡩࡧࠣࠦࡈࡵ࡮࡯ࡧࡦࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮࠭ࠤࠣࡥࡳࡪࠠࡵࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡪࡵࠣࡥࡱࡹ࡯ࠡࡷࡶࡩࡩࠦࡢࡺࠢࡖࡸࡦࡸࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡧࡵࡩ࡫ࡵࡲࡦ࠮ࠣࡒࡴࡴࡥࠡࡪࡤࡲࡩࡲࡩ࡯ࡩࠣ࡭ࡸࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤႋ")
        self.bstack1ll1llllll1_opy_ = getattr(r, bstack11ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧႌ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙ႍ࠭")] = self.config_testhub.jwt
        os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨႎ")] = self.config_testhub.build_hashed_id
    def bstack1lll1l111l1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lll1ll11l1_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1lll1111111_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1lll1111111_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll1l111l1_opy_(event_name=EVENTS.bstack1lll1ll111l_opy_, stage=STAGE.bstack111lllll_opy_)
    def __1lll1l1l1ll_opy_(self, bstack1lll111111l_opy_=10):
        if self.bstack1lll1ll11l1_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸࡺࡡࡳࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨႏ"))
            return True
        self.logger.debug(bstack11ll111_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦ႐"))
        if os.getenv(bstack11ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡈࡒ࡛ࠨ႑")) == bstack1lll1ll1ll1_opy_:
            self.cli_bin_session_id = bstack1lll1ll1ll1_opy_
            self.cli_listen_addr = bstack11ll111_opy_ (u"ࠢࡶࡰ࡬ࡼ࠿࠵ࡴ࡮ࡲ࠲ࡷࡩࡱ࠭ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࠨࡷ࠳ࡹ࡯ࡤ࡭ࠥ႒") % (self.cli_bin_session_id)
            self.bstack1lll1ll11l1_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lllll1111l_opy_, bstack11ll111_opy_ (u"ࠣࡵࡧ࡯ࠧ႓")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1lll1llll11_opy_ compat for text=True in bstack1lll1ll1l11_opy_ python
            encoding=bstack11ll111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ႔"),
            bufsize=1,
            close_fds=True,
        )
        bstack1llll1111l1_opy_ = threading.Thread(target=self.__1llll111lll_opy_, args=(bstack1lll111111l_opy_,))
        bstack1llll1111l1_opy_.start()
        bstack1llll1111l1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡶࡴࡦࡽ࡮࠻ࠢࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࡃࡻࡴࡧ࡯ࡪ࠳ࡶࡲࡰࡥࡨࡷࡸ࠴ࡲࡦࡶࡸࡶࡳࡩ࡯ࡥࡧࢀࠤࡴࡻࡴ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡵࡷࡨࡴࡻࡴ࠯ࡴࡨࡥࡩ࠮ࠩࡾࠢࡨࡶࡷࡃࠢ႕") + str(self.process.stderr.read()) + bstack11ll111_opy_ (u"ࠦࠧ႖"))
        if not self.bstack1lll1ll11l1_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡡࠢ႗") + str(id(self)) + bstack11ll111_opy_ (u"ࠨ࡝ࠡࡥ࡯ࡩࡦࡴࡵࡱࠤ႘"))
            self.__1lllll1ll1l_opy_()
        self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡰࡳࡱࡦࡩࡸࡹ࡟ࡳࡧࡤࡨࡾࡀࠠࠣ႙") + str(self.bstack1lll1ll11l1_opy_) + bstack11ll111_opy_ (u"ࠣࠤႚ"))
        return self.bstack1lll1ll11l1_opy_
    def __1llll111lll_opy_(self, bstack1lll1l1l111_opy_=10):
        bstack1llllll111l_opy_ = time.time()
        while self.process and time.time() - bstack1llllll111l_opy_ < bstack1lll1l1l111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11ll111_opy_ (u"ࠤ࡬ࡨࡂࠨႛ") in line:
                    self.cli_bin_session_id = line.split(bstack11ll111_opy_ (u"ࠥ࡭ࡩࡃࠢႜ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll111_opy_ (u"ࠦࡨࡲࡩࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠼ࠥႝ") + str(self.cli_bin_session_id) + bstack11ll111_opy_ (u"ࠧࠨ႞"))
                    continue
                if bstack11ll111_opy_ (u"ࠨ࡬ࡪࡵࡷࡩࡳࡃࠢ႟") in line:
                    self.cli_listen_addr = line.split(bstack11ll111_opy_ (u"ࠢ࡭࡫ࡶࡸࡪࡴ࠽ࠣႠ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll111_opy_ (u"ࠣࡥ࡯࡭ࡤࡲࡩࡴࡶࡨࡲࡤࡧࡤࡥࡴ࠽ࠦႡ") + str(self.cli_listen_addr) + bstack11ll111_opy_ (u"ࠤࠥႢ"))
                    continue
                if bstack11ll111_opy_ (u"ࠥࡴࡴࡸࡴ࠾ࠤႣ") in line:
                    port = line.split(bstack11ll111_opy_ (u"ࠦࡵࡵࡲࡵ࠿ࠥႤ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll111_opy_ (u"ࠧࡶ࡯ࡳࡶ࠽ࠦႥ") + str(port) + bstack11ll111_opy_ (u"ࠨࠢႦ"))
                    continue
                if line.strip() == bstack1lll1l11l11_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11ll111_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡉࡐࡡࡖࡘࡗࡋࡁࡎࠤႧ"), bstack11ll111_opy_ (u"ࠣ࠳ࠥႨ")) == bstack11ll111_opy_ (u"ࠤ࠴ࠦႩ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lll1ll11l1_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳ࠼ࠣࠦႪ") + str(e) + bstack11ll111_opy_ (u"ࠦࠧႫ"))
        return False
    @measure(event_name=EVENTS.bstack1lllll11111_opy_, stage=STAGE.bstack111lllll_opy_)
    def __1lllll1ll1l_opy_(self):
        if self.bstack1lll1l1llll_opy_:
            self.bstack1111l11l1l_opy_.stop()
            start = datetime.now()
            if self.bstack1lll1l1ll1l_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lllll111ll_opy_:
                    self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠧࡹࡴࡰࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤႬ"), datetime.now() - start)
                else:
                    self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠨࡳࡵࡱࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥႭ"), datetime.now() - start)
            self.__1lll111ll1l_opy_()
            start = datetime.now()
            self.bstack1lll1l1llll_opy_.close()
            self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠢࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤႮ"), datetime.now() - start)
            self.bstack1lll1l1llll_opy_ = None
        if self.process:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡵࡷࡳࡵࠨႯ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠤ࡮࡭ࡱࡲ࡟ࡵ࡫ࡰࡩࠧႰ"), datetime.now() - start)
            self.process = None
            if self.bstack1llllll1111_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1ll11l1ll1_opy_()
                self.logger.info(
                    bstack11ll111_opy_ (u"࡚ࠥ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳࠨႱ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11ll111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪႲ")] = self.config_testhub.build_hashed_id
        self.bstack1lll1ll11l1_opy_ = False
    def __1llll11l111_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11ll111_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢႳ")] = selenium.__version__
            data.frameworks.append(bstack11ll111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣႴ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11ll111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦႵ")] = __version__
            data.frameworks.append(bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧႶ"))
        except:
            pass
    def bstack1llll11l1l1_opy_(self, hub_url: str, platform_index: int, bstack11l11l1l1_opy_: Any):
        if self.bstack1lllllll1l1_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡶࡩࡱ࡫࡮ࡪࡷࡰ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡳࡦࡶࠣࡹࡵࠨႷ"))
            return
        try:
            bstack11ll1lll1l_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11ll111_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧႸ")
            self.bstack1lllllll1l1_opy_ = bstack1llll1llll1_opy_(
                hub_url,
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lll1lll111_opy_={bstack11ll111_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤ࡬ࡲࡰ࡯ࡢࡧࡦࡶࡳࠣႹ"): bstack11l11l1l1_opy_}
            )
            def bstack1lll11l1111_opy_(self):
                return
            if self.config.get(bstack11ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠢႺ"), True):
                Service.start = bstack1lll11l1111_opy_
                Service.stop = bstack1lll11l1111_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.upload_attachment = staticmethod(bstack11l1llllll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll11ll1ll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢႻ"), datetime.now() - bstack11ll1lll1l_opy_)
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡶࡩࡱ࡫࡮ࡪࡷࡰ࠾ࠥࠨႼ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤႽ"))
    def bstack1ll1llll1ll_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1l1l1lll1_opy_
            self.bstack1lllllll1l1_opy_ = bstack1lllll1lll1_opy_(
                platform_index,
                framework_name=bstack11ll111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨႾ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠼ࠣࠦႿ") + str(e) + bstack11ll111_opy_ (u"ࠦࠧჀ"))
            pass
    def bstack1lll11111l1_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡶࡹࡵࡧࡶࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢჁ"))
            return
        if bstack1ll1l1lll_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨჂ"): pytest.__version__ }, [bstack11ll111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦჃ")], self.bstack1111l11l1l_opy_, self.bstack1lll11111ll_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1llll1l1ll1_opy_({ bstack11ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣჄ"): pytest.__version__ }, [bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤჅ")], self.bstack1111l11l1l_opy_, self.bstack1lll11111ll_opy_)
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡹࡵࡧࡶࡸ࠿ࠦࠢ჆") + str(e) + bstack11ll111_opy_ (u"ࠦࠧჇ"))
        self.bstack1lll1llllll_opy_()
    def bstack1lll1llllll_opy_(self):
        if not self.bstack111l11lll_opy_():
            return
        bstack1l1ll1ll1_opy_ = None
        def bstack1ll1l11ll1_opy_(config, startdir):
            return bstack11ll111_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥ჈").format(bstack11ll111_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ჉"))
        def bstack11l1lll1ll_opy_():
            return
        def bstack11l11l1ll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11ll111_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ჊"):
                return bstack11ll111_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ჋")
            else:
                return bstack1l1ll1ll1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l1ll1ll1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1ll1l11ll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11l1lll1ll_opy_
            Config.getoption = bstack11l11l1ll_opy_
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡵࡥ࡫ࠤࡵࡿࡴࡦࡵࡷࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡦࡰࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠼ࠣࠦ჌") + str(e) + bstack11ll111_opy_ (u"ࠥࠦჍ"))
    def bstack1llll1l11ll_opy_(self):
        bstack1l1111l11l_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1l1111l11l_opy_, dict):
            if cli.config_observability:
                bstack1l1111l11l_opy_.update(
                    {bstack11ll111_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦ჎"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11ll111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣ჏") in accessibility.get(bstack11ll111_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢა"), {}):
                    bstack1llll111l1l_opy_ = accessibility.get(bstack11ll111_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣბ"))
                    bstack1llll111l1l_opy_.update({ bstack11ll111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠤგ"): bstack1llll111l1l_opy_.pop(bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧდ")) })
                bstack1l1111l11l_opy_.update({bstack11ll111_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥე"): accessibility })
        return bstack1l1111l11l_opy_
    @measure(event_name=EVENTS.bstack1ll1llll111_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack1lll1l1ll1l_opy_(self, bstack1lll111l11l_opy_: str = None, bstack1llll1ll11l_opy_: str = None, bstack11lll11lll_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll11111ll_opy_:
            return
        bstack11ll1lll1l_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack11lll11lll_opy_:
            req.bstack11lll11lll_opy_ = bstack11lll11lll_opy_
        if bstack1lll111l11l_opy_:
            req.bstack1lll111l11l_opy_ = bstack1lll111l11l_opy_
        if bstack1llll1ll11l_opy_:
            req.bstack1llll1ll11l_opy_ = bstack1llll1ll11l_opy_
        try:
            r = self.bstack1lll11111ll_opy_.StopBinSession(req)
            SDKCLI.bstack1lll1lllll1_opy_ = r.bstack1lll1lllll1_opy_
            SDKCLI.bstack1lll111ll_opy_ = r.bstack1lll111ll_opy_
            self.bstack1l1lll1l1l_opy_(bstack11ll111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡴࡶ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧვ"), datetime.now() - bstack11ll1lll1l_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1l1lll1l1l_opy_(self, key: str, value: timedelta):
        tag = bstack11ll111_opy_ (u"ࠧࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧზ") if self.bstack111l111l1_opy_() else bstack11ll111_opy_ (u"ࠨ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧთ")
        self.bstack1llll11l11l_opy_[bstack11ll111_opy_ (u"ࠢ࠻ࠤი").join([tag + bstack11ll111_opy_ (u"ࠣ࠯ࠥკ") + str(id(self)), key])] += value
    def bstack1ll11l1ll1_opy_(self):
        if not os.getenv(bstack11ll111_opy_ (u"ࠤࡇࡉࡇ࡛ࡇࡠࡒࡈࡖࡋࠨლ"), bstack11ll111_opy_ (u"ࠥ࠴ࠧმ")) == bstack11ll111_opy_ (u"ࠦ࠶ࠨნ"):
            return
        bstack1lll11l11l1_opy_ = dict()
        bstack11111111l1_opy_ = []
        if self.test_framework:
            bstack11111111l1_opy_.extend(list(self.test_framework.bstack11111111l1_opy_.values()))
        if self.bstack1lllllll1l1_opy_:
            bstack11111111l1_opy_.extend(list(self.bstack1lllllll1l1_opy_.bstack11111111l1_opy_.values()))
        for instance in bstack11111111l1_opy_:
            if not instance.platform_index in bstack1lll11l11l1_opy_:
                bstack1lll11l11l1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll11l11l1_opy_[instance.platform_index]
            for k, v in instance.bstack1lll111l1l1_opy_().items():
                report[k] += v
                report[k.split(bstack11ll111_opy_ (u"ࠧࡀࠢო"))[0]] += v
        bstack1lllll1ll11_opy_ = sorted([(k, v) for k, v in self.bstack1llll11l11l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1lll11l1ll1_opy_ = 0
        for r in bstack1lllll1ll11_opy_:
            bstack1lll11lll1l_opy_ = r[1].total_seconds()
            bstack1lll11l1ll1_opy_ += bstack1lll11lll1l_opy_
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡿࡷࡡ࠰࡞ࡿࡀࠦპ") + str(bstack1lll11lll1l_opy_) + bstack11ll111_opy_ (u"ࠢࠣჟ"))
        self.logger.debug(bstack11ll111_opy_ (u"ࠣ࠯࠰ࠦრ"))
        bstack1lllll11l11_opy_ = []
        for platform_index, report in bstack1lll11l11l1_opy_.items():
            bstack1lllll11l11_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lllll11l11_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1ll11ll1l_opy_ = set()
        bstack1llll1l1l1l_opy_ = 0
        for r in bstack1lllll11l11_opy_:
            bstack1lll11lll1l_opy_ = r[2].total_seconds()
            bstack1llll1l1l1l_opy_ += bstack1lll11lll1l_opy_
            bstack1ll11ll1l_opy_.add(r[0])
            self.logger.debug(bstack11ll111_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࡾࡶࡠ࠶࡝ࡾ࠼ࡾࡶࡠ࠷࡝ࡾ࠿ࠥს") + str(bstack1lll11lll1l_opy_) + bstack11ll111_opy_ (u"ࠥࠦტ"))
        if self.bstack111l111l1_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠦ࠲࠳ࠢუ"))
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠿ࡾࡸࡴࡺࡡ࡭ࡡࡦࡰ࡮ࢃࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡳ࠮ࡽࡶࡸࡷ࠮ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠫࢀࡁࠧფ") + str(bstack1llll1l1l1l_opy_) + bstack11ll111_opy_ (u"ࠨࠢქ"))
        else:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࡀࠦღ") + str(bstack1lll11l1ll1_opy_) + bstack11ll111_opy_ (u"ࠣࠤყ"))
        self.logger.debug(bstack11ll111_opy_ (u"ࠤ࠰࠱ࠧშ"))
    def bstack1lll1ll1111_opy_(self, r):
        if r is not None and getattr(r, bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࠫჩ"), None) and getattr(r.testhub, bstack11ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫც"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11ll111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦძ")))
            for bstack1lll1111l11_opy_, err in errors.items():
                if err[bstack11ll111_opy_ (u"࠭ࡴࡺࡲࡨࠫწ")] == bstack11ll111_opy_ (u"ࠧࡪࡰࡩࡳࠬჭ"):
                    self.logger.info(err[bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩხ")])
                else:
                    self.logger.error(err[bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪჯ")])
    def bstack1llll1l11l_opy_(self):
        return SDKCLI.bstack1lll1lllll1_opy_, SDKCLI.bstack1lll111ll_opy_
cli = SDKCLI()