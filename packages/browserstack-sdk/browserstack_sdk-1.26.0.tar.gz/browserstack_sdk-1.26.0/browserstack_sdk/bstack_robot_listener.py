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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111ll111l1_opy_ import RobotHandler
from bstack_utils.capture import bstack111llll111_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack111ll11l1l_opy_, bstack111lll111l_opy_, bstack11l1111l1l_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11ll11ll11_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack111ll11ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lll1ll1ll_opy_, bstack1l1l1llll_opy_, Result, \
    bstack111l1ll11l_opy_, bstack111l11l1l1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༢"): [],
        bstack11ll111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ༣"): [],
        bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ༤"): []
    }
    bstack111ll111ll_opy_ = []
    bstack111l11l111_opy_ = []
    @staticmethod
    def bstack111llll1l1_opy_(log):
        if not ((isinstance(log[bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༥")], list) or (isinstance(log[bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༦")], dict)) and len(log[bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༧")])>0) or (isinstance(log[bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༨")], str) and log[bstack11ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༩")].strip())):
            return
        active = bstack11ll11ll11_opy_.bstack111lllll11_opy_()
        log = {
            bstack11ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ༪"): log[bstack11ll111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ༫")],
            bstack11ll111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ༬"): bstack111l11l1l1_opy_().isoformat() + bstack11ll111_opy_ (u"࡛ࠧࠩ༭"),
            bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༮"): log[bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༯")],
        }
        if active:
            if active[bstack11ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨ༰")] == bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ༱"):
                log[bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ༲")] = active[bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭༳")]
            elif active[bstack11ll111_opy_ (u"ࠧࡵࡻࡳࡩࠬ༴")] == bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹ༵࠭"):
                log[bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ༶")] = active[bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦ༷ࠪ")]
        bstack111ll11ll_opy_.bstack1l1ll1l111_opy_([log])
    def __init__(self):
        self.messages = bstack111l1l111l_opy_()
        self._111l1l1l1l_opy_ = None
        self._111l1111l1_opy_ = None
        self._111l11l1ll_opy_ = OrderedDict()
        self.bstack111lll1l1l_opy_ = bstack111llll111_opy_(self.bstack111llll1l1_opy_)
    @bstack111l1ll11l_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1llll1_opy_()
        if not self._111l11l1ll_opy_.get(attrs.get(bstack11ll111_opy_ (u"ࠫ࡮ࡪࠧ༸")), None):
            self._111l11l1ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠬ࡯ࡤࠨ༹"))] = {}
        bstack111l11llll_opy_ = bstack11l1111l1l_opy_(
                bstack111ll1l1l1_opy_=attrs.get(bstack11ll111_opy_ (u"࠭ࡩࡥࠩ༺")),
                name=name,
                started_at=bstack1l1l1llll_opy_(),
                file_path=os.path.relpath(attrs[bstack11ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ༻")], start=os.getcwd()) if attrs.get(bstack11ll111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ༼")) != bstack11ll111_opy_ (u"ࠩࠪ༽") else bstack11ll111_opy_ (u"ࠪࠫ༾"),
                framework=bstack11ll111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ༿")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11ll111_opy_ (u"ࠬ࡯ࡤࠨཀ"), None)
        self._111l11l1ll_opy_[attrs.get(bstack11ll111_opy_ (u"࠭ࡩࡥࠩཁ"))][bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪག")] = bstack111l11llll_opy_
    @bstack111l1ll11l_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111ll1ll11_opy_()
        self._111l11ll1l_opy_(messages)
        for bstack111lll1111_opy_ in self.bstack111ll111ll_opy_:
            bstack111lll1111_opy_[bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪགྷ")][bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨང")].extend(self.store[bstack11ll111_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩཅ")])
            bstack111ll11ll_opy_.bstack1l1111ll1_opy_(bstack111lll1111_opy_)
        self.bstack111ll111ll_opy_ = []
        self.store[bstack11ll111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪཆ")] = []
    @bstack111l1ll11l_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111lll1l1l_opy_.start()
        if not self._111l11l1ll_opy_.get(attrs.get(bstack11ll111_opy_ (u"ࠬ࡯ࡤࠨཇ")), None):
            self._111l11l1ll_opy_[attrs.get(bstack11ll111_opy_ (u"࠭ࡩࡥࠩ཈"))] = {}
        driver = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ཉ"), None)
        bstack111llllll1_opy_ = bstack11l1111l1l_opy_(
            bstack111ll1l1l1_opy_=attrs.get(bstack11ll111_opy_ (u"ࠨ࡫ࡧࠫཊ")),
            name=name,
            started_at=bstack1l1l1llll_opy_(),
            file_path=os.path.relpath(attrs[bstack11ll111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩཋ")], start=os.getcwd()),
            scope=RobotHandler.bstack111ll1lll1_opy_(attrs.get(bstack11ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪཌ"), None)),
            framework=bstack11ll111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪཌྷ"),
            tags=attrs[bstack11ll111_opy_ (u"ࠬࡺࡡࡨࡵࠪཎ")],
            hooks=self.store[bstack11ll111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬཏ")],
            bstack11l111111l_opy_=bstack111ll11ll_opy_.bstack111lllll1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11ll111_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤཐ").format(bstack11ll111_opy_ (u"ࠣࠢࠥད").join(attrs[bstack11ll111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧདྷ")]), name) if attrs[bstack11ll111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨན")] else name
        )
        self._111l11l1ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠫ࡮ࡪࠧཔ"))][bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཕ")] = bstack111llllll1_opy_
        threading.current_thread().current_test_uuid = bstack111llllll1_opy_.bstack111ll1111l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11ll111_opy_ (u"࠭ࡩࡥࠩབ"), None)
        self.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨབྷ"), bstack111llllll1_opy_)
    @bstack111l1ll11l_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111lll1l1l_opy_.reset()
        bstack111l1111ll_opy_ = bstack111l111l11_opy_.get(attrs.get(bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨམ")), bstack11ll111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪཙ"))
        self._111l11l1ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ཚ"))][bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཛ")].stop(time=bstack1l1l1llll_opy_(), duration=int(attrs.get(bstack11ll111_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪཛྷ"), bstack11ll111_opy_ (u"࠭࠰ࠨཝ"))), result=Result(result=bstack111l1111ll_opy_, exception=attrs.get(bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཞ")), bstack11l1111111_opy_=[attrs.get(bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩཟ"))]))
        self.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫའ"), self._111l11l1ll_opy_[attrs.get(bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ཡ"))][bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧར")], True)
        self.store[bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩལ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l1ll11l_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1llll1_opy_()
        current_test_id = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨཤ"), None)
        bstack111l11111l_opy_ = current_test_id if bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩཥ"), None) else bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫས"), None)
        if attrs.get(bstack11ll111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧཧ"), bstack11ll111_opy_ (u"ࠪࠫཨ")).lower() in [bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪཀྵ"), bstack11ll111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧཪ")]:
            hook_type = bstack111ll11l11_opy_(attrs.get(bstack11ll111_opy_ (u"࠭ࡴࡺࡲࡨࠫཫ")), bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫཬ"), None))
            hook_name = bstack11ll111_opy_ (u"ࠨࡽࢀࠫ཭").format(attrs.get(bstack11ll111_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ཮"), bstack11ll111_opy_ (u"ࠪࠫ཯")))
            if hook_type in [bstack11ll111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ཰"), bstack11ll111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨཱ")]:
                hook_name = bstack11ll111_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃིࠧ").format(bstack111ll1l1ll_opy_.get(hook_type), attrs.get(bstack11ll111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ཱིࠧ"), bstack11ll111_opy_ (u"ࠨུࠩ")))
            bstack111l1lllll_opy_ = bstack111lll111l_opy_(
                bstack111ll1l1l1_opy_=bstack111l11111l_opy_ + bstack11ll111_opy_ (u"ࠩ࠰ཱུࠫ") + attrs.get(bstack11ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨྲྀ"), bstack11ll111_opy_ (u"ࠫࠬཷ")).lower(),
                name=hook_name,
                started_at=bstack1l1l1llll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11ll111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬླྀ")), start=os.getcwd()),
                framework=bstack11ll111_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬཹ"),
                tags=attrs[bstack11ll111_opy_ (u"ࠧࡵࡣࡪࡷེࠬ")],
                scope=RobotHandler.bstack111ll1lll1_opy_(attrs.get(bstack11ll111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨཻ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1lllll_opy_.bstack111ll1111l_opy_()
            threading.current_thread().current_hook_id = bstack111l11111l_opy_ + bstack11ll111_opy_ (u"ࠩ࠰ོࠫ") + attrs.get(bstack11ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨཽ"), bstack11ll111_opy_ (u"ࠫࠬཾ")).lower()
            self.store[bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩཿ")] = [bstack111l1lllll_opy_.bstack111ll1111l_opy_()]
            if bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦྀࠪ"), None):
                self.store[bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶཱྀࠫ")].append(bstack111l1lllll_opy_.bstack111ll1111l_opy_())
            else:
                self.store[bstack11ll111_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧྂ")].append(bstack111l1lllll_opy_.bstack111ll1111l_opy_())
            if bstack111l11111l_opy_:
                self._111l11l1ll_opy_[bstack111l11111l_opy_ + bstack11ll111_opy_ (u"ࠩ࠰ࠫྃ") + attrs.get(bstack11ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨ྄"), bstack11ll111_opy_ (u"ࠫࠬ྅")).lower()] = { bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ྆"): bstack111l1lllll_opy_ }
            bstack111ll11ll_opy_.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ྇"), bstack111l1lllll_opy_)
        else:
            bstack11l1111lll_opy_ = {
                bstack11ll111_opy_ (u"ࠧࡪࡦࠪྈ"): uuid4().__str__(),
                bstack11ll111_opy_ (u"ࠨࡶࡨࡼࡹ࠭ྉ"): bstack11ll111_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨྊ").format(attrs.get(bstack11ll111_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪྋ")), attrs.get(bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡴࠩྌ"), bstack11ll111_opy_ (u"ࠬ࠭ྍ"))) if attrs.get(bstack11ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫྎ"), []) else attrs.get(bstack11ll111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧྏ")),
                bstack11ll111_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨྐ"): attrs.get(bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧྑ"), []),
                bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧྒ"): bstack1l1l1llll_opy_(),
                bstack11ll111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫྒྷ"): bstack11ll111_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ྔ"),
                bstack11ll111_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫྕ"): attrs.get(bstack11ll111_opy_ (u"ࠧࡥࡱࡦࠫྖ"), bstack11ll111_opy_ (u"ࠨࠩྗ"))
            }
            if attrs.get(bstack11ll111_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪ྘"), bstack11ll111_opy_ (u"ࠪࠫྙ")) != bstack11ll111_opy_ (u"ࠫࠬྚ"):
                bstack11l1111lll_opy_[bstack11ll111_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ྛ")] = attrs.get(bstack11ll111_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧྜ"))
            if not self.bstack111l11l111_opy_:
                self._111l11l1ll_opy_[self._111ll1l11l_opy_()][bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྜྷ")].add_step(bstack11l1111lll_opy_)
                threading.current_thread().current_step_uuid = bstack11l1111lll_opy_[bstack11ll111_opy_ (u"ࠨ࡫ࡧࠫྞ")]
            self.bstack111l11l111_opy_.append(bstack11l1111lll_opy_)
    @bstack111l1ll11l_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111ll1ll11_opy_()
        self._111l11ll1l_opy_(messages)
        current_test_id = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫྟ"), None)
        bstack111l11111l_opy_ = current_test_id if current_test_id else bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ྠ"), None)
        bstack111l1ll111_opy_ = bstack111l111l11_opy_.get(attrs.get(bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫྡ")), bstack11ll111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ྡྷ"))
        bstack111l11lll1_opy_ = attrs.get(bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྣ"))
        if bstack111l1ll111_opy_ != bstack11ll111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨྤ") and not attrs.get(bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྥ")) and self._111l1l1l1l_opy_:
            bstack111l11lll1_opy_ = self._111l1l1l1l_opy_
        bstack111llll11l_opy_ = Result(result=bstack111l1ll111_opy_, exception=bstack111l11lll1_opy_, bstack11l1111111_opy_=[bstack111l11lll1_opy_])
        if attrs.get(bstack11ll111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧྦ"), bstack11ll111_opy_ (u"ࠪࠫྦྷ")).lower() in [bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪྨ"), bstack11ll111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧྩ")]:
            bstack111l11111l_opy_ = current_test_id if current_test_id else bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩྪ"), None)
            if bstack111l11111l_opy_:
                bstack11l1111ll1_opy_ = bstack111l11111l_opy_ + bstack11ll111_opy_ (u"ࠢ࠮ࠤྫ") + attrs.get(bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ྫྷ"), bstack11ll111_opy_ (u"ࠩࠪྭ")).lower()
                self._111l11l1ll_opy_[bstack11l1111ll1_opy_][bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྮ")].stop(time=bstack1l1l1llll_opy_(), duration=int(attrs.get(bstack11ll111_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩྯ"), bstack11ll111_opy_ (u"ࠬ࠶ࠧྰ"))), result=bstack111llll11l_opy_)
                bstack111ll11ll_opy_.bstack111llll1ll_opy_(bstack11ll111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨྱ"), self._111l11l1ll_opy_[bstack11l1111ll1_opy_][bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྲ")])
        else:
            bstack111l11111l_opy_ = current_test_id if current_test_id else bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪླ"), None)
            if bstack111l11111l_opy_ and len(self.bstack111l11l111_opy_) == 1:
                current_step_uuid = bstack1lll1ll1ll_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭ྴ"), None)
                self._111l11l1ll_opy_[bstack111l11111l_opy_][bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྵ")].bstack111lll11l1_opy_(current_step_uuid, duration=int(attrs.get(bstack11ll111_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩྶ"), bstack11ll111_opy_ (u"ࠬ࠶ࠧྷ"))), result=bstack111llll11l_opy_)
            else:
                self.bstack111ll11111_opy_(attrs)
            self.bstack111l11l111_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11ll111_opy_ (u"࠭ࡨࡵ࡯࡯ࠫྸ"), bstack11ll111_opy_ (u"ࠧ࡯ࡱࠪྐྵ")) == bstack11ll111_opy_ (u"ࠨࡻࡨࡷࠬྺ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11ll11ll11_opy_.bstack111lllll11_opy_():
                logs.append({
                    bstack11ll111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬྻ"): bstack1l1l1llll_opy_(),
                    bstack11ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྼ"): message.get(bstack11ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ྽")),
                    bstack11ll111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ྾"): message.get(bstack11ll111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ྿")),
                    **bstack11ll11ll11_opy_.bstack111lllll11_opy_()
                })
                if len(logs) > 0:
                    bstack111ll11ll_opy_.bstack1l1ll1l111_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack111ll11ll_opy_.bstack111ll1l111_opy_()
    def bstack111ll11111_opy_(self, bstack111ll1ll1l_opy_):
        if not bstack11ll11ll11_opy_.bstack111lllll11_opy_():
            return
        kwname = bstack11ll111_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭࿀").format(bstack111ll1ll1l_opy_.get(bstack11ll111_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ࿁")), bstack111ll1ll1l_opy_.get(bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ࿂"), bstack11ll111_opy_ (u"ࠪࠫ࿃"))) if bstack111ll1ll1l_opy_.get(bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿄"), []) else bstack111ll1ll1l_opy_.get(bstack11ll111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿅"))
        error_message = bstack11ll111_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟࿆ࠦࠧ").format(kwname, bstack111ll1ll1l_opy_.get(bstack11ll111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ࿇")), str(bstack111ll1ll1l_opy_.get(bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿈"))))
        bstack111l111l1l_opy_ = bstack11ll111_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣ࿉").format(kwname, bstack111ll1ll1l_opy_.get(bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ࿊")))
        bstack111l1l1ll1_opy_ = error_message if bstack111ll1ll1l_opy_.get(bstack11ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿋")) else bstack111l111l1l_opy_
        bstack111l1lll1l_opy_ = {
            bstack11ll111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ࿌"): self.bstack111l11l111_opy_[-1].get(bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ࿍"), bstack1l1l1llll_opy_()),
            bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿎"): bstack111l1l1ll1_opy_,
            bstack11ll111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿏"): bstack11ll111_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ࿐") if bstack111ll1ll1l_opy_.get(bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ࿑")) == bstack11ll111_opy_ (u"ࠫࡋࡇࡉࡍࠩ࿒") else bstack11ll111_opy_ (u"ࠬࡏࡎࡇࡑࠪ࿓"),
            **bstack11ll11ll11_opy_.bstack111lllll11_opy_()
        }
        bstack111ll11ll_opy_.bstack1l1ll1l111_opy_([bstack111l1lll1l_opy_])
    def _111ll1l11l_opy_(self):
        for bstack111ll1l1l1_opy_ in reversed(self._111l11l1ll_opy_):
            bstack111l11ll11_opy_ = bstack111ll1l1l1_opy_
            data = self._111l11l1ll_opy_[bstack111ll1l1l1_opy_][bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿔")]
            if isinstance(data, bstack111lll111l_opy_):
                if not bstack11ll111_opy_ (u"ࠧࡆࡃࡆࡌࠬ࿕") in data.bstack111l11l11l_opy_():
                    return bstack111l11ll11_opy_
            else:
                return bstack111l11ll11_opy_
    def _111l11ll1l_opy_(self, messages):
        try:
            bstack111ll11ll1_opy_ = BuiltIn().get_variable_value(bstack11ll111_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢ࿖")) in (bstack111ll11lll_opy_.DEBUG, bstack111ll11lll_opy_.TRACE)
            for message, bstack111l1l1l11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿗"))
                level = message.get(bstack11ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿘"))
                if level == bstack111ll11lll_opy_.FAIL:
                    self._111l1l1l1l_opy_ = name or self._111l1l1l1l_opy_
                    self._111l1111l1_opy_ = bstack111l1l1l11_opy_.get(bstack11ll111_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ࿙")) if bstack111ll11ll1_opy_ and bstack111l1l1l11_opy_ else self._111l1111l1_opy_
        except:
            pass
    @classmethod
    def bstack111llll1ll_opy_(self, event: str, bstack111l1l11l1_opy_: bstack111ll11l1l_opy_, bstack111l1l1111_opy_=False):
        if event == bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ࿚"):
            bstack111l1l11l1_opy_.set(hooks=self.store[bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ࿛")])
        if event == bstack11ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ࿜"):
            event = bstack11ll111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ࿝")
        if bstack111l1l1111_opy_:
            bstack111l1ll1l1_opy_ = {
                bstack11ll111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭࿞"): event,
                bstack111l1l11l1_opy_.bstack111l1l11ll_opy_(): bstack111l1l11l1_opy_.bstack111l1ll1ll_opy_(event)
            }
            self.bstack111ll111ll_opy_.append(bstack111l1ll1l1_opy_)
        else:
            bstack111ll11ll_opy_.bstack111llll1ll_opy_(event, bstack111l1l11l1_opy_)
class bstack111l1l111l_opy_:
    def __init__(self):
        self._111l1l1lll_opy_ = []
    def bstack111l1llll1_opy_(self):
        self._111l1l1lll_opy_.append([])
    def bstack111ll1ll11_opy_(self):
        return self._111l1l1lll_opy_.pop() if self._111l1l1lll_opy_ else list()
    def push(self, message):
        self._111l1l1lll_opy_[-1].append(message) if self._111l1l1lll_opy_ else self._111l1l1lll_opy_.append([message])
class bstack111ll11lll_opy_:
    FAIL = bstack11ll111_opy_ (u"ࠪࡊࡆࡏࡌࠨ࿟")
    ERROR = bstack11ll111_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ࿠")
    WARNING = bstack11ll111_opy_ (u"ࠬ࡝ࡁࡓࡐࠪ࿡")
    bstack111l1lll11_opy_ = bstack11ll111_opy_ (u"࠭ࡉࡏࡈࡒࠫ࿢")
    DEBUG = bstack11ll111_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭࿣")
    TRACE = bstack11ll111_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧ࿤")
    bstack111ll1llll_opy_ = [FAIL, ERROR]
def bstack111l111lll_opy_(bstack111l111ll1_opy_):
    if not bstack111l111ll1_opy_:
        return None
    if bstack111l111ll1_opy_.get(bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿥"), None):
        return getattr(bstack111l111ll1_opy_[bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿦")], bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩ࿧"), None)
    return bstack111l111ll1_opy_.get(bstack11ll111_opy_ (u"ࠬࡻࡵࡪࡦࠪ࿨"), None)
def bstack111ll11l11_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ࿩"), bstack11ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ࿪")]:
        return
    if hook_type.lower() == bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ࿫"):
        if current_test_uuid is None:
            return bstack11ll111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭࿬")
        else:
            return bstack11ll111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ࿭")
    elif hook_type.lower() == bstack11ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭࿮"):
        if current_test_uuid is None:
            return bstack11ll111_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨ࿯")
        else:
            return bstack11ll111_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ࿰")