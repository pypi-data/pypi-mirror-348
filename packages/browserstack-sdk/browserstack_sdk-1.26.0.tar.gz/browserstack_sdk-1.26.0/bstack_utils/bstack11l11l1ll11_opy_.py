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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1l11llll_opy_
from browserstack_sdk.bstack1l11lll1ll_opy_ import bstack1lll1111l_opy_
def _11l11l111l1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11l1llll_opy_:
    def __init__(self, handler):
        self._11l11l1l111_opy_ = {}
        self._11l11l1l11l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1lll1111l_opy_.version()
        if bstack11l1l11llll_opy_(pytest_version, bstack11ll111_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢᯥ")) >= 0:
            self._11l11l1l111_opy_[bstack11ll111_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩ᯦ࠬ")] = Module._register_setup_function_fixture
            self._11l11l1l111_opy_[bstack11ll111_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯧ")] = Module._register_setup_module_fixture
            self._11l11l1l111_opy_[bstack11ll111_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯨ")] = Class._register_setup_class_fixture
            self._11l11l1l111_opy_[bstack11ll111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯩ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11l11lll_opy_(bstack11ll111_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯪ"))
            Module._register_setup_module_fixture = self.bstack11l11l11lll_opy_(bstack11ll111_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯫ"))
            Class._register_setup_class_fixture = self.bstack11l11l11lll_opy_(bstack11ll111_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯬ"))
            Class._register_setup_method_fixture = self.bstack11l11l11lll_opy_(bstack11ll111_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯭ"))
        else:
            self._11l11l1l111_opy_[bstack11ll111_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯮ")] = Module._inject_setup_function_fixture
            self._11l11l1l111_opy_[bstack11ll111_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯯ")] = Module._inject_setup_module_fixture
            self._11l11l1l111_opy_[bstack11ll111_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯰ")] = Class._inject_setup_class_fixture
            self._11l11l1l111_opy_[bstack11ll111_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯱ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11l11lll_opy_(bstack11ll111_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧ᯲ࠪ"))
            Module._inject_setup_module_fixture = self.bstack11l11l11lll_opy_(bstack11ll111_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦ᯳ࠩ"))
            Class._inject_setup_class_fixture = self.bstack11l11l11lll_opy_(bstack11ll111_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᯴"))
            Class._inject_setup_method_fixture = self.bstack11l11l11lll_opy_(bstack11ll111_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᯵"))
    def bstack11l11l11111_opy_(self, bstack11l11l1lll1_opy_, hook_type):
        bstack11l11l11l1l_opy_ = id(bstack11l11l1lll1_opy_.__class__)
        if (bstack11l11l11l1l_opy_, hook_type) in self._11l11l1l11l_opy_:
            return
        meth = getattr(bstack11l11l1lll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11l1l11l_opy_[(bstack11l11l11l1l_opy_, hook_type)] = meth
            setattr(bstack11l11l1lll1_opy_, hook_type, self.bstack11l11l1111l_opy_(hook_type, bstack11l11l11l1l_opy_))
    def bstack11l11l1ll1l_opy_(self, instance, bstack11l11l11l11_opy_):
        if bstack11l11l11l11_opy_ == bstack11ll111_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ᯶"):
            self.bstack11l11l11111_opy_(instance.obj, bstack11ll111_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨ᯷"))
            self.bstack11l11l11111_opy_(instance.obj, bstack11ll111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥ᯸"))
        if bstack11l11l11l11_opy_ == bstack11ll111_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ᯹"):
            self.bstack11l11l11111_opy_(instance.obj, bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢ᯺"))
            self.bstack11l11l11111_opy_(instance.obj, bstack11ll111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦ᯻"))
        if bstack11l11l11l11_opy_ == bstack11ll111_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥ᯼"):
            self.bstack11l11l11111_opy_(instance.obj, bstack11ll111_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤ᯽"))
            self.bstack11l11l11111_opy_(instance.obj, bstack11ll111_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨ᯾"))
        if bstack11l11l11l11_opy_ == bstack11ll111_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ᯿"):
            self.bstack11l11l11111_opy_(instance.obj, bstack11ll111_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨᰀ"))
            self.bstack11l11l11111_opy_(instance.obj, bstack11ll111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥᰁ"))
    @staticmethod
    def bstack11l11l11ll1_opy_(hook_type, func, args):
        if hook_type in [bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᰂ"), bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᰃ")]:
            _11l11l111l1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11l1111l_opy_(self, hook_type, bstack11l11l11l1l_opy_):
        def bstack11l11l1l1l1_opy_(arg=None):
            self.handler(hook_type, bstack11ll111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᰄ"))
            result = None
            try:
                bstack1111111111_opy_ = self._11l11l1l11l_opy_[(bstack11l11l11l1l_opy_, hook_type)]
                self.bstack11l11l11ll1_opy_(hook_type, bstack1111111111_opy_, (arg,))
                result = Result(result=bstack11ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᰅ"))
            except Exception as e:
                result = Result(result=bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᰆ"), exception=e)
                self.handler(hook_type, bstack11ll111_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᰇ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll111_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᰈ"), result)
        def bstack11l11l111ll_opy_(this, arg=None):
            self.handler(hook_type, bstack11ll111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᰉ"))
            result = None
            exception = None
            try:
                self.bstack11l11l11ll1_opy_(hook_type, self._11l11l1l11l_opy_[hook_type], (this, arg))
                result = Result(result=bstack11ll111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᰊ"))
            except Exception as e:
                result = Result(result=bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᰋ"), exception=e)
                self.handler(hook_type, bstack11ll111_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᰌ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᰍ"), result)
        if hook_type in [bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᰎ"), bstack11ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᰏ")]:
            return bstack11l11l111ll_opy_
        return bstack11l11l1l1l1_opy_
    def bstack11l11l11lll_opy_(self, bstack11l11l11l11_opy_):
        def bstack11l11l1l1ll_opy_(this, *args, **kwargs):
            self.bstack11l11l1ll1l_opy_(this, bstack11l11l11l11_opy_)
            self._11l11l1l111_opy_[bstack11l11l11l11_opy_](this, *args, **kwargs)
        return bstack11l11l1l1ll_opy_