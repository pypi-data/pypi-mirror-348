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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111llllll1_opy_ import bstack111lll111l_opy_, bstack11l1111l1l_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11ll11ll11_opy_
from bstack_utils.helper import bstack1lll1ll1ll_opy_, bstack1l1l1llll_opy_, Result
from bstack_utils.bstack111lllllll_opy_ import bstack111ll11ll_opy_
from bstack_utils.capture import bstack111llll111_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1ll1l1l1ll_opy_:
    def __init__(self):
        self.bstack111lll1l1l_opy_ = bstack111llll111_opy_(self.bstack111llll1l1_opy_)
        self.tests = {}
    @staticmethod
    def bstack111llll1l1_opy_(log):
        if not (log[bstack11ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ໕")] and log[bstack11ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໖")].strip()):
            return
        active = bstack11ll11ll11_opy_.bstack111lllll11_opy_()
        log = {
            bstack11ll111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ໗"): log[bstack11ll111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ໘")],
            bstack11ll111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ໙"): bstack1l1l1llll_opy_(),
            bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໚"): log[bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ໛")],
        }
        if active:
            if active[bstack11ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨໜ")] == bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩໝ"):
                log[bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬໞ")] = active[bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ໟ")]
            elif active[bstack11ll111_opy_ (u"ࠧࡵࡻࡳࡩࠬ໠")] == bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹ࠭໡"):
                log[bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ໢")] = active[bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ໣")]
        bstack111ll11ll_opy_.bstack1l1ll1l111_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111lll1l1l_opy_.start()
        driver = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ໤"), None)
        bstack111llllll1_opy_ = bstack11l1111l1l_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1l1l1llll_opy_(),
            file_path=attrs.feature.filename,
            result=bstack11ll111_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨ໥"),
            framework=bstack11ll111_opy_ (u"࠭ࡂࡦࡪࡤࡺࡪ࠭໦"),
            scope=[attrs.feature.name],
            bstack11l111111l_opy_=bstack111ll11ll_opy_.bstack111lllll1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໧")] = bstack111llllll1_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack111ll11ll_opy_.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ໨"), bstack111llllll1_opy_)
    def end_test(self, attrs):
        bstack11l1111l11_opy_ = {
            bstack11ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ໩"): attrs.feature.name,
            bstack11ll111_opy_ (u"ࠥࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣ໪"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111llllll1_opy_ = self.tests[current_test_uuid][bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໫")]
        meta = {
            bstack11ll111_opy_ (u"ࠧ࡬ࡥࡢࡶࡸࡶࡪࠨ໬"): bstack11l1111l11_opy_,
            bstack11ll111_opy_ (u"ࠨࡳࡵࡧࡳࡷࠧ໭"): bstack111llllll1_opy_.meta.get(bstack11ll111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭໮"), []),
            bstack11ll111_opy_ (u"ࠣࡵࡦࡩࡳࡧࡲࡪࡱࠥ໯"): {
                bstack11ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ໰"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111llllll1_opy_.bstack11l11111ll_opy_(meta)
        bstack111llllll1_opy_.bstack11l111l111_opy_(bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ໱"), []))
        bstack111lll1lll_opy_, exception = self._11l11111l1_opy_(attrs)
        bstack111llll11l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1111111_opy_=[bstack111lll1lll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໲")].stop(time=bstack1l1l1llll_opy_(), duration=int(attrs.duration)*1000, result=bstack111llll11l_opy_)
        bstack111ll11ll_opy_.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ໳"), self.tests[threading.current_thread().current_test_uuid][bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ໴")])
    def bstack1l11ll1l11_opy_(self, attrs):
        bstack11l1111lll_opy_ = {
            bstack11ll111_opy_ (u"ࠧࡪࡦࠪ໵"): uuid4().__str__(),
            bstack11ll111_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ໶"): attrs.keyword,
            bstack11ll111_opy_ (u"ࠩࡶࡸࡪࡶ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩ໷"): [],
            bstack11ll111_opy_ (u"ࠪࡸࡪࡾࡴࠨ໸"): attrs.name,
            bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ໹"): bstack1l1l1llll_opy_(),
            bstack11ll111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ໺"): bstack11ll111_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ໻"),
            bstack11ll111_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ໼"): bstack11ll111_opy_ (u"ࠨࠩ໽")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໾")].add_step(bstack11l1111lll_opy_)
        threading.current_thread().current_step_uuid = bstack11l1111lll_opy_[bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭໿")]
    def bstack1111l1111_opy_(self, attrs):
        current_test_id = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨༀ"), None)
        current_step_uuid = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩ༁"), None)
        bstack111lll1lll_opy_, exception = self._11l11111l1_opy_(attrs)
        bstack111llll11l_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1111111_opy_=[bstack111lll1lll_opy_])
        self.tests[current_test_id][bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༂")].bstack111lll11l1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111llll11l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l11l111_opy_(self, name, attrs):
        try:
            bstack11l111l11l_opy_ = uuid4().__str__()
            self.tests[bstack11l111l11l_opy_] = {}
            self.bstack111lll1l1l_opy_.start()
            scopes = []
            driver = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭༃"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭༄")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l111l11l_opy_)
            if name in [bstack11ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ༅"), bstack11ll111_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ༆")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ༇"), bstack11ll111_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ༈")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11ll111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ༉")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111lll111l_opy_(
                name=name,
                uuid=bstack11l111l11l_opy_,
                started_at=bstack1l1l1llll_opy_(),
                file_path=file_path,
                framework=bstack11ll111_opy_ (u"ࠢࡃࡧ࡫ࡥࡻ࡫ࠢ༊"),
                bstack11l111111l_opy_=bstack111ll11ll_opy_.bstack111lllll1l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11ll111_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤ་"),
                hook_type=name
            )
            self.tests[bstack11l111l11l_opy_][bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠧ༌")] = hook_data
            current_test_id = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠥࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢ།"), None)
            if current_test_id:
                hook_data.bstack111lll1l11_opy_(current_test_id)
            if name == bstack11ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ༎"):
                threading.current_thread().before_all_hook_uuid = bstack11l111l11l_opy_
            threading.current_thread().current_hook_uuid = bstack11l111l11l_opy_
            bstack111ll11ll_opy_.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩࠨ༏"), hook_data)
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡫ࡳࡴࡱࠠࡦࡸࡨࡲࡹࡹࠬࠡࡪࡲࡳࡰࠦ࡮ࡢ࡯ࡨ࠾ࠥࠫࡳ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠨࡷࠧ༐"), name, e)
    def bstack1llll1111_opy_(self, attrs):
        bstack11l1111ll1_opy_ = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ༑"), None)
        hook_data = self.tests[bstack11l1111ll1_opy_][bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ༒")]
        status = bstack11ll111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ༓")
        exception = None
        bstack111lll1lll_opy_ = None
        if hook_data.name == bstack11ll111_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ༔"):
            self.bstack111lll1l1l_opy_.reset()
            bstack111lll1ll1_opy_ = self.tests[bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ༕"), None)][bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ༖")].result.result
            if bstack111lll1ll1_opy_ == bstack11ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ༗"):
                if attrs.hook_failures == 1:
                    status = bstack11ll111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪ༘ࠢ")
                elif attrs.hook_failures == 2:
                    status = bstack11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤ༙ࠣ")
            elif attrs.aborted:
                status = bstack11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༚")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11ll111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧ༛") and attrs.hook_failures == 1:
                status = bstack11ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ༜")
            elif hasattr(attrs, bstack11ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬ༝")) and attrs.error_message:
                status = bstack11ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ༞")
            bstack111lll1lll_opy_, exception = self._11l11111l1_opy_(attrs)
        bstack111llll11l_opy_ = Result(result=status, exception=exception, bstack11l1111111_opy_=[bstack111lll1lll_opy_])
        hook_data.stop(time=bstack1l1l1llll_opy_(), duration=0, result=bstack111llll11l_opy_)
        bstack111ll11ll_opy_.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ༟"), self.tests[bstack11l1111ll1_opy_][bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ༠")])
        threading.current_thread().current_hook_uuid = None
    def _11l11111l1_opy_(self, attrs):
        try:
            import traceback
            bstack11l1l11111_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111lll1lll_opy_ = bstack11l1l11111_opy_[-1] if bstack11l1l11111_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡷࡧࡣࡦࡤࡤࡧࡰࠨ༡"))
            bstack111lll1lll_opy_ = None
            exception = None
        return bstack111lll1lll_opy_, exception