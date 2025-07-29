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
from uuid import uuid4
from bstack_utils.helper import bstack1l1l1llll_opy_, bstack11ll11l1l11_opy_
from bstack_utils.bstack1l1lll1111_opy_ import bstack111l1l1111l_opy_
class bstack111ll11l1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1111llll1l1_opy_=None, bstack1111ll1ll1l_opy_=True, bstack1l11l1111l1_opy_=None, bstack11l1llll1_opy_=None, result=None, duration=None, bstack111ll1l1l1_opy_=None, meta={}):
        self.bstack111ll1l1l1_opy_ = bstack111ll1l1l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111ll1ll1l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111llll1l1_opy_ = bstack1111llll1l1_opy_
        self.bstack1l11l1111l1_opy_ = bstack1l11l1111l1_opy_
        self.bstack11l1llll1_opy_ = bstack11l1llll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll1111l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l11111ll_opy_(self, meta):
        self.meta = meta
    def bstack11l111l111_opy_(self, hooks):
        self.hooks = hooks
    def bstack1111lll1lll_opy_(self):
        bstack1111lll111l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᷧ"): bstack1111lll111l_opy_,
            bstack11ll111_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᷨ"): bstack1111lll111l_opy_,
            bstack11ll111_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᷩ"): bstack1111lll111l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11ll111_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣᷪ") + key)
            setattr(self, key, val)
    def bstack1111lll1l11_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᷫ"): self.name,
            bstack11ll111_opy_ (u"ࠩࡥࡳࡩࡿࠧᷬ"): {
                bstack11ll111_opy_ (u"ࠪࡰࡦࡴࡧࠨᷭ"): bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᷮ"),
                bstack11ll111_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᷯ"): self.code
            },
            bstack11ll111_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᷰ"): self.scope,
            bstack11ll111_opy_ (u"ࠧࡵࡣࡪࡷࠬᷱ"): self.tags,
            bstack11ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᷲ"): self.framework,
            bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᷳ"): self.started_at
        }
    def bstack1111ll1ll11_opy_(self):
        return {
         bstack11ll111_opy_ (u"ࠪࡱࡪࡺࡡࠨᷴ"): self.meta
        }
    def bstack1111lllll11_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ᷵"): {
                bstack11ll111_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ᷶"): self.bstack1111llll1l1_opy_
            }
        }
    def bstack1111lll1111_opy_(self, bstack1111lll1l1l_opy_, details):
        step = next(filter(lambda st: st[bstack11ll111_opy_ (u"࠭ࡩࡥ᷷ࠩ")] == bstack1111lll1l1l_opy_, self.meta[bstack11ll111_opy_ (u"ࠧࡴࡶࡨࡴࡸ᷸࠭")]), None)
        step.update(details)
    def bstack1l11ll1l11_opy_(self, bstack1111lll1l1l_opy_):
        step = next(filter(lambda st: st[bstack11ll111_opy_ (u"ࠨ࡫ࡧ᷹ࠫ")] == bstack1111lll1l1l_opy_, self.meta[bstack11ll111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᷺")]), None)
        step.update({
            bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᷻"): bstack1l1l1llll_opy_()
        })
    def bstack111lll11l1_opy_(self, bstack1111lll1l1l_opy_, result, duration=None):
        bstack1l11l1111l1_opy_ = bstack1l1l1llll_opy_()
        if bstack1111lll1l1l_opy_ is not None and self.meta.get(bstack11ll111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ᷼")):
            step = next(filter(lambda st: st[bstack11ll111_opy_ (u"ࠬ࡯ࡤࠨ᷽")] == bstack1111lll1l1l_opy_, self.meta[bstack11ll111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ᷾")]), None)
            step.update({
                bstack11ll111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸ᷿ࠬ"): bstack1l11l1111l1_opy_,
                bstack11ll111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪḀ"): duration if duration else bstack11ll11l1l11_opy_(step[bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ḁ")], bstack1l11l1111l1_opy_),
                bstack11ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪḂ"): result.result,
                bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬḃ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111llll1ll_opy_):
        if self.meta.get(bstack11ll111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫḄ")):
            self.meta[bstack11ll111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬḅ")].append(bstack1111llll1ll_opy_)
        else:
            self.meta[bstack11ll111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Ḇ")] = [ bstack1111llll1ll_opy_ ]
    def bstack1111lll11ll_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ḇ"): self.bstack111ll1111l_opy_(),
            **self.bstack1111lll1l11_opy_(),
            **self.bstack1111lll1lll_opy_(),
            **self.bstack1111ll1ll11_opy_()
        }
    def bstack1111lll1ll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧḈ"): self.bstack1l11l1111l1_opy_,
            bstack11ll111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫḉ"): self.duration,
            bstack11ll111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫḊ"): self.result.result
        }
        if data[bstack11ll111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬḋ")] == bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ḍ"):
            data[bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ḍ")] = self.result.bstack1111l1l11l_opy_()
            data[bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩḎ")] = [{bstack11ll111_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬḏ"): self.result.bstack11l1ll1llll_opy_()}]
        return data
    def bstack1111llll11l_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨḐ"): self.bstack111ll1111l_opy_(),
            **self.bstack1111lll1l11_opy_(),
            **self.bstack1111lll1lll_opy_(),
            **self.bstack1111lll1ll1_opy_(),
            **self.bstack1111ll1ll11_opy_()
        }
    def bstack111l1ll1ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11ll111_opy_ (u"ࠫࡘࡺࡡࡳࡶࡨࡨࠬḑ") in event:
            return self.bstack1111lll11ll_opy_()
        elif bstack11ll111_opy_ (u"ࠬࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧḒ") in event:
            return self.bstack1111llll11l_opy_()
    def bstack111l1l11ll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11l1111l1_opy_ = time if time else bstack1l1l1llll_opy_()
        self.duration = duration if duration else bstack11ll11l1l11_opy_(self.started_at, self.bstack1l11l1111l1_opy_)
        if result:
            self.result = result
class bstack11l1111l1l_opy_(bstack111ll11l1l_opy_):
    def __init__(self, hooks=[], bstack11l111111l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
        super().__init__(*args, **kwargs, bstack11l1llll1_opy_=bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࠫḓ"))
    @classmethod
    def bstack1111lll11l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll111_opy_ (u"ࠧࡪࡦࠪḔ"): id(step),
                bstack11ll111_opy_ (u"ࠨࡶࡨࡼࡹ࠭ḕ"): step.name,
                bstack11ll111_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪḖ"): step.keyword,
            })
        return bstack11l1111l1l_opy_(
            **kwargs,
            meta={
                bstack11ll111_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫḗ"): {
                    bstack11ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩḘ"): feature.name,
                    bstack11ll111_opy_ (u"ࠬࡶࡡࡵࡪࠪḙ"): feature.filename,
                    bstack11ll111_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫḚ"): feature.description
                },
                bstack11ll111_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩḛ"): {
                    bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ḝ"): scenario.name
                },
                bstack11ll111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨḝ"): steps,
                bstack11ll111_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬḞ"): bstack111l1l1111l_opy_(test)
            }
        )
    def bstack1111ll1llll_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪḟ"): self.hooks
        }
    def bstack1111llll111_opy_(self):
        if self.bstack11l111111l_opy_:
            return {
                bstack11ll111_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫḠ"): self.bstack11l111111l_opy_
            }
        return {}
    def bstack1111llll11l_opy_(self):
        return {
            **super().bstack1111llll11l_opy_(),
            **self.bstack1111ll1llll_opy_()
        }
    def bstack1111lll11ll_opy_(self):
        return {
            **super().bstack1111lll11ll_opy_(),
            **self.bstack1111llll111_opy_()
        }
    def bstack111l1l11ll_opy_(self):
        return bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨḡ")
class bstack111lll111l_opy_(bstack111ll11l1l_opy_):
    def __init__(self, hook_type, *args,bstack11l111111l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111ll1lll1_opy_ = None
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
        super().__init__(*args, **kwargs, bstack11l1llll1_opy_=bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࠬḢ"))
    def bstack111l11l11l_opy_(self):
        return self.hook_type
    def bstack1111ll1l1ll_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫḣ"): self.hook_type
        }
    def bstack1111llll11l_opy_(self):
        return {
            **super().bstack1111llll11l_opy_(),
            **self.bstack1111ll1l1ll_opy_()
        }
    def bstack1111lll11ll_opy_(self):
        return {
            **super().bstack1111lll11ll_opy_(),
            bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧḤ"): self.bstack1111ll1lll1_opy_,
            **self.bstack1111ll1l1ll_opy_()
        }
    def bstack111l1l11ll_opy_(self):
        return bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬḥ")
    def bstack111lll1l11_opy_(self, bstack1111ll1lll1_opy_):
        self.bstack1111ll1lll1_opy_ = bstack1111ll1lll1_opy_