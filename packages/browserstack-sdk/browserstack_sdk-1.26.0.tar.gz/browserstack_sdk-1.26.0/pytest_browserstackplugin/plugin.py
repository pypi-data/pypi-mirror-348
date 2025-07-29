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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l1l11llll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1llll1111l_opy_, bstack11l1lll1l1_opy_, update, bstack11l11l1l1_opy_,
                                       bstack1ll1l11ll1_opy_, bstack11l1lll1ll_opy_, bstack1l1l11l1l_opy_, bstack11lllllll_opy_,
                                       bstack11l1ll1l1l_opy_, bstack11l1l1ll11_opy_, bstack1l1l1111l1_opy_, bstack1l11111l1_opy_,
                                       bstack11llllll1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11lllll11_opy_)
from browserstack_sdk.bstack1l11lll1ll_opy_ import bstack1lll1111l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1l1ll11l_opy_
from bstack_utils.capture import bstack111llll111_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11111lll1_opy_, bstack1l111ll1l1_opy_, bstack1l11111ll_opy_, \
    bstack1lll11llll_opy_
from bstack_utils.helper import bstack1lll1ll1ll_opy_, bstack11ll111l1l1_opy_, bstack111l11l1l1_opy_, bstack111111l11_opy_, bstack1l1ll1ll1l1_opy_, bstack1l1l1llll_opy_, \
    bstack11l1l1l11ll_opy_, \
    bstack11ll111ll1l_opy_, bstack1l111l11l_opy_, bstack11l1lll11l_opy_, bstack11l1l1ll11l_opy_, bstack1ll1l1lll_opy_, Notset, \
    bstack1l1lll111_opy_, bstack11ll11l1l11_opy_, bstack11l1l11ll11_opy_, Result, bstack11ll11l1111_opy_, bstack11l1l111ll1_opy_, bstack111l1ll11l_opy_, \
    bstack1lll1l11_opy_, bstack1111lll1_opy_, bstack11lll11ll_opy_, bstack11l1l1l1l11_opy_
from bstack_utils.bstack11l11l1ll11_opy_ import bstack11l11l1llll_opy_
from bstack_utils.messages import bstack1l111l1ll1_opy_, bstack1l1lllllll_opy_, bstack11l11lll11_opy_, bstack11l1l11l1_opy_, bstack1l11lll11l_opy_, \
    bstack11lll1llll_opy_, bstack11lll1l111_opy_, bstack1ll11l1l11_opy_, bstack1l1l1l1l1_opy_, bstack1ll11lll_opy_, \
    bstack11ll11l1l_opy_, bstack111lll11l_opy_
from bstack_utils.proxy import bstack111111lll_opy_, bstack111111l1_opy_
from bstack_utils.bstack1l1lll1111_opy_ import bstack111l1l11111_opy_, bstack111l11lll11_opy_, bstack111l1l111l1_opy_, bstack111l11ll111_opy_, \
    bstack111l11ll1ll_opy_, bstack111l11l1ll1_opy_, bstack111l11ll11l_opy_, bstack1l111lll1_opy_, bstack111l11ll1l1_opy_
from bstack_utils.bstack1111ll11l_opy_ import bstack1ll11ll11l_opy_
from bstack_utils.bstack1l11lll1l_opy_ import bstack111l1111_opy_, bstack1ll111lll1_opy_, bstack1ll1111l_opy_, \
    bstack1l1l1ll1l_opy_, bstack11111ll11_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack11l1111l1l_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11ll11ll11_opy_
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack111ll11ll_opy_
from bstack_utils.bstack1l11ll111l_opy_ import bstack1l11ll111l_opy_
from browserstack_sdk.__init__ import bstack11l1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll11llll_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll1_opy_ import bstack1l1lllll1_opy_, bstack1l111l11_opy_, bstack1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11l1l11ll_opy_, bstack1lllll1l11l_opy_, bstack1ll1lll1ll1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l1lllll1_opy_ import bstack1l1lllll1_opy_, bstack1l111l11_opy_, bstack1ll1ll1l_opy_
bstack11l1l1111_opy_ = None
bstack1ll1lll111_opy_ = None
bstack1llll11l_opy_ = None
bstack11l11l11_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack11l11l1l_opy_ = None
bstack1ll111ll_opy_ = None
bstack1111l1lll_opy_ = None
bstack1ll1ll1ll_opy_ = None
bstack1lll11l111_opy_ = None
bstack1l1ll1ll1_opy_ = None
bstack1lll111l_opy_ = None
bstack1111lll1l_opy_ = None
bstack111lll1l_opy_ = bstack11ll111_opy_ (u"ࠫࠬᾋ")
CONFIG = {}
bstack11l1ll11_opy_ = False
bstack11l111llll_opy_ = bstack11ll111_opy_ (u"ࠬ࠭ᾌ")
bstack1l1lll1ll_opy_ = bstack11ll111_opy_ (u"࠭ࠧᾍ")
bstack111l11ll1_opy_ = False
bstack11lll111l_opy_ = []
bstack1l1llllll1_opy_ = bstack11111lll1_opy_
bstack11111l1l1l1_opy_ = bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᾎ")
bstack111l1lll_opy_ = {}
bstack1l1lll1ll1_opy_ = None
bstack11l1111ll_opy_ = False
logger = bstack1l1l1ll11l_opy_.get_logger(__name__, bstack1l1llllll1_opy_)
store = {
    bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᾏ"): []
}
bstack11111ll11l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l11l1ll_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11l1l11ll_opy_(
    test_framework_name=bstack1ll1111l11_opy_[bstack11ll111_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ᾐ")] if bstack1ll1l1lll_opy_() else bstack1ll1111l11_opy_[bstack11ll111_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࠪᾑ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11l111111_opy_(page, bstack1111l111_opy_):
    try:
        page.evaluate(bstack11ll111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᾒ"),
                      bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩᾓ") + json.dumps(
                          bstack1111l111_opy_) + bstack11ll111_opy_ (u"ࠨࡽࡾࠤᾔ"))
    except Exception as e:
        print(bstack11ll111_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧᾕ"), e)
def bstack1l1ll1l11_opy_(page, message, level):
    try:
        page.evaluate(bstack11ll111_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᾖ"), bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧᾗ") + json.dumps(
            message) + bstack11ll111_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭ᾘ") + json.dumps(level) + bstack11ll111_opy_ (u"ࠫࢂࢃࠧᾙ"))
    except Exception as e:
        print(bstack11ll111_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣᾚ"), e)
def pytest_configure(config):
    global bstack11l111llll_opy_
    global CONFIG
    bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
    config.args = bstack11ll11ll11_opy_.bstack1111l1111l1_opy_(config.args)
    bstack11lll1l1l_opy_.bstack11l1ll1l1_opy_(bstack11lll11ll_opy_(config.getoption(bstack11ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᾛ"))))
    try:
        bstack1l1l1ll11l_opy_.bstack11l1111l1ll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1l1lllll1_opy_.invoke(bstack1l111l11_opy_.CONNECT, bstack1ll1ll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᾜ"), bstack11ll111_opy_ (u"ࠨ࠲ࠪᾝ")))
        config = json.loads(os.environ.get(bstack11ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠣᾞ"), bstack11ll111_opy_ (u"ࠥࡿࢂࠨᾟ")))
        cli.bstack1llll11l1l1_opy_(bstack11l1lll11l_opy_(bstack11l111llll_opy_, CONFIG), cli_context.platform_index, bstack11l11l1l1_opy_)
    if cli.bstack1lllll11l1l_opy_(bstack1lll1ll1lll_opy_):
        cli.bstack1lll11111l1_opy_()
        logger.debug(bstack11ll111_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᾠ") + str(cli_context.platform_index) + bstack11ll111_opy_ (u"ࠧࠨᾡ"))
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.BEFORE_ALL, bstack1ll1lll1ll1_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11ll111_opy_ (u"ࠨࡷࡩࡧࡱࠦᾢ"), None)
    if cli.is_running() and when == bstack11ll111_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᾣ"):
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.LOG_REPORT, bstack1ll1lll1ll1_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᾤ"):
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.BEFORE_EACH, bstack1ll1lll1ll1_opy_.POST, item, call, outcome)
        elif when == bstack11ll111_opy_ (u"ࠤࡦࡥࡱࡲࠢᾥ"):
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.LOG_REPORT, bstack1ll1lll1ll1_opy_.POST, item, call, outcome)
        elif when == bstack11ll111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᾦ"):
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.AFTER_EACH, bstack1ll1lll1ll1_opy_.POST, item, call, outcome)
        return # skip all existing bstack11111l1ll1l_opy_
    skipSessionName = item.config.getoption(bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᾧ"))
    plugins = item.config.getoption(bstack11ll111_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨᾨ"))
    report = outcome.get_result()
    bstack11111lll11l_opy_(item, call, report)
    if bstack11ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦᾩ") not in plugins or bstack1ll1l1lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack11ll111_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣᾪ"), None)
    page = getattr(item, bstack11ll111_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢᾫ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack11111l1ll11_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack11111l1llll_opy_(item, report, summary, skipSessionName)
def bstack11111l1ll11_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᾬ") and report.skipped:
        bstack111l11ll1l1_opy_(report)
    if report.when in [bstack11ll111_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᾭ"), bstack11ll111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᾮ")]:
        return
    if not bstack1l1ll1ll1l1_opy_():
        return
    try:
        if (str(skipSessionName).lower() != bstack11ll111_opy_ (u"ࠬࡺࡲࡶࡧࠪᾯ") and not cli.is_running()):
            item._driver.execute_script(
                bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫᾰ") + json.dumps(
                    report.nodeid) + bstack11ll111_opy_ (u"ࠧࡾࡿࠪᾱ"))
        os.environ[bstack11ll111_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᾲ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11ll111_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤᾳ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll111_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᾴ")))
    bstack1lll1111ll_opy_ = bstack11ll111_opy_ (u"ࠦࠧ᾵")
    bstack111l11ll1l1_opy_(report)
    if not passed:
        try:
            bstack1lll1111ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11ll111_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᾶ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1111ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11ll111_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᾷ")))
        bstack1lll1111ll_opy_ = bstack11ll111_opy_ (u"ࠢࠣᾸ")
        if not passed:
            try:
                bstack1lll1111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll111_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᾹ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1111ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭Ὰ")
                    + json.dumps(bstack11ll111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦΆ"))
                    + bstack11ll111_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᾼ")
                )
            else:
                item._driver.execute_script(
                    bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪ᾽")
                    + json.dumps(str(bstack1lll1111ll_opy_))
                    + bstack11ll111_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤι")
                )
        except Exception as e:
            summary.append(bstack11ll111_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧ᾿").format(e))
def bstack11111ll111l_opy_(test_name, error_message):
    try:
        bstack11111ll1lll_opy_ = []
        bstack11l1l111ll_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ῀"), bstack11ll111_opy_ (u"ࠩ࠳ࠫ῁"))
        bstack11llll11ll_opy_ = {bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨῂ"): test_name, bstack11ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪῃ"): error_message, bstack11ll111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫῄ"): bstack11l1l111ll_opy_}
        bstack11111l1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ῅"))
        if os.path.exists(bstack11111l1l11l_opy_):
            with open(bstack11111l1l11l_opy_) as f:
                bstack11111ll1lll_opy_ = json.load(f)
        bstack11111ll1lll_opy_.append(bstack11llll11ll_opy_)
        with open(bstack11111l1l11l_opy_, bstack11ll111_opy_ (u"ࠧࡸࠩῆ")) as f:
            json.dump(bstack11111ll1lll_opy_, f)
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ῇ") + str(e))
def bstack11111l1llll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11ll111_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣῈ"), bstack11ll111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧΈ")]:
        return
    if (str(skipSessionName).lower() != bstack11ll111_opy_ (u"ࠫࡹࡸࡵࡦࠩῊ")):
        bstack11l111111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll111_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢΉ")))
    bstack1lll1111ll_opy_ = bstack11ll111_opy_ (u"ࠨࠢῌ")
    bstack111l11ll1l1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll1111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll111_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢ῍").format(e)
                )
        try:
            if passed:
                bstack11111ll11_opy_(getattr(item, bstack11ll111_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ῎"), None), bstack11ll111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ῏"))
            else:
                error_message = bstack11ll111_opy_ (u"ࠪࠫῐ")
                if bstack1lll1111ll_opy_:
                    bstack1l1ll1l11_opy_(item._page, str(bstack1lll1111ll_opy_), bstack11ll111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥῑ"))
                    bstack11111ll11_opy_(getattr(item, bstack11ll111_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫῒ"), None), bstack11ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨΐ"), str(bstack1lll1111ll_opy_))
                    error_message = str(bstack1lll1111ll_opy_)
                else:
                    bstack11111ll11_opy_(getattr(item, bstack11ll111_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭῔"), None), bstack11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ῕"))
                bstack11111ll111l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11ll111_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨῖ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11ll111_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢῗ"), default=bstack11ll111_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥῘ"), help=bstack11ll111_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦῙ"))
    parser.addoption(bstack11ll111_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧῚ"), default=bstack11ll111_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨΊ"), help=bstack11ll111_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ῜"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11ll111_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦ῝"), action=bstack11ll111_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤ῞"), default=bstack11ll111_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦ῟"),
                         help=bstack11ll111_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦῠ"))
def bstack111llll1l1_opy_(log):
    if not (log[bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧῡ")] and log[bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨῢ")].strip()):
        return
    active = bstack111lllll11_opy_()
    log = {
        bstack11ll111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧΰ"): log[bstack11ll111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨῤ")],
        bstack11ll111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ῥ"): bstack111l11l1l1_opy_().isoformat() + bstack11ll111_opy_ (u"ࠫ࡟࠭ῦ"),
        bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ῧ"): log[bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧῨ")],
    }
    if active:
        if active[bstack11ll111_opy_ (u"ࠧࡵࡻࡳࡩࠬῩ")] == bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰ࠭Ὺ"):
            log[bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩΎ")] = active[bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪῬ")]
        elif active[bstack11ll111_opy_ (u"ࠫࡹࡿࡰࡦࠩ῭")] == bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࠪ΅"):
            log[bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭`")] = active[bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ῰")]
    bstack111ll11ll_opy_.bstack1l1ll1l111_opy_([log])
def bstack111lllll11_opy_():
    if len(store[bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ῱")]) > 0 and store[bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ῲ")][-1]:
        return {
            bstack11ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨῳ"): bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩῴ"),
            bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ῵"): store[bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪῶ")][-1]
        }
    if store.get(bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫῷ"), None):
        return {
            bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭Ὸ"): bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺࠧΌ"),
            bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪῺ"): store[bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨΏ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.INIT_TEST, bstack1ll1lll1ll1_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.INIT_TEST, bstack1ll1lll1ll1_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._11111llll11_opy_ = True
        bstack1lll1llll1_opy_ = bstack1ll11llll1_opy_.bstack11ll1l11ll_opy_(bstack11ll111ll1l_opy_(item.own_markers))
        if not cli.bstack1lllll11l1l_opy_(bstack1lll1ll1lll_opy_):
            item._a11y_test_case = bstack1lll1llll1_opy_
            if bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫῼ"), None):
                driver = getattr(item, bstack11ll111_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ´"), None)
                item._a11y_started = bstack1ll11llll1_opy_.bstack1l1l1ll111_opy_(driver, bstack1lll1llll1_opy_)
        if not bstack111ll11ll_opy_.on() or bstack11111l1l1l1_opy_ != bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ῾"):
            return
        global current_test_uuid #, bstack111lll1l1l_opy_
        bstack111l111ll1_opy_ = {
            bstack11ll111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭῿"): uuid4().__str__(),
            bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ "): bstack111l11l1l1_opy_().isoformat() + bstack11ll111_opy_ (u"ࠪ࡞ࠬ ")
        }
        current_test_uuid = bstack111l111ll1_opy_[bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩ ")]
        store[bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ ")] = bstack111l111ll1_opy_[bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l11l1ll_opy_[item.nodeid] = {**_111l11l1ll_opy_[item.nodeid], **bstack111l111ll1_opy_}
        bstack11111l1111l_opy_(item, _111l11l1ll_opy_[item.nodeid], bstack11ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ "))
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪ "), str(err))
def pytest_runtest_setup(item):
    store[bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ ")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.BEFORE_EACH, bstack1ll1lll1ll1_opy_.PRE, item, bstack11ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ "))
        return # skip all existing bstack11111l1ll1l_opy_
    global bstack11111ll11l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1l1ll11l_opy_():
        atexit.register(bstack1ll1llll1_opy_)
        if not bstack11111ll11l1_opy_:
            try:
                bstack11111l1l111_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1l1l1l11_opy_():
                    bstack11111l1l111_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111l1l111_opy_:
                    signal.signal(s, bstack11111l11ll1_opy_)
                bstack11111ll11l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡩ࡬ࡷࡹ࡫ࡲࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡪࡤࡲࡩࡲࡥࡳࡵ࠽ࠤࠧ ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l11111_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ ")
    try:
        if not bstack111ll11ll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l111ll1_opy_ = {
            bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ​"): uuid,
            bstack11ll111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ‌"): bstack111l11l1l1_opy_().isoformat() + bstack11ll111_opy_ (u"ࠨ࡜ࠪ‍"),
            bstack11ll111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ‎"): bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ‏"),
            bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ‐"): bstack11ll111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ‑"),
            bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ‒"): bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭–")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ—")] = item
        store[bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭―")] = [uuid]
        if not _111l11l1ll_opy_.get(item.nodeid, None):
            _111l11l1ll_opy_[item.nodeid] = {bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ‖"): [], bstack11ll111_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭‗"): []}
        _111l11l1ll_opy_[item.nodeid][bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ‘")].append(bstack111l111ll1_opy_[bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ’")])
        _111l11l1ll_opy_[item.nodeid + bstack11ll111_opy_ (u"ࠧ࠮ࡵࡨࡸࡺࡶࠧ‚")] = bstack111l111ll1_opy_
        bstack11111llll1l_opy_(item, bstack111l111ll1_opy_, bstack11ll111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ‛"))
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ“"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.AFTER_EACH, bstack1ll1lll1ll1_opy_.PRE, item, bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ”"))
        return # skip all existing bstack11111l1ll1l_opy_
    try:
        global bstack111l1lll_opy_
        bstack11l1l111ll_opy_ = 0
        if bstack111l11ll1_opy_ is True:
            bstack11l1l111ll_opy_ = int(os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ„")))
        if bstack1l11l1llll_opy_.bstack11l1l111_opy_() == bstack11ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥ‟"):
            if bstack1l11l1llll_opy_.bstack1llllll1l1_opy_() == bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ†"):
                bstack11111ll1l11_opy_ = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ‡"), None)
                bstack1111l1l1_opy_ = bstack11111ll1l11_opy_ + bstack11ll111_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦ•")
                driver = getattr(item, bstack11ll111_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ‣"), None)
                bstack1lllll11l1_opy_ = getattr(item, bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨ․"), None)
                bstack1l11lll1l1_opy_ = getattr(item, bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩ‥"), None)
                PercySDK.screenshot(driver, bstack1111l1l1_opy_, bstack1lllll11l1_opy_=bstack1lllll11l1_opy_, bstack1l11lll1l1_opy_=bstack1l11lll1l1_opy_, bstack1l11l11l1_opy_=bstack11l1l111ll_opy_)
        if not cli.bstack1lllll11l1l_opy_(bstack1lll1ll1lll_opy_):
            if getattr(item, bstack11ll111_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬ…"), False):
                bstack1lll1111l_opy_.bstack11ll1111l1_opy_(getattr(item, bstack11ll111_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ‧"), None), bstack111l1lll_opy_, logger, item)
        if not bstack111ll11ll_opy_.on():
            return
        bstack111l111ll1_opy_ = {
            bstack11ll111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ "): uuid4().__str__(),
            bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ "): bstack111l11l1l1_opy_().isoformat() + bstack11ll111_opy_ (u"ࠩ࡝ࠫ‪"),
            bstack11ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨ‫"): bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ‬"),
            bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ‭"): bstack11ll111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ‮"),
            bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ "): bstack11ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ‰")
        }
        _111l11l1ll_opy_[item.nodeid + bstack11ll111_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬ‱")] = bstack111l111ll1_opy_
        bstack11111llll1l_opy_(item, bstack111l111ll1_opy_, bstack11ll111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ′"))
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪ″"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l11ll111_opy_(fixturedef.argname):
        store[bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ‴")] = request.node
    elif bstack111l11ll1ll_opy_(fixturedef.argname):
        store[bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ‵")] = request.node
    if not bstack111ll11ll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.SETUP_FIXTURE, bstack1ll1lll1ll1_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.SETUP_FIXTURE, bstack1ll1lll1ll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111l1ll1l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.SETUP_FIXTURE, bstack1ll1lll1ll1_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.SETUP_FIXTURE, bstack1ll1lll1ll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111l1ll1l_opy_
    try:
        fixture = {
            bstack11ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ‶"): fixturedef.argname,
            bstack11ll111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ‷"): bstack11l1l1l11ll_opy_(outcome),
            bstack11ll111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ‸"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ‹")]
        if not _111l11l1ll_opy_.get(current_test_item.nodeid, None):
            _111l11l1ll_opy_[current_test_item.nodeid] = {bstack11ll111_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭›"): []}
        _111l11l1ll_opy_[current_test_item.nodeid][bstack11ll111_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ※")].append(fixture)
    except Exception as err:
        logger.debug(bstack11ll111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ‼"), str(err))
if bstack1ll1l1lll_opy_() and bstack111ll11ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.STEP, bstack1ll1lll1ll1_opy_.PRE, request, step)
            return
        try:
            _111l11l1ll_opy_[request.node.nodeid][bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ‽")].bstack1l11ll1l11_opy_(id(step))
        except Exception as err:
            print(bstack11ll111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭‾"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.STEP, bstack1ll1lll1ll1_opy_.POST, request, step, exception)
            return
        try:
            _111l11l1ll_opy_[request.node.nodeid][bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ‿")].bstack111lll11l1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11ll111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ⁀"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.STEP, bstack1ll1lll1ll1_opy_.POST, request, step)
            return
        try:
            bstack111llllll1_opy_: bstack11l1111l1l_opy_ = _111l11l1ll_opy_[request.node.nodeid][bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⁁")]
            bstack111llllll1_opy_.bstack111lll11l1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11ll111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩ⁂"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111l1l1l1_opy_
        try:
            if not bstack111ll11ll_opy_.on() or bstack11111l1l1l1_opy_ != bstack11ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⁃"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.TEST, bstack1ll1lll1ll1_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭⁄"), None)
            if not _111l11l1ll_opy_.get(request.node.nodeid, None):
                _111l11l1ll_opy_[request.node.nodeid] = {}
            bstack111llllll1_opy_ = bstack11l1111l1l_opy_.bstack1111lll11l1_opy_(
                scenario, feature, request.node,
                name=bstack111l11l1ll1_opy_(request.node, scenario),
                started_at=bstack1l1l1llll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11ll111_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ⁅"),
                tags=bstack111l11ll11l_opy_(feature, scenario),
                bstack11l111111l_opy_=bstack111ll11ll_opy_.bstack111lllll1l_opy_(driver) if driver and driver.session_id else {}
            )
            _111l11l1ll_opy_[request.node.nodeid][bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⁆")] = bstack111llllll1_opy_
            bstack11111lll111_opy_(bstack111llllll1_opy_.uuid)
            bstack111ll11ll_opy_.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⁇"), bstack111llllll1_opy_)
        except Exception as err:
            print(bstack11ll111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭⁈"), str(err))
def bstack11111l1lll1_opy_(bstack11l111l11l_opy_):
    if bstack11l111l11l_opy_ in store[bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⁉")]:
        store[bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⁊")].remove(bstack11l111l11l_opy_)
def bstack11111lll111_opy_(test_uuid):
    store[bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⁋")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111ll11ll_opy_.bstack1111l1lll11_opy_
def bstack11111lll11l_opy_(item, call, report):
    logger.debug(bstack11ll111_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡳࡶࠪ⁌"))
    global bstack11111l1l1l1_opy_
    bstack1ll1ll1l11_opy_ = bstack1l1l1llll_opy_()
    if hasattr(report, bstack11ll111_opy_ (u"ࠩࡶࡸࡴࡶࠧ⁍")):
        bstack1ll1ll1l11_opy_ = bstack11ll11l1111_opy_(report.stop)
    elif hasattr(report, bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩ⁎")):
        bstack1ll1ll1l11_opy_ = bstack11ll11l1111_opy_(report.start)
    try:
        if getattr(report, bstack11ll111_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⁏"), bstack11ll111_opy_ (u"ࠬ࠭⁐")) == bstack11ll111_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⁑"):
            logger.debug(bstack11ll111_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ⁒").format(getattr(report, bstack11ll111_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⁓"), bstack11ll111_opy_ (u"ࠩࠪ⁔")).__str__(), bstack11111l1l1l1_opy_))
            if bstack11111l1l1l1_opy_ == bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⁕"):
                _111l11l1ll_opy_[item.nodeid][bstack11ll111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁖")] = bstack1ll1ll1l11_opy_
                bstack11111l1111l_opy_(item, _111l11l1ll_opy_[item.nodeid], bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⁗"), report, call)
                store[bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⁘")] = None
            elif bstack11111l1l1l1_opy_ == bstack11ll111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ⁙"):
                bstack111llllll1_opy_ = _111l11l1ll_opy_[item.nodeid][bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⁚")]
                bstack111llllll1_opy_.set(hooks=_111l11l1ll_opy_[item.nodeid].get(bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⁛"), []))
                exception, bstack11l1111111_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l1111111_opy_ = [call.excinfo.exconly(), getattr(report, bstack11ll111_opy_ (u"ࠪࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠩ⁜"), bstack11ll111_opy_ (u"ࠫࠬ⁝"))]
                bstack111llllll1_opy_.stop(time=bstack1ll1ll1l11_opy_, result=Result(result=getattr(report, bstack11ll111_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⁞"), bstack11ll111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ ")), exception=exception, bstack11l1111111_opy_=bstack11l1111111_opy_))
                bstack111ll11ll_opy_.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⁠"), _111l11l1ll_opy_[item.nodeid][bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⁡")])
        elif getattr(report, bstack11ll111_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⁢"), bstack11ll111_opy_ (u"ࠪࠫ⁣")) in [bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⁤"), bstack11ll111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⁥")]:
            logger.debug(bstack11ll111_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ⁦").format(getattr(report, bstack11ll111_opy_ (u"ࠧࡸࡪࡨࡲࠬ⁧"), bstack11ll111_opy_ (u"ࠨࠩ⁨")).__str__(), bstack11111l1l1l1_opy_))
            bstack11l1111ll1_opy_ = item.nodeid + bstack11ll111_opy_ (u"ࠩ࠰ࠫ⁩") + getattr(report, bstack11ll111_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⁪"), bstack11ll111_opy_ (u"ࠫࠬ⁫"))
            if getattr(report, bstack11ll111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⁬"), False):
                hook_type = bstack11ll111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⁭") if getattr(report, bstack11ll111_opy_ (u"ࠧࡸࡪࡨࡲࠬ⁮"), bstack11ll111_opy_ (u"ࠨࠩ⁯")) == bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⁰") else bstack11ll111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧⁱ")
                _111l11l1ll_opy_[bstack11l1111ll1_opy_] = {
                    bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩ⁲"): uuid4().__str__(),
                    bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⁳"): bstack1ll1ll1l11_opy_,
                    bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⁴"): hook_type
                }
            _111l11l1ll_opy_[bstack11l1111ll1_opy_][bstack11ll111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⁵")] = bstack1ll1ll1l11_opy_
            bstack11111l1lll1_opy_(_111l11l1ll_opy_[bstack11l1111ll1_opy_][bstack11ll111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⁶")])
            bstack11111llll1l_opy_(item, _111l11l1ll_opy_[bstack11l1111ll1_opy_], bstack11ll111_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⁷"), report, call)
            if getattr(report, bstack11ll111_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⁸"), bstack11ll111_opy_ (u"ࠫࠬ⁹")) == bstack11ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⁺"):
                if getattr(report, bstack11ll111_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ⁻"), bstack11ll111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⁼")) == bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⁽"):
                    bstack111l111ll1_opy_ = {
                        bstack11ll111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⁾"): uuid4().__str__(),
                        bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧⁿ"): bstack1l1l1llll_opy_(),
                        bstack11ll111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₀"): bstack1l1l1llll_opy_()
                    }
                    _111l11l1ll_opy_[item.nodeid] = {**_111l11l1ll_opy_[item.nodeid], **bstack111l111ll1_opy_}
                    bstack11111l1111l_opy_(item, _111l11l1ll_opy_[item.nodeid], bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭₁"))
                    bstack11111l1111l_opy_(item, _111l11l1ll_opy_[item.nodeid], bstack11ll111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ₂"), report, call)
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬ₃"), str(err))
def bstack11111ll11ll_opy_(test, bstack111l111ll1_opy_, result=None, call=None, bstack11l1llll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111llllll1_opy_ = {
        bstack11ll111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭₄"): bstack111l111ll1_opy_[bstack11ll111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ₅")],
        bstack11ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨ₆"): bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ₇"),
        bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ₈"): test.name,
        bstack11ll111_opy_ (u"࠭ࡢࡰࡦࡼࠫ₉"): {
            bstack11ll111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ₊"): bstack11ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ₋"),
            bstack11ll111_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ₌"): inspect.getsource(test.obj)
        },
        bstack11ll111_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ₍"): test.name,
        bstack11ll111_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ₎"): test.name,
        bstack11ll111_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ₏"): bstack11ll11ll11_opy_.bstack111ll1lll1_opy_(test),
        bstack11ll111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩₐ"): file_path,
        bstack11ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩₑ"): file_path,
        bstack11ll111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨₒ"): bstack11ll111_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪₓ"),
        bstack11ll111_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨₔ"): file_path,
        bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨₕ"): bstack111l111ll1_opy_[bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩₖ")],
        bstack11ll111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩₗ"): bstack11ll111_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧₘ"),
        bstack11ll111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫₙ"): {
            bstack11ll111_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ₚ"): test.nodeid
        },
        bstack11ll111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨₛ"): bstack11ll111ll1l_opy_(test.own_markers)
    }
    if bstack11l1llll1_opy_ in [bstack11ll111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬₜ"), bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ₝")]:
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"࠭࡭ࡦࡶࡤࠫ₞")] = {
            bstack11ll111_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ₟"): bstack111l111ll1_opy_.get(bstack11ll111_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ₠"), [])
        }
    if bstack11l1llll1_opy_ == bstack11ll111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ₡"):
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ₢")] = bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ₣")
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ₤")] = bstack111l111ll1_opy_[bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ₥")]
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ₦")] = bstack111l111ll1_opy_[bstack11ll111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₧")]
    if result:
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ₨")] = result.outcome
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ₩")] = result.duration * 1000
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₪")] = bstack111l111ll1_opy_[bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₫")]
        if result.failed:
            bstack111llllll1_opy_[bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ€")] = bstack111ll11ll_opy_.bstack1111l1l11l_opy_(call.excinfo.typename)
            bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ₭")] = bstack111ll11ll_opy_.bstack1111ll11lll_opy_(call.excinfo, result)
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ₮")] = bstack111l111ll1_opy_[bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ₯")]
    if outcome:
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ₰")] = bstack11l1l1l11ll_opy_(outcome)
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ₱")] = 0
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₲")] = bstack111l111ll1_opy_[bstack11ll111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ₳")]
        if bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ₴")] == bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ₵"):
            bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ₶")] = bstack11ll111_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ₷")  # bstack11111l111ll_opy_
            bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ₸")] = [{bstack11ll111_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ₹"): [bstack11ll111_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ₺")]}]
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭₻")] = bstack111l111ll1_opy_[bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ₼")]
    return bstack111llllll1_opy_
def bstack11111lll1l1_opy_(test, bstack111l1lllll_opy_, bstack11l1llll1_opy_, result, call, outcome, bstack11111ll1l1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1lllll_opy_[bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ₽")]
    hook_name = bstack111l1lllll_opy_[bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭₾")]
    hook_data = {
        bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩ₿"): bstack111l1lllll_opy_[bstack11ll111_opy_ (u"ࠬࡻࡵࡪࡦࠪ⃀")],
        bstack11ll111_opy_ (u"࠭ࡴࡺࡲࡨࠫ⃁"): bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⃂"),
        bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭⃃"): bstack11ll111_opy_ (u"ࠩࡾࢁࠬ⃄").format(bstack111l11lll11_opy_(hook_name)),
        bstack11ll111_opy_ (u"ࠪࡦࡴࡪࡹࠨ⃅"): {
            bstack11ll111_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ⃆"): bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⃇"),
            bstack11ll111_opy_ (u"࠭ࡣࡰࡦࡨࠫ⃈"): None
        },
        bstack11ll111_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭⃉"): test.name,
        bstack11ll111_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ⃊"): bstack11ll11ll11_opy_.bstack111ll1lll1_opy_(test, hook_name),
        bstack11ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ⃋"): file_path,
        bstack11ll111_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ⃌"): file_path,
        bstack11ll111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⃍"): bstack11ll111_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⃎"),
        bstack11ll111_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ⃏"): file_path,
        bstack11ll111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⃐"): bstack111l1lllll_opy_[bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⃑")],
        bstack11ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯⃒ࠬ"): bstack11ll111_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶ⃓ࠬ") if bstack11111l1l1l1_opy_ == bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ⃔") else bstack11ll111_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⃕"),
        bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⃖"): hook_type
    }
    bstack1111ll1lll1_opy_ = bstack111l111lll_opy_(_111l11l1ll_opy_.get(test.nodeid, None))
    if bstack1111ll1lll1_opy_:
        hook_data[bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ⃗")] = bstack1111ll1lll1_opy_
    if result:
        hook_data[bstack11ll111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⃘")] = result.outcome
        hook_data[bstack11ll111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵ⃙ࠪ")] = result.duration * 1000
        hook_data[bstack11ll111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⃚")] = bstack111l1lllll_opy_[bstack11ll111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⃛")]
        if result.failed:
            hook_data[bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⃜")] = bstack111ll11ll_opy_.bstack1111l1l11l_opy_(call.excinfo.typename)
            hook_data[bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⃝")] = bstack111ll11ll_opy_.bstack1111ll11lll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11ll111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⃞")] = bstack11l1l1l11ll_opy_(outcome)
        hook_data[bstack11ll111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⃟")] = 100
        hook_data[bstack11ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⃠")] = bstack111l1lllll_opy_[bstack11ll111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⃡")]
        if hook_data[bstack11ll111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⃢")] == bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⃣"):
            hook_data[bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⃤")] = bstack11ll111_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ⃥")  # bstack11111l111ll_opy_
            hook_data[bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦ⃦ࠩ")] = [{bstack11ll111_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⃧"): [bstack11ll111_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸ⃨ࠧ")]}]
    if bstack11111ll1l1l_opy_:
        hook_data[bstack11ll111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⃩")] = bstack11111ll1l1l_opy_.result
        hook_data[bstack11ll111_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ⃪࠭")] = bstack11ll11l1l11_opy_(bstack111l1lllll_opy_[bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶ⃫ࠪ")], bstack111l1lllll_opy_[bstack11ll111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸ⃬ࠬ")])
        hook_data[bstack11ll111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ⃭࠭")] = bstack111l1lllll_opy_[bstack11ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺ⃮ࠧ")]
        if hook_data[bstack11ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶ⃯ࠪ")] == bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⃰"):
            hook_data[bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⃱")] = bstack111ll11ll_opy_.bstack1111l1l11l_opy_(bstack11111ll1l1l_opy_.exception_type)
            hook_data[bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⃲")] = [{bstack11ll111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⃳"): bstack11l1l11ll11_opy_(bstack11111ll1l1l_opy_.exception)}]
    return hook_data
def bstack11111l1111l_opy_(test, bstack111l111ll1_opy_, bstack11l1llll1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11ll111_opy_ (u"ࠨࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ⃴").format(bstack11l1llll1_opy_))
    bstack111llllll1_opy_ = bstack11111ll11ll_opy_(test, bstack111l111ll1_opy_, result, call, bstack11l1llll1_opy_, outcome)
    driver = getattr(test, bstack11ll111_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⃵"), None)
    if bstack11l1llll1_opy_ == bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⃶") and driver:
        bstack111llllll1_opy_[bstack11ll111_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ⃷")] = bstack111ll11ll_opy_.bstack111lllll1l_opy_(driver)
    if bstack11l1llll1_opy_ == bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⃸"):
        bstack11l1llll1_opy_ = bstack11ll111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⃹")
    bstack111l1ll1l1_opy_ = {
        bstack11ll111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⃺"): bstack11l1llll1_opy_,
        bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⃻"): bstack111llllll1_opy_
    }
    bstack111ll11ll_opy_.bstack1l1111ll1_opy_(bstack111l1ll1l1_opy_)
    if bstack11l1llll1_opy_ == bstack11ll111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⃼"):
        threading.current_thread().bstackTestMeta = {bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⃽"): bstack11ll111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⃾")}
    elif bstack11l1llll1_opy_ == bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⃿"):
        threading.current_thread().bstackTestMeta = {bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭℀"): getattr(result, bstack11ll111_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ℁"), bstack11ll111_opy_ (u"ࠨࠩℂ"))}
def bstack11111llll1l_opy_(test, bstack111l111ll1_opy_, bstack11l1llll1_opy_, result=None, call=None, outcome=None, bstack11111ll1l1l_opy_=None):
    logger.debug(bstack11ll111_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤ࡭ࡵ࡯࡬ࠢࡧࡥࡹࡧࠬࠡࡧࡹࡩࡳࡺࡔࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ℃").format(bstack11l1llll1_opy_))
    hook_data = bstack11111lll1l1_opy_(test, bstack111l111ll1_opy_, bstack11l1llll1_opy_, result, call, outcome, bstack11111ll1l1l_opy_)
    bstack111l1ll1l1_opy_ = {
        bstack11ll111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ℄"): bstack11l1llll1_opy_,
        bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭℅"): hook_data
    }
    bstack111ll11ll_opy_.bstack1l1111ll1_opy_(bstack111l1ll1l1_opy_)
def bstack111l111lll_opy_(bstack111l111ll1_opy_):
    if not bstack111l111ll1_opy_:
        return None
    if bstack111l111ll1_opy_.get(bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ℆"), None):
        return getattr(bstack111l111ll1_opy_[bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩℇ")], bstack11ll111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ℈"), None)
    return bstack111l111ll1_opy_.get(bstack11ll111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭℉"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.LOG, bstack1ll1lll1ll1_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_.LOG, bstack1ll1lll1ll1_opy_.POST, request, caplog)
        return # skip all existing bstack11111l1ll1l_opy_
    try:
        if not bstack111ll11ll_opy_.on():
            return
        places = [bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨℊ"), bstack11ll111_opy_ (u"ࠪࡧࡦࡲ࡬ࠨℋ"), bstack11ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ℌ")]
        logs = []
        for bstack11111ll1111_opy_ in places:
            records = caplog.get_records(bstack11111ll1111_opy_)
            bstack11111l111l1_opy_ = bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬℍ") if bstack11111ll1111_opy_ == bstack11ll111_opy_ (u"࠭ࡣࡢ࡮࡯ࠫℎ") else bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧℏ")
            bstack11111l11l11_opy_ = request.node.nodeid + (bstack11ll111_opy_ (u"ࠨࠩℐ") if bstack11111ll1111_opy_ == bstack11ll111_opy_ (u"ࠩࡦࡥࡱࡲࠧℑ") else bstack11ll111_opy_ (u"ࠪ࠱ࠬℒ") + bstack11111ll1111_opy_)
            test_uuid = bstack111l111lll_opy_(_111l11l1ll_opy_.get(bstack11111l11l11_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l1l111ll1_opy_(record.message):
                    continue
                logs.append({
                    bstack11ll111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧℓ"): bstack11ll111l1l1_opy_(record.created).isoformat() + bstack11ll111_opy_ (u"ࠬࡠࠧ℔"),
                    bstack11ll111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬℕ"): record.levelname,
                    bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ№"): record.message,
                    bstack11111l111l1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111ll11ll_opy_.bstack1l1ll1l111_opy_(logs)
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ℗"), str(err))
def bstack1l11lllll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11l1111ll_opy_
    bstack1l1l111ll1_opy_ = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭℘"), None) and bstack1lll1ll1ll_opy_(
            threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩℙ"), None)
    bstack111l11l11_opy_ = getattr(driver, bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫℚ"), None) != None and getattr(driver, bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬℛ"), None) == True
    if sequence == bstack11ll111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ℜ") and driver != None:
      if not bstack11l1111ll_opy_ and bstack1l1ll1ll1l1_opy_() and bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧℝ") in CONFIG and CONFIG[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ℞")] == True and bstack1l11ll111l_opy_.bstack1ll111l1ll_opy_(driver_command) and (bstack111l11l11_opy_ or bstack1l1l111ll1_opy_) and not bstack11lllll11_opy_(args):
        try:
          bstack11l1111ll_opy_ = True
          logger.debug(bstack11ll111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ℟").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11ll111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨ℠").format(str(err)))
        bstack11l1111ll_opy_ = False
    if sequence == bstack11ll111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ℡"):
        if driver_command == bstack11ll111_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ™"):
            bstack111ll11ll_opy_.bstack11111l1l_opy_({
                bstack11ll111_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ℣"): response[bstack11ll111_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ℤ")],
                bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ℥"): store[bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭Ω")]
            })
def bstack1ll1llll1_opy_():
    global bstack11lll111l_opy_
    bstack1l1l1ll11l_opy_.bstack1l11l1l1l1_opy_()
    logging.shutdown()
    bstack111ll11ll_opy_.bstack111ll1l111_opy_()
    for driver in bstack11lll111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11111l11ll1_opy_(*args):
    global bstack11lll111l_opy_
    bstack111ll11ll_opy_.bstack111ll1l111_opy_()
    for driver in bstack11lll111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11llll1l_opy_, stage=STAGE.bstack111lllll_opy_, bstack11l1l11ll1_opy_=bstack1l1lll1ll1_opy_)
def bstack111l111l_opy_(self, *args, **kwargs):
    bstack1l1111l1_opy_ = bstack11l1l1111_opy_(self, *args, **kwargs)
    bstack11lll1lll_opy_ = getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ℧"), None)
    if bstack11lll1lll_opy_ and bstack11lll1lll_opy_.get(bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫℨ"), bstack11ll111_opy_ (u"ࠬ࠭℩")) == bstack11ll111_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧK"):
        bstack111ll11ll_opy_.bstack1ll1llll_opy_(self)
    return bstack1l1111l1_opy_
@measure(event_name=EVENTS.bstack1ll111l1l_opy_, stage=STAGE.bstack11ll1ll1l_opy_, bstack11l1l11ll1_opy_=bstack1l1lll1ll1_opy_)
def bstack11lll11l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
    if bstack11lll1l1l_opy_.get_property(bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫÅ")):
        return
    bstack11lll1l1l_opy_.bstack1l1lllll11_opy_(bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬℬ"), True)
    global bstack111lll1l_opy_
    global bstack1llll1ll1_opy_
    bstack111lll1l_opy_ = framework_name
    logger.info(bstack111lll11l_opy_.format(bstack111lll1l_opy_.split(bstack11ll111_opy_ (u"ࠩ࠰ࠫℭ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1ll1ll1l1_opy_():
            Service.start = bstack1l1l11l1l_opy_
            Service.stop = bstack11lllllll_opy_
            webdriver.Remote.get = bstack1lll1l11l1_opy_
            webdriver.Remote.__init__ = bstack11l111ll1_opy_
            if not isinstance(os.getenv(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ℮")), str):
                return
            WebDriver.close = bstack11l1ll1l1l_opy_
            WebDriver.quit = bstack11ll11l11_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111ll11ll_opy_.on():
            webdriver.Remote.__init__ = bstack111l111l_opy_
        bstack1llll1ll1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11ll111_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩℯ")):
        bstack1llll1ll1_opy_ = eval(os.environ.get(bstack11ll111_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪℰ")))
    if not bstack1llll1ll1_opy_:
        bstack1l1l1111l1_opy_(bstack11ll111_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣℱ"), bstack11ll11l1l_opy_)
    if bstack11111111l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._111l1ll1_opy_ = bstack1l1l11ll11_opy_
        except Exception as e:
            logger.error(bstack11lll1llll_opy_.format(str(e)))
    if bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧℲ") in str(framework_name).lower():
        if not bstack1l1ll1ll1l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll1l11ll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11l1lll1ll_opy_
            Config.getoption = bstack11l11l1ll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11lll11ll1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll11l1l1_opy_, stage=STAGE.bstack111lllll_opy_, bstack11l1l11ll1_opy_=bstack1l1lll1ll1_opy_)
def bstack11ll11l11_opy_(self):
    global bstack111lll1l_opy_
    global bstack1111llll1_opy_
    global bstack1ll1lll111_opy_
    try:
        if bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨℳ") in bstack111lll1l_opy_ and self.session_id != None and bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ℴ"), bstack11ll111_opy_ (u"ࠪࠫℵ")) != bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬℶ"):
            bstack1lllll1l1_opy_ = bstack11ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬℷ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ℸ")
            bstack1111lll1_opy_(logger, True)
            if self != None:
                bstack1l1l1ll1l_opy_(self, bstack1lllll1l1_opy_, bstack11ll111_opy_ (u"ࠧ࠭ࠢࠪℹ").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lllll11l1l_opy_(bstack1lll1ll1lll_opy_):
            item = store.get(bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ℺"), None)
            if item is not None and bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ℻"), None):
                bstack1lll1111l_opy_.bstack11ll1111l1_opy_(self, bstack111l1lll_opy_, logger, item)
        threading.current_thread().testStatus = bstack11ll111_opy_ (u"ࠪࠫℼ")
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧℽ") + str(e))
    bstack1ll1lll111_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1l1l1l_opy_, stage=STAGE.bstack111lllll_opy_, bstack11l1l11ll1_opy_=bstack1l1lll1ll1_opy_)
def bstack11l111ll1_opy_(self, command_executor,
             desired_capabilities=None, bstack1ll11l1l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1111llll1_opy_
    global bstack1l1lll1ll1_opy_
    global bstack111l11ll1_opy_
    global bstack111lll1l_opy_
    global bstack11l1l1111_opy_
    global bstack11lll111l_opy_
    global bstack11l111llll_opy_
    global bstack1l1lll1ll_opy_
    global bstack111l1lll_opy_
    CONFIG[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧℾ")] = str(bstack111lll1l_opy_) + str(__version__)
    command_executor = bstack11l1lll11l_opy_(bstack11l111llll_opy_, CONFIG)
    logger.debug(bstack11l1l11l1_opy_.format(command_executor))
    proxy = bstack11llllll1_opy_(CONFIG, proxy)
    bstack11l1l111ll_opy_ = 0
    try:
        if bstack111l11ll1_opy_ is True:
            bstack11l1l111ll_opy_ = int(os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ℿ")))
    except:
        bstack11l1l111ll_opy_ = 0
    bstack11ll1111l_opy_ = bstack1llll1111l_opy_(CONFIG, bstack11l1l111ll_opy_)
    logger.debug(bstack1ll11l1l11_opy_.format(str(bstack11ll1111l_opy_)))
    bstack111l1lll_opy_ = CONFIG.get(bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⅀"))[bstack11l1l111ll_opy_]
    if bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⅁") in CONFIG and CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⅂")]:
        bstack1ll1111l_opy_(bstack11ll1111l_opy_, bstack1l1lll1ll_opy_)
    if bstack1ll11llll1_opy_.bstack11lll1l1ll_opy_(CONFIG, bstack11l1l111ll_opy_) and bstack1ll11llll1_opy_.bstack11l1ll1l11_opy_(bstack11ll1111l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lllll11l1l_opy_(bstack1lll1ll1lll_opy_):
            bstack1ll11llll1_opy_.set_capabilities(bstack11ll1111l_opy_, CONFIG)
    if desired_capabilities:
        bstack111ll1l1_opy_ = bstack11l1lll1l1_opy_(desired_capabilities)
        bstack111ll1l1_opy_[bstack11ll111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ⅃")] = bstack1l1lll111_opy_(CONFIG)
        bstack1l1llll111_opy_ = bstack1llll1111l_opy_(bstack111ll1l1_opy_)
        if bstack1l1llll111_opy_:
            bstack11ll1111l_opy_ = update(bstack1l1llll111_opy_, bstack11ll1111l_opy_)
        desired_capabilities = None
    if options:
        bstack11l1l1ll11_opy_(options, bstack11ll1111l_opy_)
    if not options:
        options = bstack11l11l1l1_opy_(bstack11ll1111l_opy_)
    if proxy and bstack1l111l11l_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ⅄")):
        options.proxy(proxy)
    if options and bstack1l111l11l_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫⅅ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l111l11l_opy_() < version.parse(bstack11ll111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬⅆ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11ll1111l_opy_)
    logger.info(bstack11l11lll11_opy_)
    bstack1l1l11llll_opy_.end(EVENTS.bstack1ll111l1l_opy_.value, EVENTS.bstack1ll111l1l_opy_.value + bstack11ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢⅇ"),
                               EVENTS.bstack1ll111l1l_opy_.value + bstack11ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨⅈ"), True, None)
    if bstack1l111l11l_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩⅉ")):
        bstack11l1l1111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111l11l_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⅊")):
        bstack11l1l1111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1ll11l1l_opy_=bstack1ll11l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l111l11l_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ⅋")):
        bstack11l1l1111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll11l1l_opy_=bstack1ll11l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11l1l1111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll11l1l_opy_=bstack1ll11l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l1ll11l1l_opy_ = bstack11ll111_opy_ (u"ࠬ࠭⅌")
        if bstack1l111l11l_opy_() >= version.parse(bstack11ll111_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ⅍")):
            bstack1l1ll11l1l_opy_ = self.caps.get(bstack11ll111_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢⅎ"))
        else:
            bstack1l1ll11l1l_opy_ = self.capabilities.get(bstack11ll111_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ⅏"))
        if bstack1l1ll11l1l_opy_:
            bstack1lll1l11_opy_(bstack1l1ll11l1l_opy_)
            if bstack1l111l11l_opy_() <= version.parse(bstack11ll111_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ⅐")):
                self.command_executor._url = bstack11ll111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⅑") + bstack11l111llll_opy_ + bstack11ll111_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ⅒")
            else:
                self.command_executor._url = bstack11ll111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ⅓") + bstack1l1ll11l1l_opy_ + bstack11ll111_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ⅔")
            logger.debug(bstack1l1lllllll_opy_.format(bstack1l1ll11l1l_opy_))
        else:
            logger.debug(bstack1l111l1ll1_opy_.format(bstack11ll111_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ⅕")))
    except Exception as e:
        logger.debug(bstack1l111l1ll1_opy_.format(e))
    bstack1111llll1_opy_ = self.session_id
    if bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⅖") in bstack111lll1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⅗"), None)
        if item:
            bstack11111ll1ll1_opy_ = getattr(item, bstack11ll111_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ⅘"), False)
            if not getattr(item, bstack11ll111_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⅙"), None) and bstack11111ll1ll1_opy_:
                setattr(store[bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⅚")], bstack11ll111_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⅛"), self)
        bstack11lll1lll_opy_ = getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ⅜"), None)
        if bstack11lll1lll_opy_ and bstack11lll1lll_opy_.get(bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⅝"), bstack11ll111_opy_ (u"ࠩࠪ⅞")) == bstack11ll111_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⅟"):
            bstack111ll11ll_opy_.bstack1ll1llll_opy_(self)
    bstack11lll111l_opy_.append(self)
    if bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧⅠ") in CONFIG and bstack11ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪⅡ") in CONFIG[bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩⅢ")][bstack11l1l111ll_opy_]:
        bstack1l1lll1ll1_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅣ")][bstack11l1l111ll_opy_][bstack11ll111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ⅴ")]
    logger.debug(bstack1ll11lll_opy_.format(bstack1111llll1_opy_))
@measure(event_name=EVENTS.bstack11ll11111l_opy_, stage=STAGE.bstack111lllll_opy_, bstack11l1l11ll1_opy_=bstack1l1lll1ll1_opy_)
def bstack1lll1l11l1_opy_(self, url):
    global bstack1ll1ll1ll_opy_
    global CONFIG
    try:
        bstack1ll111lll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1l1l1l1_opy_.format(str(err)))
    try:
        bstack1ll1ll1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack11lll1l11_opy_ = str(e)
            if any(err_msg in bstack11lll1l11_opy_ for err_msg in bstack1l11111ll_opy_):
                bstack1ll111lll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1l1l1l1_opy_.format(str(err)))
        raise e
def bstack1llll1llll_opy_(item, when):
    global bstack1lll111l_opy_
    try:
        bstack1lll111l_opy_(item, when)
    except Exception as e:
        pass
def bstack11lll11ll1_opy_(item, call, rep):
    global bstack1111lll1l_opy_
    global bstack11lll111l_opy_
    name = bstack11ll111_opy_ (u"ࠩࠪⅥ")
    try:
        if rep.when == bstack11ll111_opy_ (u"ࠪࡧࡦࡲ࡬ࠨⅦ"):
            bstack1111llll1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ⅷ"))
            try:
                if (str(skipSessionName).lower() != bstack11ll111_opy_ (u"ࠬࡺࡲࡶࡧࠪⅨ")):
                    name = str(rep.nodeid)
                    bstack1ll1l1ll_opy_ = bstack111l1111_opy_(bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧⅩ"), name, bstack11ll111_opy_ (u"ࠧࠨⅪ"), bstack11ll111_opy_ (u"ࠨࠩⅫ"), bstack11ll111_opy_ (u"ࠩࠪⅬ"), bstack11ll111_opy_ (u"ࠪࠫⅭ"))
                    os.environ[bstack11ll111_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧⅮ")] = name
                    for driver in bstack11lll111l_opy_:
                        if bstack1111llll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll1l1ll_opy_)
            except Exception as e:
                logger.debug(bstack11ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬⅯ").format(str(e)))
            try:
                bstack1l111lll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧⅰ"):
                    status = bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧⅱ") if rep.outcome.lower() == bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨⅲ") else bstack11ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩⅳ")
                    reason = bstack11ll111_opy_ (u"ࠪࠫⅴ")
                    if status == bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫⅵ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11ll111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪⅶ") if status == bstack11ll111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ⅷ") else bstack11ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ⅸ")
                    data = name + bstack11ll111_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪⅹ") if status == bstack11ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩⅺ") else name + bstack11ll111_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ⅻ") + reason
                    bstack1lll1l111_opy_ = bstack111l1111_opy_(bstack11ll111_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ⅼ"), bstack11ll111_opy_ (u"ࠬ࠭ⅽ"), bstack11ll111_opy_ (u"࠭ࠧⅾ"), bstack11ll111_opy_ (u"ࠧࠨⅿ"), level, data)
                    for driver in bstack11lll111l_opy_:
                        if bstack1111llll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll1l111_opy_)
            except Exception as e:
                logger.debug(bstack11ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬↀ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ↁ").format(str(e)))
    bstack1111lll1l_opy_(item, call, rep)
notset = Notset()
def bstack11l11l1ll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1ll1ll1_opy_
    if str(name).lower() == bstack11ll111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪↂ"):
        return bstack11ll111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥↃ")
    else:
        return bstack1l1ll1ll1_opy_(self, name, default, skip)
def bstack1l1l11ll11_opy_(self):
    global CONFIG
    global bstack1ll111ll_opy_
    try:
        proxy = bstack111111lll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11ll111_opy_ (u"ࠬ࠴ࡰࡢࡥࠪↄ")):
                proxies = bstack111111l1_opy_(proxy, bstack11l1lll11l_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1lll1l1_opy_ = proxies.popitem()
                    if bstack11ll111_opy_ (u"ࠨ࠺࠰࠱ࠥↅ") in bstack1ll1lll1l1_opy_:
                        return bstack1ll1lll1l1_opy_
                    else:
                        return bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣↆ") + bstack1ll1lll1l1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧↇ").format(str(e)))
    return bstack1ll111ll_opy_(self)
def bstack11111111l_opy_():
    return (bstack11ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬↈ") in CONFIG or bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ↉") in CONFIG) and bstack111111l11_opy_() and bstack1l111l11l_opy_() >= version.parse(
        bstack1l111ll1l1_opy_)
def bstack11111ll1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1lll1ll1_opy_
    global bstack111l11ll1_opy_
    global bstack111lll1l_opy_
    CONFIG[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭↊")] = str(bstack111lll1l_opy_) + str(__version__)
    bstack11l1l111ll_opy_ = 0
    try:
        if bstack111l11ll1_opy_ is True:
            bstack11l1l111ll_opy_ = int(os.environ.get(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ↋")))
    except:
        bstack11l1l111ll_opy_ = 0
    CONFIG[bstack11ll111_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ↌")] = True
    bstack11ll1111l_opy_ = bstack1llll1111l_opy_(CONFIG, bstack11l1l111ll_opy_)
    logger.debug(bstack1ll11l1l11_opy_.format(str(bstack11ll1111l_opy_)))
    if CONFIG.get(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ↍")):
        bstack1ll1111l_opy_(bstack11ll1111l_opy_, bstack1l1lll1ll_opy_)
    if bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ↎") in CONFIG and bstack11ll111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ↏") in CONFIG[bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭←")][bstack11l1l111ll_opy_]:
        bstack1l1lll1ll1_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ↑")][bstack11l1l111ll_opy_][bstack11ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ→")]
    import urllib
    import json
    if bstack11ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ↓") in CONFIG and str(CONFIG[bstack11ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ↔")]).lower() != bstack11ll111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ↕"):
        bstack11ll1ll1l1_opy_ = bstack11l1llll1l_opy_()
        bstack11l1111l_opy_ = bstack11ll1ll1l1_opy_ + urllib.parse.quote(json.dumps(bstack11ll1111l_opy_))
    else:
        bstack11l1111l_opy_ = bstack11ll111_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ↖") + urllib.parse.quote(json.dumps(bstack11ll1111l_opy_))
    browser = self.connect(bstack11l1111l_opy_)
    return browser
def bstack11llllllll_opy_():
    global bstack1llll1ll1_opy_
    global bstack111lll1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l1lll1_opy_
        if not bstack1l1ll1ll1l1_opy_():
            global bstack1l1lll111l_opy_
            if not bstack1l1lll111l_opy_:
                from bstack_utils.helper import bstack1lll111lll_opy_, bstack1llll111_opy_
                bstack1l1lll111l_opy_ = bstack1lll111lll_opy_()
                bstack1llll111_opy_(bstack111lll1l_opy_)
            BrowserType.connect = bstack1l1l1lll1_opy_
            return
        BrowserType.launch = bstack11111ll1_opy_
        bstack1llll1ll1_opy_ = True
    except Exception as e:
        pass
def bstack11111lllll1_opy_():
    global CONFIG
    global bstack11l1ll11_opy_
    global bstack11l111llll_opy_
    global bstack1l1lll1ll_opy_
    global bstack111l11ll1_opy_
    global bstack1l1llllll1_opy_
    CONFIG = json.loads(os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ↗")))
    bstack11l1ll11_opy_ = eval(os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ↘")))
    bstack11l111llll_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ↙"))
    bstack1l11111l1_opy_(CONFIG, bstack11l1ll11_opy_)
    bstack1l1llllll1_opy_ = bstack1l1l1ll11l_opy_.bstack1lllllll1_opy_(CONFIG, bstack1l1llllll1_opy_)
    if cli.bstack111l111l1_opy_():
        bstack1l1lllll1_opy_.invoke(bstack1l111l11_opy_.CONNECT, bstack1ll1ll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭↚"), bstack11ll111_opy_ (u"ࠧ࠱ࠩ↛")))
        cli.bstack1ll1llll1ll_opy_(cli_context.platform_index)
        cli.bstack1llll11l1l1_opy_(bstack11l1lll11l_opy_(bstack11l111llll_opy_, CONFIG), cli_context.platform_index, bstack11l11l1l1_opy_)
        cli.bstack1lll11111l1_opy_()
        logger.debug(bstack11ll111_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ↜") + str(cli_context.platform_index) + bstack11ll111_opy_ (u"ࠤࠥ↝"))
        return # skip all existing bstack11111l1ll1l_opy_
    global bstack11l1l1111_opy_
    global bstack1ll1lll111_opy_
    global bstack1llll11l_opy_
    global bstack11l11l11_opy_
    global bstack1l1lll1l11_opy_
    global bstack11l11l1l_opy_
    global bstack1111l1lll_opy_
    global bstack1ll1ll1ll_opy_
    global bstack1ll111ll_opy_
    global bstack1l1ll1ll1_opy_
    global bstack1lll111l_opy_
    global bstack1111lll1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11l1l1111_opy_ = webdriver.Remote.__init__
        bstack1ll1lll111_opy_ = WebDriver.quit
        bstack1111l1lll_opy_ = WebDriver.close
        bstack1ll1ll1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭↞") in CONFIG or bstack11ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ↟") in CONFIG) and bstack111111l11_opy_():
        if bstack1l111l11l_opy_() < version.parse(bstack1l111ll1l1_opy_):
            logger.error(bstack11lll1l111_opy_.format(bstack1l111l11l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1ll111ll_opy_ = RemoteConnection._111l1ll1_opy_
            except Exception as e:
                logger.error(bstack11lll1llll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1ll1ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack1lll111l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l11lll11l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1111lll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭↠"))
    bstack1l1lll1ll_opy_ = CONFIG.get(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ↡"), {}).get(bstack11ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ↢"))
    bstack111l11ll1_opy_ = True
    bstack11lll11l_opy_(bstack1lll11llll_opy_)
if (bstack11l1l1ll11l_opy_()):
    bstack11111lllll1_opy_()
@bstack111l1ll11l_opy_(class_method=False)
def bstack11111l11lll_opy_(hook_name, event, bstack1l111lll1ll_opy_=None):
    if hook_name not in [bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ↣"), bstack11ll111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭↤"), bstack11ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ↥"), bstack11ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭↦"), bstack11ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ↧"), bstack11ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ↨"), bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭↩"), bstack11ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ↪")]:
        return
    node = store[bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭↫")]
    if hook_name in [bstack11ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ↬"), bstack11ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭↭")]:
        node = store[bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ↮")]
    elif hook_name in [bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ↯"), bstack11ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ↰")]:
        node = store[bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭↱")]
    hook_type = bstack111l1l111l1_opy_(hook_name)
    if event == bstack11ll111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ↲"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_[hook_type], bstack1ll1lll1ll1_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1lllll_opy_ = {
            bstack11ll111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ↳"): uuid,
            bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ↴"): bstack1l1l1llll_opy_(),
            bstack11ll111_opy_ (u"ࠬࡺࡹࡱࡧࠪ↵"): bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ↶"),
            bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ↷"): hook_type,
            bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ↸"): hook_name
        }
        store[bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭↹")].append(uuid)
        bstack11111lll1ll_opy_ = node.nodeid
        if hook_type == bstack11ll111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ↺"):
            if not _111l11l1ll_opy_.get(bstack11111lll1ll_opy_, None):
                _111l11l1ll_opy_[bstack11111lll1ll_opy_] = {bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ↻"): []}
            _111l11l1ll_opy_[bstack11111lll1ll_opy_][bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ↼")].append(bstack111l1lllll_opy_[bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↽")])
        _111l11l1ll_opy_[bstack11111lll1ll_opy_ + bstack11ll111_opy_ (u"ࠧ࠮ࠩ↾") + hook_name] = bstack111l1lllll_opy_
        bstack11111llll1l_opy_(node, bstack111l1lllll_opy_, bstack11ll111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ↿"))
    elif event == bstack11ll111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⇀"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1l11l_opy_[hook_type], bstack1ll1lll1ll1_opy_.POST, node, None, bstack1l111lll1ll_opy_)
            return
        bstack11l1111ll1_opy_ = node.nodeid + bstack11ll111_opy_ (u"ࠪ࠱ࠬ⇁") + hook_name
        _111l11l1ll_opy_[bstack11l1111ll1_opy_][bstack11ll111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⇂")] = bstack1l1l1llll_opy_()
        bstack11111l1lll1_opy_(_111l11l1ll_opy_[bstack11l1111ll1_opy_][bstack11ll111_opy_ (u"ࠬࡻࡵࡪࡦࠪ⇃")])
        bstack11111llll1l_opy_(node, _111l11l1ll_opy_[bstack11l1111ll1_opy_], bstack11ll111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⇄"), bstack11111ll1l1l_opy_=bstack1l111lll1ll_opy_)
def bstack11111l1l1ll_opy_():
    global bstack11111l1l1l1_opy_
    if bstack1ll1l1lll_opy_():
        bstack11111l1l1l1_opy_ = bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ⇅")
    else:
        bstack11111l1l1l1_opy_ = bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⇆")
@bstack111ll11ll_opy_.bstack1111l1lll11_opy_
def bstack11111l11l1l_opy_():
    bstack11111l1l1ll_opy_()
    if cli.is_running():
        try:
            bstack11l11l1llll_opy_(bstack11111l11lll_opy_)
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⇇").format(e))
        return
    if bstack111111l11_opy_():
        bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
        bstack11ll111_opy_ (u"ࠪࠫࠬࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡃࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡩࡨࡸࡸࠦࡵࡴࡧࡧࠤ࡫ࡵࡲࠡࡣ࠴࠵ࡾࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠮ࡹࡵࡥࡵࡶࡩ࡯ࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡳࡷࡱࠤࡧ࡫ࡣࡢࡷࡶࡩࠥ࡯ࡴࠡ࡫ࡶࠤࡵࡧࡴࡤࡪࡨࡨࠥ࡯࡮ࠡࡣࠣࡨ࡮࡬ࡦࡦࡴࡨࡲࡹࠦࡰࡳࡱࡦࡩࡸࡹࠠࡪࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡹࡸࠦࡷࡦࠢࡱࡩࡪࡪࠠࡵࡱࠣࡹࡸ࡫ࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡒࡤࡸࡨ࡮ࠨࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡫ࡥࡳࡪ࡬ࡦࡴࠬࠤ࡫ࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠫࠬ࠭⇈")
        if bstack11lll1l1l_opy_.get_property(bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⇉")):
            if CONFIG.get(bstack11ll111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⇊")) is not None and int(CONFIG[bstack11ll111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⇋")]) > 1:
                bstack1ll11ll11l_opy_(bstack1l11lllll_opy_)
            return
        bstack1ll11ll11l_opy_(bstack1l11lllll_opy_)
    try:
        bstack11l11l1llll_opy_(bstack11111l11lll_opy_)
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ⇌").format(e))
bstack11111l11l1l_opy_()