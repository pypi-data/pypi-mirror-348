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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11llll11111_opy_, bstack11lll1l1l11_opy_, bstack11ll111ll1_opy_, bstack111l1ll11l_opy_, bstack11l11ll1l11_opy_, bstack11l11ll11l1_opy_, bstack11l1ll11l1l_opy_, bstack1l1l1llll_opy_, bstack1lll1ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l111llll_opy_ import bstack111l11l11l1_opy_
import bstack_utils.bstack1lll111l1l_opy_ as bstack1l11lll111_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11ll11ll11_opy_
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from bstack_utils.bstack1l11ll111l_opy_ import bstack1l11ll111l_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack111ll11l1l_opy_
bstack1111l1lll1l_opy_ = bstack11ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫḦ")
logger = logging.getLogger(__name__)
class bstack111ll11ll_opy_:
    bstack111l111llll_opy_ = None
    bs_config = None
    bstack1ll1ll1ll1_opy_ = None
    @classmethod
    @bstack111l1ll11l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1lll11l_opy_, stage=STAGE.bstack111lllll_opy_)
    def launch(cls, bs_config, bstack1ll1ll1ll1_opy_):
        cls.bs_config = bs_config
        cls.bstack1ll1ll1ll1_opy_ = bstack1ll1ll1ll1_opy_
        try:
            cls.bstack1111ll11ll1_opy_()
            bstack11llll1ll1l_opy_ = bstack11llll11111_opy_(bs_config)
            bstack11llll11ll1_opy_ = bstack11lll1l1l11_opy_(bs_config)
            data = bstack1l11lll111_opy_.bstack1111l1ll1ll_opy_(bs_config, bstack1ll1ll1ll1_opy_)
            config = {
                bstack11ll111_opy_ (u"ࠬࡧࡵࡵࡪࠪḧ"): (bstack11llll1ll1l_opy_, bstack11llll11ll1_opy_),
                bstack11ll111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧḨ"): cls.default_headers()
            }
            response = bstack11ll111ll1_opy_(bstack11ll111_opy_ (u"ࠧࡑࡑࡖࡘࠬḩ"), cls.request_url(bstack11ll111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠲࠰ࡤࡸ࡭ࡱࡪࡳࠨḪ")), data, config)
            if response.status_code != 200:
                bstack1l1111l11l_opy_ = response.json()
                if bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪḫ")] == False:
                    cls.bstack1111l1lllll_opy_(bstack1l1111l11l_opy_)
                    return
                cls.bstack1111l1l11ll_opy_(bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḬ")])
                cls.bstack1111ll111ll_opy_(bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫḭ")])
                return None
            bstack1111l1l1l1l_opy_ = cls.bstack1111l1l111l_opy_(response)
            return bstack1111l1l1l1l_opy_, response.json()
        except Exception as error:
            logger.error(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥḮ").format(str(error)))
            return None
    @classmethod
    @bstack111l1ll11l_opy_(class_method=True)
    def stop(cls, bstack1111l1ll111_opy_=None):
        if not bstack11ll11ll11_opy_.on() and not bstack1ll11llll1_opy_.on():
            return
        if os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪḯ")) == bstack11ll111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧḰ") or os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ḱ")) == bstack11ll111_opy_ (u"ࠤࡱࡹࡱࡲࠢḲ"):
            logger.error(bstack11ll111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ḳ"))
            return {
                bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫḴ"): bstack11ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫḵ"),
                bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧḶ"): bstack11ll111_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬḷ")
            }
        try:
            cls.bstack111l111llll_opy_.shutdown()
            data = {
                bstack11ll111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭Ḹ"): bstack1l1l1llll_opy_()
            }
            if not bstack1111l1ll111_opy_ is None:
                data[bstack11ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭ḹ")] = [{
                    bstack11ll111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪḺ"): bstack11ll111_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩḻ"),
                    bstack11ll111_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬḼ"): bstack1111l1ll111_opy_
                }]
            config = {
                bstack11ll111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧḽ"): cls.default_headers()
            }
            bstack11l1l1ll1l1_opy_ = bstack11ll111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨḾ").format(os.environ[bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨḿ")])
            bstack1111l1l1111_opy_ = cls.request_url(bstack11l1l1ll1l1_opy_)
            response = bstack11ll111ll1_opy_(bstack11ll111_opy_ (u"ࠩࡓ࡙࡙࠭Ṁ"), bstack1111l1l1111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11ll111_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤṁ"))
        except Exception as error:
            logger.error(bstack11ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣṂ") + str(error))
            return {
                bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬṃ"): bstack11ll111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬṄ"),
                bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨṅ"): str(error)
            }
    @classmethod
    @bstack111l1ll11l_opy_(class_method=True)
    def bstack1111l1l111l_opy_(cls, response):
        bstack1l1111l11l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111l1l1l1l_opy_ = {}
        if bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"ࠨ࡬ࡺࡸࠬṆ")) is None:
            os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ṇ")] = bstack11ll111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨṈ")
        else:
            os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨṉ")] = bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"ࠬࡰࡷࡵࠩṊ"), bstack11ll111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫṋ"))
        os.environ[bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬṌ")] = bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪṍ"), bstack11ll111_opy_ (u"ࠩࡱࡹࡱࡲࠧṎ"))
        logger.info(bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࡩࡷࡥࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨṏ") + os.getenv(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩṐ")));
        if bstack11ll11ll11_opy_.bstack1111ll11l11_opy_(cls.bs_config, cls.bstack1ll1ll1ll1_opy_.get(bstack11ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ṑ"), bstack11ll111_opy_ (u"࠭ࠧṒ"))) is True:
            bstack111l1111l1l_opy_, build_hashed_id, bstack1111ll11l1l_opy_ = cls.bstack1111l1l1ll1_opy_(bstack1l1111l11l_opy_)
            if bstack111l1111l1l_opy_ != None and build_hashed_id != None:
                bstack1111l1l1l1l_opy_[bstack11ll111_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧṓ")] = {
                    bstack11ll111_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫṔ"): bstack111l1111l1l_opy_,
                    bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫṕ"): build_hashed_id,
                    bstack11ll111_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧṖ"): bstack1111ll11l1l_opy_
                }
            else:
                bstack1111l1l1l1l_opy_[bstack11ll111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫṗ")] = {}
        else:
            bstack1111l1l1l1l_opy_[bstack11ll111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬṘ")] = {}
        bstack1111ll111l1_opy_, build_hashed_id = cls.bstack1111l1ll1l1_opy_(bstack1l1111l11l_opy_)
        if bstack1111ll111l1_opy_ != None and build_hashed_id != None:
            bstack1111l1l1l1l_opy_[bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ṙ")] = {
                bstack11ll111_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫṚ"): bstack1111ll111l1_opy_,
                bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪṛ"): build_hashed_id,
            }
        else:
            bstack1111l1l1l1l_opy_[bstack11ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṜ")] = {}
        if bstack1111l1l1l1l_opy_[bstack11ll111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪṝ")].get(bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ṟ")) != None or bstack1111l1l1l1l_opy_[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṟ")].get(bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨṠ")) != None:
            cls.bstack1111l1l1lll_opy_(bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"ࠧ࡫ࡹࡷࠫṡ")), bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪṢ")))
        return bstack1111l1l1l1l_opy_
    @classmethod
    def bstack1111l1l1ll1_opy_(cls, bstack1l1111l11l_opy_):
        if bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩṣ")) == None:
            cls.bstack1111l1l11ll_opy_()
            return [None, None, None]
        if bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪṤ")][bstack11ll111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬṥ")] != True:
            cls.bstack1111l1l11ll_opy_(bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬṦ")])
            return [None, None, None]
        logger.debug(bstack11ll111_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪṧ"))
        os.environ[bstack11ll111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭Ṩ")] = bstack11ll111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ṩ")
        if bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"ࠩ࡭ࡻࡹ࠭Ṫ")):
            os.environ[bstack11ll111_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧṫ")] = json.dumps({
                bstack11ll111_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭Ṭ"): bstack11llll11111_opy_(cls.bs_config),
                bstack11ll111_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧṭ"): bstack11lll1l1l11_opy_(cls.bs_config)
            })
        if bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨṮ")):
            os.environ[bstack11ll111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ṯ")] = bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪṰ")]
        if bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩṱ")].get(bstack11ll111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫṲ"), {}).get(bstack11ll111_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨṳ")):
            os.environ[bstack11ll111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭Ṵ")] = str(bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ṵ")][bstack11ll111_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṶ")][bstack11ll111_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬṷ")])
        else:
            os.environ[bstack11ll111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪṸ")] = bstack11ll111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣṹ")
        return [bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠫ࡯ࡽࡴࠨṺ")], bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧṻ")], os.environ[bstack11ll111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧṼ")]]
    @classmethod
    def bstack1111l1ll1l1_opy_(cls, bstack1l1111l11l_opy_):
        if bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧṽ")) == None:
            cls.bstack1111ll111ll_opy_()
            return [None, None]
        if bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṾ")][bstack11ll111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪṿ")] != True:
            cls.bstack1111ll111ll_opy_(bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪẀ")])
            return [None, None]
        if bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫẁ")].get(bstack11ll111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭Ẃ")):
            logger.debug(bstack11ll111_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪẃ"))
            parsed = json.loads(os.getenv(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨẄ"), bstack11ll111_opy_ (u"ࠨࡽࢀࠫẅ")))
            capabilities = bstack1l11lll111_opy_.bstack1111ll1l11l_opy_(bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩẆ")][bstack11ll111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫẇ")][bstack11ll111_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪẈ")], bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪẉ"), bstack11ll111_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬẊ"))
            bstack1111ll111l1_opy_ = capabilities[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬẋ")]
            os.environ[bstack11ll111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭Ẍ")] = bstack1111ll111l1_opy_
            if bstack11ll111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦẍ") in bstack1l1111l11l_opy_ and bstack1l1111l11l_opy_.get(bstack11ll111_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤẎ")) is None:
                parsed[bstack11ll111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬẏ")] = capabilities[bstack11ll111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ẑ")]
            os.environ[bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧẑ")] = json.dumps(parsed)
            scripts = bstack1l11lll111_opy_.bstack1111ll1l11l_opy_(bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧẒ")][bstack11ll111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩẓ")][bstack11ll111_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪẔ")], bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨẕ"), bstack11ll111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࠬẖ"))
            bstack1l11ll111l_opy_.bstack11ll111l1l_opy_(scripts)
            commands = bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬẗ")][bstack11ll111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧẘ")][bstack11ll111_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࡖࡲ࡛ࡷࡧࡰࠨẙ")].get(bstack11ll111_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪẚ"))
            bstack1l11ll111l_opy_.bstack11lll1lll11_opy_(commands)
            bstack1l11ll111l_opy_.store()
        return [bstack1111ll111l1_opy_, bstack1l1111l11l_opy_[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫẛ")]]
    @classmethod
    def bstack1111l1l11ll_opy_(cls, response=None):
        os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨẜ")] = bstack11ll111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩẝ")
        os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩẞ")] = bstack11ll111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫẟ")
        os.environ[bstack11ll111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭Ạ")] = bstack11ll111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧạ")
        os.environ[bstack11ll111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨẢ")] = bstack11ll111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣả")
        os.environ[bstack11ll111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬẤ")] = bstack11ll111_opy_ (u"ࠧࡴࡵ࡭࡮ࠥấ")
        cls.bstack1111l1lllll_opy_(response, bstack11ll111_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨẦ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll111ll_opy_(cls, response=None):
        os.environ[bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬầ")] = bstack11ll111_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ẩ")
        os.environ[bstack11ll111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧẩ")] = bstack11ll111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨẪ")
        os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨẫ")] = bstack11ll111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪẬ")
        cls.bstack1111l1lllll_opy_(response, bstack11ll111_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨậ"))
        return [None, None, None]
    @classmethod
    def bstack1111l1l1lll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫẮ")] = jwt
        os.environ[bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ắ")] = build_hashed_id
    @classmethod
    def bstack1111l1lllll_opy_(cls, response=None, product=bstack11ll111_opy_ (u"ࠤࠥẰ")):
        if response == None or response.get(bstack11ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪằ")) == None:
            logger.error(product + bstack11ll111_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨẲ"))
            return
        for error in response[bstack11ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬẳ")]:
            bstack11l1l111lll_opy_ = error[bstack11ll111_opy_ (u"࠭࡫ࡦࡻࠪẴ")]
            error_message = error[bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨẵ")]
            if error_message:
                if bstack11l1l111lll_opy_ == bstack11ll111_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠢẶ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11ll111_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥặ") + product + bstack11ll111_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣẸ"))
    @classmethod
    def bstack1111ll11ll1_opy_(cls):
        if cls.bstack111l111llll_opy_ is not None:
            return
        cls.bstack111l111llll_opy_ = bstack111l11l11l1_opy_(cls.bstack1111l1l11l1_opy_)
        cls.bstack111l111llll_opy_.start()
    @classmethod
    def bstack111ll1l111_opy_(cls):
        if cls.bstack111l111llll_opy_ is None:
            return
        cls.bstack111l111llll_opy_.shutdown()
    @classmethod
    @bstack111l1ll11l_opy_(class_method=True)
    def bstack1111l1l11l1_opy_(cls, bstack111l1l11l1_opy_, event_url=bstack11ll111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪẹ")):
        config = {
            bstack11ll111_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭Ẻ"): cls.default_headers()
        }
        logger.debug(bstack11ll111_opy_ (u"ࠨࡰࡰࡵࡷࡣࡩࡧࡴࡢ࠼ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡵࠣࡿࢂࠨẻ").format(bstack11ll111_opy_ (u"ࠧ࠭ࠢࠪẼ").join([event[bstack11ll111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬẽ")] for event in bstack111l1l11l1_opy_])))
        response = bstack11ll111ll1_opy_(bstack11ll111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧẾ"), cls.request_url(event_url), bstack111l1l11l1_opy_, config)
        bstack11llll1l11l_opy_ = response.json()
    @classmethod
    def bstack1l1111ll1_opy_(cls, bstack111l1l11l1_opy_, event_url=bstack11ll111_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩế")):
        logger.debug(bstack11ll111_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡣࡧࡨࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦỀ").format(bstack111l1l11l1_opy_[bstack11ll111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩề")]))
        if not bstack1l11lll111_opy_.bstack1111ll1l111_opy_(bstack111l1l11l1_opy_[bstack11ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪỂ")]):
            logger.debug(bstack11ll111_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡓࡵࡴࠡࡣࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧể").format(bstack111l1l11l1_opy_[bstack11ll111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬỄ")]))
            return
        bstack1l1l1l1ll_opy_ = bstack1l11lll111_opy_.bstack1111l1l1l11_opy_(bstack111l1l11l1_opy_[bstack11ll111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ễ")], bstack111l1l11l1_opy_.get(bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬỆ")))
        if bstack1l1l1l1ll_opy_ != None:
            if bstack111l1l11l1_opy_.get(bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ệ")) != None:
                bstack111l1l11l1_opy_[bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧỈ")][bstack11ll111_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫỉ")] = bstack1l1l1l1ll_opy_
            else:
                bstack111l1l11l1_opy_[bstack11ll111_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬỊ")] = bstack1l1l1l1ll_opy_
        if event_url == bstack11ll111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧị"):
            cls.bstack1111ll11ll1_opy_()
            logger.debug(bstack11ll111_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧỌ").format(bstack111l1l11l1_opy_[bstack11ll111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧọ")]))
            cls.bstack111l111llll_opy_.add(bstack111l1l11l1_opy_)
        elif event_url == bstack11ll111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩỎ"):
            cls.bstack1111l1l11l1_opy_([bstack111l1l11l1_opy_], event_url)
    @classmethod
    @bstack111l1ll11l_opy_(class_method=True)
    def bstack1l1ll1l111_opy_(cls, logs):
        bstack1111ll1l1l1_opy_ = []
        for log in logs:
            bstack1111l1llll1_opy_ = {
                bstack11ll111_opy_ (u"ࠬࡱࡩ࡯ࡦࠪỏ"): bstack11ll111_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨỐ"),
                bstack11ll111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ố"): log[bstack11ll111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧỒ")],
                bstack11ll111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬồ"): log[bstack11ll111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ổ")],
                bstack11ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫổ"): {},
                bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ỗ"): log[bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧỗ")],
            }
            if bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧỘ") in log:
                bstack1111l1llll1_opy_[bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨộ")] = log[bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩỚ")]
            elif bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪớ") in log:
                bstack1111l1llll1_opy_[bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫỜ")] = log[bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬờ")]
            bstack1111ll1l1l1_opy_.append(bstack1111l1llll1_opy_)
        cls.bstack1l1111ll1_opy_({
            bstack11ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪỞ"): bstack11ll111_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫở"),
            bstack11ll111_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭Ỡ"): bstack1111ll1l1l1_opy_
        })
    @classmethod
    @bstack111l1ll11l_opy_(class_method=True)
    def bstack1111ll1111l_opy_(cls, steps):
        bstack1111ll11111_opy_ = []
        for step in steps:
            bstack1111l1ll11l_opy_ = {
                bstack11ll111_opy_ (u"ࠩ࡮࡭ࡳࡪࠧỡ"): bstack11ll111_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭Ợ"),
                bstack11ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪợ"): step[bstack11ll111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫỤ")],
                bstack11ll111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩụ"): step[bstack11ll111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪỦ")],
                bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩủ"): step[bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪỨ")],
                bstack11ll111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬứ"): step[bstack11ll111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭Ừ")]
            }
            if bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬừ") in step:
                bstack1111l1ll11l_opy_[bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ử")] = step[bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧử")]
            elif bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨỮ") in step:
                bstack1111l1ll11l_opy_[bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩữ")] = step[bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪỰ")]
            bstack1111ll11111_opy_.append(bstack1111l1ll11l_opy_)
        cls.bstack1l1111ll1_opy_({
            bstack11ll111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨự"): bstack11ll111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩỲ"),
            bstack11ll111_opy_ (u"࠭࡬ࡰࡩࡶࠫỳ"): bstack1111ll11111_opy_
        })
    @classmethod
    @bstack111l1ll11l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l1ll1ll1_opy_, stage=STAGE.bstack111lllll_opy_)
    def bstack11111l1l_opy_(cls, screenshot):
        cls.bstack1l1111ll1_opy_({
            bstack11ll111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫỴ"): bstack11ll111_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬỵ"),
            bstack11ll111_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧỶ"): [{
                bstack11ll111_opy_ (u"ࠪ࡯࡮ࡴࡤࠨỷ"): bstack11ll111_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭Ỹ"),
                bstack11ll111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨỹ"): datetime.datetime.utcnow().isoformat() + bstack11ll111_opy_ (u"࡚࠭ࠨỺ"),
                bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨỻ"): screenshot[bstack11ll111_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧỼ")],
                bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩỽ"): screenshot[bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪỾ")]
            }]
        }, event_url=bstack11ll111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩỿ"))
    @classmethod
    @bstack111l1ll11l_opy_(class_method=True)
    def bstack1ll1llll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1111ll1_opy_({
            bstack11ll111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩἀ"): bstack11ll111_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪἁ"),
            bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩἂ"): {
                bstack11ll111_opy_ (u"ࠣࡷࡸ࡭ࡩࠨἃ"): cls.current_test_uuid(),
                bstack11ll111_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣἄ"): cls.bstack111lllll1l_opy_(driver)
            }
        })
    @classmethod
    def bstack111llll1ll_opy_(cls, event: str, bstack111l1l11l1_opy_: bstack111ll11l1l_opy_):
        bstack111l1ll1l1_opy_ = {
            bstack11ll111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧἅ"): event,
            bstack111l1l11l1_opy_.bstack111l1l11ll_opy_(): bstack111l1l11l1_opy_.bstack111l1ll1ll_opy_(event)
        }
        cls.bstack1l1111ll1_opy_(bstack111l1ll1l1_opy_)
        result = getattr(bstack111l1l11l1_opy_, bstack11ll111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫἆ"), None)
        if event == bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ἇ"):
            threading.current_thread().bstackTestMeta = {bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ἀ"): bstack11ll111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨἉ")}
        elif event == bstack11ll111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪἊ"):
            threading.current_thread().bstackTestMeta = {bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩἋ"): getattr(result, bstack11ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪἌ"), bstack11ll111_opy_ (u"ࠫࠬἍ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩἎ"), None) is None or os.environ[bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪἏ")] == bstack11ll111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧἐ")) and (os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ἑ"), None) is None or os.environ[bstack11ll111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧἒ")] == bstack11ll111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣἓ")):
            return False
        return True
    @staticmethod
    def bstack1111l1lll11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111ll11ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11ll111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪἔ"): bstack11ll111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨἕ"),
            bstack11ll111_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩ἖"): bstack11ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬ἗")
        }
        if os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬἘ"), None):
            headers[bstack11ll111_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩἙ")] = bstack11ll111_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭Ἒ").format(os.environ[bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠣἛ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11ll111_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫἜ").format(bstack1111l1lll1l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪἝ"), None)
    @staticmethod
    def bstack111lllll1l_opy_(driver):
        return {
            bstack11l11ll1l11_opy_(): bstack11l11ll11l1_opy_(driver)
        }
    @staticmethod
    def bstack1111ll11lll_opy_(exception_info, report):
        return [{bstack11ll111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ἞"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111l1l11l_opy_(typename):
        if bstack11ll111_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ἟") in typename:
            return bstack11ll111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥἠ")
        return bstack11ll111_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦἡ")