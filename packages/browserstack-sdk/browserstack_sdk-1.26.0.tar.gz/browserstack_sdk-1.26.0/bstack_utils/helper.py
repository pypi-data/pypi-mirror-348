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
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll1l1ll11_opy_, bstack1l1ll1l1ll_opy_, bstack1lll1l111l_opy_, bstack1lll111l11_opy_,
                                    bstack11ll1ll1l11_opy_, bstack11ll1l111l1_opy_, bstack11ll11l1lll_opy_, bstack11ll1l111ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1l1lll_opy_, bstack11lll1llll_opy_
from bstack_utils.proxy import bstack111lllll1_opy_, bstack111111lll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1l1ll11l_opy_
from browserstack_sdk._version import __version__
bstack11lll1l1l_opy_ = Config.bstack11l11l1l11_opy_()
logger = bstack1l1l1ll11l_opy_.get_logger(__name__, bstack1l1l1ll11l_opy_.bstack1ll1lll11ll_opy_())
def bstack11llll11111_opy_(config):
    return config[bstack11ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᧁ")]
def bstack11lll1l1l11_opy_(config):
    return config[bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᧂ")]
def bstack1l1111ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11ll11l11l1_opy_(obj):
    values = []
    bstack11ll11111l1_opy_ = re.compile(bstack11ll111_opy_ (u"ࡳࠤࡡࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࡝ࡦ࠮ࠨࠧᧃ"), re.I)
    for key in obj.keys():
        if bstack11ll11111l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1ll1l1ll_opy_(config):
    tags = []
    tags.extend(bstack11ll11l11l1_opy_(os.environ))
    tags.extend(bstack11ll11l11l1_opy_(config))
    return tags
def bstack11ll111ll1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1llll1ll_opy_(bstack11l11ll1ll1_opy_):
    if not bstack11l11ll1ll1_opy_:
        return bstack11ll111_opy_ (u"ࠩࠪᧄ")
    return bstack11ll111_opy_ (u"ࠥࡿࢂࠦࠨࡼࡿࠬࠦᧅ").format(bstack11l11ll1ll1_opy_.name, bstack11l11ll1ll1_opy_.email)
def bstack11lll1l11l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1l11ll1l_opy_ = repo.common_dir
        info = {
            bstack11ll111_opy_ (u"ࠦࡸ࡮ࡡࠣᧆ"): repo.head.commit.hexsha,
            bstack11ll111_opy_ (u"ࠧࡹࡨࡰࡴࡷࡣࡸ࡮ࡡࠣᧇ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11ll111_opy_ (u"ࠨࡢࡳࡣࡱࡧ࡭ࠨᧈ"): repo.active_branch.name,
            bstack11ll111_opy_ (u"ࠢࡵࡣࡪࠦᧉ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11ll111_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࠦ᧊"): bstack11l1llll1ll_opy_(repo.head.commit.committer),
            bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࡤࡪࡡࡵࡧࠥ᧋"): repo.head.commit.committed_datetime.isoformat(),
            bstack11ll111_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࠥ᧌"): bstack11l1llll1ll_opy_(repo.head.commit.author),
            bstack11ll111_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡣࡩࡧࡴࡦࠤ᧍"): repo.head.commit.authored_datetime.isoformat(),
            bstack11ll111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᧎"): repo.head.commit.message,
            bstack11ll111_opy_ (u"ࠨࡲࡰࡱࡷࠦ᧏"): repo.git.rev_parse(bstack11ll111_opy_ (u"ࠢ࠮࠯ࡶ࡬ࡴࡽ࠭ࡵࡱࡳࡰࡪࡼࡥ࡭ࠤ᧐")),
            bstack11ll111_opy_ (u"ࠣࡥࡲࡱࡲࡵ࡮ࡠࡩ࡬ࡸࡤࡪࡩࡳࠤ᧑"): bstack11l1l11ll1l_opy_,
            bstack11ll111_opy_ (u"ࠤࡺࡳࡷࡱࡴࡳࡧࡨࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ᧒"): subprocess.check_output([bstack11ll111_opy_ (u"ࠥ࡫࡮ࡺࠢ᧓"), bstack11ll111_opy_ (u"ࠦࡷ࡫ࡶ࠮ࡲࡤࡶࡸ࡫ࠢ᧔"), bstack11ll111_opy_ (u"ࠧ࠳࠭ࡨ࡫ࡷ࠱ࡨࡵ࡭࡮ࡱࡱ࠱ࡩ࡯ࡲࠣ᧕")]).strip().decode(
                bstack11ll111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᧖")),
            bstack11ll111_opy_ (u"ࠢ࡭ࡣࡶࡸࡤࡺࡡࡨࠤ᧗"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11ll111_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡴࡡࡶ࡭ࡳࡩࡥࡠ࡮ࡤࡷࡹࡥࡴࡢࡩࠥ᧘"): repo.git.rev_list(
                bstack11ll111_opy_ (u"ࠤࡾࢁ࠳࠴ࡻࡾࠤ᧙").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l11lll1ll_opy_ = []
        for remote in remotes:
            bstack11ll1111ll1_opy_ = {
                bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᧚"): remote.name,
                bstack11ll111_opy_ (u"ࠦࡺࡸ࡬ࠣ᧛"): remote.url,
            }
            bstack11l11lll1ll_opy_.append(bstack11ll1111ll1_opy_)
        bstack11l1llll1l1_opy_ = {
            bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᧜"): bstack11ll111_opy_ (u"ࠨࡧࡪࡶࠥ᧝"),
            **info,
            bstack11ll111_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫ࡳࠣ᧞"): bstack11l11lll1ll_opy_
        }
        bstack11l1llll1l1_opy_ = bstack11l1ll11lll_opy_(bstack11l1llll1l1_opy_)
        return bstack11l1llll1l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ᧟").format(err))
        return {}
def bstack11l1ll11lll_opy_(bstack11l1llll1l1_opy_):
    bstack11l1l1l111l_opy_ = bstack11l1l111l11_opy_(bstack11l1llll1l1_opy_)
    if bstack11l1l1l111l_opy_ and bstack11l1l1l111l_opy_ > bstack11ll1ll1l11_opy_:
        bstack11l11llll11_opy_ = bstack11l1l1l111l_opy_ - bstack11ll1ll1l11_opy_
        bstack11l1l111l1l_opy_ = bstack11l11ll111l_opy_(bstack11l1llll1l1_opy_[bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥ᧠")], bstack11l11llll11_opy_)
        bstack11l1llll1l1_opy_[bstack11ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦ᧡")] = bstack11l1l111l1l_opy_
        logger.info(bstack11ll111_opy_ (u"࡙ࠦ࡮ࡥࠡࡥࡲࡱࡲ࡯ࡴࠡࡪࡤࡷࠥࡨࡥࡦࡰࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩ࠴ࠠࡔ࡫ࡽࡩࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࠡࡣࡩࡸࡪࡸࠠࡵࡴࡸࡲࡨࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡼࡿࠣࡏࡇࠨ᧢")
                    .format(bstack11l1l111l11_opy_(bstack11l1llll1l1_opy_) / 1024))
    return bstack11l1llll1l1_opy_
def bstack11l1l111l11_opy_(bstack1ll1lllll_opy_):
    try:
        if bstack1ll1lllll_opy_:
            bstack11l11lll1l1_opy_ = json.dumps(bstack1ll1lllll_opy_)
            bstack11ll111111l_opy_ = sys.getsizeof(bstack11l11lll1l1_opy_)
            return bstack11ll111111l_opy_
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡨࡧ࡬ࡤࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡎࡘࡕࡎࠡࡱࡥ࡮ࡪࡩࡴ࠻ࠢࡾࢁࠧ᧣").format(e))
    return -1
def bstack11l11ll111l_opy_(field, bstack11l1l1l11l1_opy_):
    try:
        bstack11l1l1l1111_opy_ = len(bytes(bstack11ll1l111l1_opy_, bstack11ll111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᧤")))
        bstack11l1llll11l_opy_ = bytes(field, bstack11ll111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᧥"))
        bstack11l1l11l111_opy_ = len(bstack11l1llll11l_opy_)
        bstack11l1ll11111_opy_ = ceil(bstack11l1l11l111_opy_ - bstack11l1l1l11l1_opy_ - bstack11l1l1l1111_opy_)
        if bstack11l1ll11111_opy_ > 0:
            bstack11l11ll1111_opy_ = bstack11l1llll11l_opy_[:bstack11l1ll11111_opy_].decode(bstack11ll111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᧦"), errors=bstack11ll111_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࠩ᧧")) + bstack11ll1l111l1_opy_
            return bstack11l11ll1111_opy_
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩࡦ࡮ࡧ࠰ࠥࡴ࡯ࡵࡪ࡬ࡲ࡬ࠦࡷࡢࡵࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩࠦࡨࡦࡴࡨ࠾ࠥࢁࡽࠣ᧨").format(e))
    return field
def bstack11lll1ll1_opy_():
    env = os.environ
    if (bstack11ll111_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤ᧩") in env and len(env[bstack11ll111_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥ᧪")]) > 0) or (
            bstack11ll111_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧ᧫") in env and len(env[bstack11ll111_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨ᧬")]) > 0):
        return {
            bstack11ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨ᧭"): bstack11ll111_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥ᧮"),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᧯"): env.get(bstack11ll111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᧰")),
            bstack11ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᧱"): env.get(bstack11ll111_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣ᧲")),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᧳"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᧴"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠤࡆࡍࠧ᧵")) == bstack11ll111_opy_ (u"ࠥࡸࡷࡻࡥࠣ᧶") and bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨ᧷"))):
        return {
            bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᧸"): bstack11ll111_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣ᧹"),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᧺"): env.get(bstack11ll111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᧻")),
            bstack11ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᧼"): env.get(bstack11ll111_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢ᧽")),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᧾"): env.get(bstack11ll111_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣ᧿"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠨࡃࡊࠤᨀ")) == bstack11ll111_opy_ (u"ࠢࡵࡴࡸࡩࠧᨁ") and bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣᨂ"))):
        return {
            bstack11ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨃ"): bstack11ll111_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨᨄ"),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨅ"): env.get(bstack11ll111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧᨆ")),
            bstack11ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨇ"): env.get(bstack11ll111_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᨈ")),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨉ"): env.get(bstack11ll111_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᨊ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠥࡇࡎࠨᨋ")) == bstack11ll111_opy_ (u"ࠦࡹࡸࡵࡦࠤᨌ") and env.get(bstack11ll111_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᨍ")) == bstack11ll111_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᨎ"):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨏ"): bstack11ll111_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᨐ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᨑ"): None,
            bstack11ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᨒ"): None,
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨓ"): None
        }
    if env.get(bstack11ll111_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᨔ")) and env.get(bstack11ll111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᨕ")):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨖ"): bstack11ll111_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦᨗ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰᨘࠧ"): env.get(bstack11ll111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣᨙ")),
            bstack11ll111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨚ"): None,
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᨛ"): env.get(bstack11ll111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᨜"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠢࡄࡋࠥ᨝")) == bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨ᨞") and bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣ᨟"))):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᨠ"): bstack11ll111_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥᨡ"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᨢ"): env.get(bstack11ll111_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤᨣ")),
            bstack11ll111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨤ"): None,
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨥ"): env.get(bstack11ll111_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᨦ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠥࡇࡎࠨᨧ")) == bstack11ll111_opy_ (u"ࠦࡹࡸࡵࡦࠤᨨ") and bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᨩ"))):
        return {
            bstack11ll111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᨪ"): bstack11ll111_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥᨫ"),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᨬ"): env.get(bstack11ll111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᨭ")),
            bstack11ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᨮ"): env.get(bstack11ll111_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᨯ")),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᨰ"): env.get(bstack11ll111_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤᨱ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠢࡄࡋࠥᨲ")) == bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨᨳ") and bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧᨴ"))):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᨵ"): bstack11ll111_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦᨶ"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᨷ"): env.get(bstack11ll111_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥᨸ")),
            bstack11ll111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨹ"): env.get(bstack11ll111_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᨺ")),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨻ"): env.get(bstack11ll111_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨᨼ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠦࡈࡏࠢᨽ")) == bstack11ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥᨾ") and bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤᨿ"))):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩀ"): bstack11ll111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦᩁ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩂ"): env.get(bstack11ll111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᩃ")),
            bstack11ll111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩄ"): env.get(bstack11ll111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢᩅ")) or env.get(bstack11ll111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᩆ")),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᩇ"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᩈ"))
        }
    if bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᩉ"))):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᩊ"): bstack11ll111_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦᩋ"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᩌ"): bstack11ll111_opy_ (u"ࠨࡻࡾࡽࢀࠦᩍ").format(env.get(bstack11ll111_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᩎ")), env.get(bstack11ll111_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨᩏ"))),
            bstack11ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᩐ"): env.get(bstack11ll111_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤᩑ")),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᩒ"): env.get(bstack11ll111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᩓ"))
        }
    if bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣᩔ"))):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩕ"): bstack11ll111_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥᩖ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩗ"): bstack11ll111_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤᩘ").format(env.get(bstack11ll111_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪᩙ")), env.get(bstack11ll111_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ᩚ")), env.get(bstack11ll111_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧᩛ")), env.get(bstack11ll111_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫᩜ"))),
            bstack11ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᩝ"): env.get(bstack11ll111_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᩞ")),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᩟"): env.get(bstack11ll111_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖ᩠ࠧ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨᩡ")) and env.get(bstack11ll111_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᩢ")):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩣ"): bstack11ll111_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥᩤ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩥ"): bstack11ll111_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨᩦ").format(env.get(bstack11ll111_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᩧ")), env.get(bstack11ll111_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪᩨ")), env.get(bstack11ll111_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ᩩ"))),
            bstack11ll111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᩪ"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᩫ")),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᩬ"): env.get(bstack11ll111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᩭ"))
        }
    if any([env.get(bstack11ll111_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᩮ")), env.get(bstack11ll111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᩯ")), env.get(bstack11ll111_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᩰ"))]):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩱ"): bstack11ll111_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣᩲ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩳ"): env.get(bstack11ll111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᩴ")),
            bstack11ll111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᩵"): env.get(bstack11ll111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᩶")),
            bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᩷"): env.get(bstack11ll111_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᩸"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨ᩹")):
        return {
            bstack11ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᩺"): bstack11ll111_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥ᩻"),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᩼"): env.get(bstack11ll111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢ᩽")),
            bstack11ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᩾"): env.get(bstack11ll111_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨ᩿")),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᪀"): env.get(bstack11ll111_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢ᪁"))
        }
    if env.get(bstack11ll111_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦ᪂")) or env.get(bstack11ll111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ᪃")):
        return {
            bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪄"): bstack11ll111_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢ᪅"),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪆"): env.get(bstack11ll111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᪇")),
            bstack11ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪈"): bstack11ll111_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥ᪉") if env.get(bstack11ll111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ᪊")) else None,
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪋"): env.get(bstack11ll111_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦ᪌"))
        }
    if any([env.get(bstack11ll111_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧ᪍")), env.get(bstack11ll111_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤ᪎")), env.get(bstack11ll111_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤ᪏"))]):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪐"): bstack11ll111_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥ᪑"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪒"): None,
            bstack11ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᪓"): env.get(bstack11ll111_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦ᪔")),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᪕"): env.get(bstack11ll111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᪖"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨ᪗")):
        return {
            bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪘"): bstack11ll111_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣ᪙"),
            bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪚"): env.get(bstack11ll111_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᪛")),
            bstack11ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪜"): bstack11ll111_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥ᪝").format(env.get(bstack11ll111_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭᪞"))) if env.get(bstack11ll111_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ᪟")) else None,
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪠"): env.get(bstack11ll111_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᪡"))
        }
    if bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣ᪢"))):
        return {
            bstack11ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪣"): bstack11ll111_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥ᪤"),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪥"): env.get(bstack11ll111_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣ᪦")),
            bstack11ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᪧ"): env.get(bstack11ll111_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤ᪨")),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪩"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᪪"))
        }
    if bstack11lll11ll_opy_(env.get(bstack11ll111_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥ᪫"))):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪬"): bstack11ll111_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧ᪭"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪮"): bstack11ll111_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢ᪯").format(env.get(bstack11ll111_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫ᪰")), env.get(bstack11ll111_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬ᪱")), env.get(bstack11ll111_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩ᪲"))),
            bstack11ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪳"): env.get(bstack11ll111_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨ᪴")),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵ᪵ࠦ"): env.get(bstack11ll111_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨ᪶"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠢࡄࡋ᪷ࠥ")) == bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨ᪸") and env.get(bstack11ll111_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤ᪹")) == bstack11ll111_opy_ (u"ࠥ࠵᪺ࠧ"):
        return {
            bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪻"): bstack11ll111_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧ᪼"),
            bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪽"): bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥ᪾").format(env.get(bstack11ll111_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐᪿࠬ"))),
            bstack11ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨᫀࠦ"): None,
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫁"): None,
        }
    if env.get(bstack11ll111_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢ᫂")):
        return {
            bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧ᫃ࠥ"): bstack11ll111_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹ᫄ࠣ"),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᫅"): None,
            bstack11ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫆"): env.get(bstack11ll111_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥ᫇")),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫈"): env.get(bstack11ll111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᫉"))
        }
    if any([env.get(bstack11ll111_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅ᫊ࠣ")), env.get(bstack11ll111_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨ᫋")), env.get(bstack11ll111_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧᫌ")), env.get(bstack11ll111_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤᫍ"))]):
        return {
            bstack11ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᫎ"): bstack11ll111_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨ᫏"),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᫐"): None,
            bstack11ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᫑"): env.get(bstack11ll111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᫒")) or None,
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᫓"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᫔"), 0)
        }
    if env.get(bstack11ll111_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᫕")):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫖"): bstack11ll111_opy_ (u"ࠦࡌࡵࡃࡅࠤ᫗"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᫘"): None,
            bstack11ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᫙"): env.get(bstack11ll111_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᫚")),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᫛"): env.get(bstack11ll111_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣ᫜"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᫝")):
        return {
            bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᫞"): bstack11ll111_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣ᫟"),
            bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᫠"): env.get(bstack11ll111_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᫡")),
            bstack11ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫢"): env.get(bstack11ll111_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧ᫣")),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫤"): env.get(bstack11ll111_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ᫥"))
        }
    return {bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᫦"): None}
def get_host_info():
    return {
        bstack11ll111_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣ᫧"): platform.node(),
        bstack11ll111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ᫨"): platform.system(),
        bstack11ll111_opy_ (u"ࠣࡶࡼࡴࡪࠨ᫩"): platform.machine(),
        bstack11ll111_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥ᫪"): platform.version(),
        bstack11ll111_opy_ (u"ࠥࡥࡷࡩࡨࠣ᫫"): platform.architecture()[0]
    }
def bstack111111l11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11ll1l11_opy_():
    if bstack11lll1l1l_opy_.get_property(bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ᫬")):
        return bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᫭")
    return bstack11ll111_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬ᫮")
def bstack11l11ll11l1_opy_(driver):
    info = {
        bstack11ll111_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᫯"): driver.capabilities,
        bstack11ll111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬ᫰"): driver.session_id,
        bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ᫱"): driver.capabilities.get(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᫲"), None),
        bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᫳"): driver.capabilities.get(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᫴"), None),
        bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᫵"): driver.capabilities.get(bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭᫶"), None),
        bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᫷"):driver.capabilities.get(bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ᫸"), None),
    }
    if bstack11l11ll1l11_opy_() == bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᫹"):
        if bstack11l1l1l11l_opy_():
            info[bstack11ll111_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ᫺")] = bstack11ll111_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᫻")
        elif driver.capabilities.get(bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᫼"), {}).get(bstack11ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ᫽"), False):
            info[bstack11ll111_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ᫾")] = bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭᫿")
        else:
            info[bstack11ll111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᬀ")] = bstack11ll111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᬁ")
    return info
def bstack11l1l1l11l_opy_():
    if bstack11lll1l1l_opy_.get_property(bstack11ll111_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᬂ")):
        return True
    if bstack11lll11ll_opy_(os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧᬃ"), None)):
        return True
    return False
def bstack11ll111ll1_opy_(bstack11l1l1111l1_opy_, url, data, config):
    headers = config.get(bstack11ll111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᬄ"), None)
    proxies = bstack111lllll1_opy_(config, url)
    auth = config.get(bstack11ll111_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᬅ"), None)
    response = requests.request(
            bstack11l1l1111l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll1111l1l_opy_(bstack1l1ll111l1_opy_, size):
    bstack1ll1ll111l_opy_ = []
    while len(bstack1l1ll111l1_opy_) > size:
        bstack1ll11ll1ll_opy_ = bstack1l1ll111l1_opy_[:size]
        bstack1ll1ll111l_opy_.append(bstack1ll11ll1ll_opy_)
        bstack1l1ll111l1_opy_ = bstack1l1ll111l1_opy_[size:]
    bstack1ll1ll111l_opy_.append(bstack1l1ll111l1_opy_)
    return bstack1ll1ll111l_opy_
def bstack11l1ll11l1l_opy_(message, bstack11l1lll11ll_opy_=False):
    os.write(1, bytes(message, bstack11ll111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᬆ")))
    os.write(1, bytes(bstack11ll111_opy_ (u"ࠪࡠࡳ࠭ᬇ"), bstack11ll111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᬈ")))
    if bstack11l1lll11ll_opy_:
        with open(bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫᬉ") + os.environ[bstack11ll111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᬊ")] + bstack11ll111_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬᬋ"), bstack11ll111_opy_ (u"ࠨࡣࠪᬌ")) as f:
            f.write(message + bstack11ll111_opy_ (u"ࠩ࡟ࡲࠬᬍ"))
def bstack1l1ll1ll1l1_opy_():
    return os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᬎ")].lower() == bstack11ll111_opy_ (u"ࠫࡹࡸࡵࡦࠩᬏ")
def bstack1l111ll1l_opy_(bstack11l1l1ll1l1_opy_):
    return bstack11ll111_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᬐ").format(bstack11ll1l1ll11_opy_, bstack11l1l1ll1l1_opy_)
def bstack1l1l1llll_opy_():
    return bstack111l11l1l1_opy_().replace(tzinfo=None).isoformat() + bstack11ll111_opy_ (u"࡚࠭ࠨᬑ")
def bstack11ll11l1l11_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11ll111_opy_ (u"࡛ࠧࠩᬒ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11ll111_opy_ (u"ࠨ࡜ࠪᬓ")))).total_seconds() * 1000
def bstack11ll11l1111_opy_(timestamp):
    return bstack11ll111l1l1_opy_(timestamp).isoformat() + bstack11ll111_opy_ (u"ࠩ࡝ࠫᬔ")
def bstack11l1l1lllll_opy_(bstack11l1llllll1_opy_):
    date_format = bstack11ll111_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨᬕ")
    bstack11l1ll11l11_opy_ = datetime.datetime.strptime(bstack11l1llllll1_opy_, date_format)
    return bstack11l1ll11l11_opy_.isoformat() + bstack11ll111_opy_ (u"ࠫ࡟࠭ᬖ")
def bstack11l1l1l11ll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᬗ")
    else:
        return bstack11ll111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᬘ")
def bstack11lll11ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬᬙ")
def bstack11l1ll1l1l1_opy_(val):
    return val.__str__().lower() == bstack11ll111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᬚ")
def bstack111l1ll11l_opy_(bstack11l1l111lll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l111lll_opy_ as e:
                print(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤᬛ").format(func.__name__, bstack11l1l111lll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11ll1lll_opy_(bstack11l1lllll1l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1lllll1l_opy_(cls, *args, **kwargs)
            except bstack11l1l111lll_opy_ as e:
                print(bstack11ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᬜ").format(bstack11l1lllll1l_opy_.__name__, bstack11l1l111lll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11ll1lll_opy_
    else:
        return decorator
def bstack111l11lll_opy_(bstack1111lll111_opy_):
    if os.getenv(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᬝ")) is not None:
        return bstack11lll11ll_opy_(os.getenv(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᬞ")))
    if bstack11ll111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᬟ") in bstack1111lll111_opy_ and bstack11l1ll1l1l1_opy_(bstack1111lll111_opy_[bstack11ll111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᬠ")]):
        return False
    if bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᬡ") in bstack1111lll111_opy_ and bstack11l1ll1l1l1_opy_(bstack1111lll111_opy_[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᬢ")]):
        return False
    return True
def bstack1ll1l1lll_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1l1lll11_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥᬣ"), None)
        return bstack11l1l1lll11_opy_ is None or bstack11l1l1lll11_opy_ == bstack11ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᬤ")
    except Exception as e:
        return False
def bstack11l1lll11l_opy_(hub_url, CONFIG):
    if bstack1l111l11l_opy_() <= version.parse(bstack11ll111_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬᬥ")):
        if hub_url:
            return bstack11ll111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᬦ") + hub_url + bstack11ll111_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦᬧ")
        return bstack1lll1l111l_opy_
    if hub_url:
        return bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᬨ") + hub_url + bstack11ll111_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥᬩ")
    return bstack1lll111l11_opy_
def bstack11l1l1ll11l_opy_():
    return isinstance(os.getenv(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩᬪ")), str)
def bstack1ll111111l_opy_(url):
    return urlparse(url).hostname
def bstack11ll11llll_opy_(hostname):
    for bstack1ll11l11ll_opy_ in bstack1l1ll1l1ll_opy_:
        regex = re.compile(bstack1ll11l11ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l11l1ll_opy_(bstack11l11ll1l1l_opy_, file_name, logger):
    bstack11l1l11l1l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠫࢃ࠭ᬫ")), bstack11l11ll1l1l_opy_)
    try:
        if not os.path.exists(bstack11l1l11l1l_opy_):
            os.makedirs(bstack11l1l11l1l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠬࢄࠧᬬ")), bstack11l11ll1l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11ll111_opy_ (u"࠭ࡷࠨᬭ")):
                pass
            with open(file_path, bstack11ll111_opy_ (u"ࠢࡸ࠭ࠥᬮ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1l1lll_opy_.format(str(e)))
def bstack11l1ll1ll1l_opy_(file_name, key, value, logger):
    file_path = bstack11l1l11l1ll_opy_(bstack11ll111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᬯ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll1ll11_opy_ = json.load(open(file_path, bstack11ll111_opy_ (u"ࠩࡵࡦࠬᬰ")))
        else:
            bstack1lll1ll11_opy_ = {}
        bstack1lll1ll11_opy_[key] = value
        with open(file_path, bstack11ll111_opy_ (u"ࠥࡻ࠰ࠨᬱ")) as outfile:
            json.dump(bstack1lll1ll11_opy_, outfile)
def bstack1l1l111l_opy_(file_name, logger):
    file_path = bstack11l1l11l1ll_opy_(bstack11ll111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᬲ"), file_name, logger)
    bstack1lll1ll11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11ll111_opy_ (u"ࠬࡸࠧᬳ")) as bstack11l11111_opy_:
            bstack1lll1ll11_opy_ = json.load(bstack11l11111_opy_)
    return bstack1lll1ll11_opy_
def bstack1llll1l1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻᬴ࠢࠪ") + file_path + bstack11ll111_opy_ (u"ࠧࠡࠩᬵ") + str(e))
def bstack1l111l11l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11ll111_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥᬶ")
def bstack1l1lll111_opy_(config):
    if bstack11ll111_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᬷ") in config:
        del (config[bstack11ll111_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᬸ")])
        return False
    if bstack1l111l11l_opy_() < version.parse(bstack11ll111_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪᬹ")):
        return False
    if bstack1l111l11l_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫᬺ")):
        return True
    if bstack11ll111_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᬻ") in config and config[bstack11ll111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᬼ")] is False:
        return False
    else:
        return True
def bstack1l111lllll_opy_(args_list, bstack11l1lll111l_opy_):
    index = -1
    for value in bstack11l1lll111l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l1111111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l1111111_opy_ = bstack11l1111111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11ll111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᬽ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᬾ"), exception=exception)
    def bstack1111l1l11l_opy_(self):
        if self.result != bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᬿ"):
            return None
        if isinstance(self.exception_type, str) and bstack11ll111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᭀ") in self.exception_type:
            return bstack11ll111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᭁ")
        return bstack11ll111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᭂ")
    def bstack11l1ll1llll_opy_(self):
        if self.result != bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᭃ"):
            return None
        if self.bstack11l1111111_opy_:
            return self.bstack11l1111111_opy_
        return bstack11l1l11ll11_opy_(self.exception)
def bstack11l1l11ll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1l111ll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll1ll1ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l1l111l1_opy_(config, logger):
    try:
        import playwright
        bstack11l1lll1lll_opy_ = playwright.__file__
        bstack11l1l1l1ll1_opy_ = os.path.split(bstack11l1lll1lll_opy_)
        bstack11ll11111ll_opy_ = bstack11l1l1l1ll1_opy_[0] + bstack11ll111_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶ᭄ࠫ")
        os.environ[bstack11ll111_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬᭅ")] = bstack111111lll_opy_(config)
        with open(bstack11ll11111ll_opy_, bstack11ll111_opy_ (u"ࠪࡶࠬᭆ")) as f:
            bstack1ll1l11ll_opy_ = f.read()
            bstack11l1l1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪᭇ")
            bstack11ll111l111_opy_ = bstack1ll1l11ll_opy_.find(bstack11l1l1l1l1l_opy_)
            if bstack11ll111l111_opy_ == -1:
              process = subprocess.Popen(bstack11ll111_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤᭈ"), shell=True, cwd=bstack11l1l1l1ll1_opy_[0])
              process.wait()
              bstack11l1lll1111_opy_ = bstack11ll111_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭ᭉ")
              bstack11l1lll11l1_opy_ = bstack11ll111_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦᭊ")
              bstack11l1l11l1l1_opy_ = bstack1ll1l11ll_opy_.replace(bstack11l1lll1111_opy_, bstack11l1lll11l1_opy_)
              with open(bstack11ll11111ll_opy_, bstack11ll111_opy_ (u"ࠨࡹࠪᭋ")) as f:
                f.write(bstack11l1l11l1l1_opy_)
    except Exception as e:
        logger.error(bstack11lll1llll_opy_.format(str(e)))
def bstack11ll1l1l11_opy_():
  try:
    bstack11ll111l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᭌ"))
    bstack11l1l111111_opy_ = []
    if os.path.exists(bstack11ll111l1ll_opy_):
      with open(bstack11ll111l1ll_opy_) as f:
        bstack11l1l111111_opy_ = json.load(f)
      os.remove(bstack11ll111l1ll_opy_)
    return bstack11l1l111111_opy_
  except:
    pass
  return []
def bstack1lll1l11_opy_(bstack1l1ll11l1l_opy_):
  try:
    bstack11l1l111111_opy_ = []
    bstack11ll111l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ᭍"))
    if os.path.exists(bstack11ll111l1ll_opy_):
      with open(bstack11ll111l1ll_opy_) as f:
        bstack11l1l111111_opy_ = json.load(f)
    bstack11l1l111111_opy_.append(bstack1l1ll11l1l_opy_)
    with open(bstack11ll111l1ll_opy_, bstack11ll111_opy_ (u"ࠫࡼ࠭᭎")) as f:
        json.dump(bstack11l1l111111_opy_, f)
  except:
    pass
def bstack1111lll1_opy_(logger, bstack11ll11l111l_opy_ = False):
  try:
    test_name = os.environ.get(bstack11ll111_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ᭏"), bstack11ll111_opy_ (u"࠭ࠧ᭐"))
    if test_name == bstack11ll111_opy_ (u"ࠧࠨ᭑"):
        test_name = threading.current_thread().__dict__.get(bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧ᭒"), bstack11ll111_opy_ (u"ࠩࠪ᭓"))
    bstack11l11lll111_opy_ = bstack11ll111_opy_ (u"ࠪ࠰ࠥ࠭᭔").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll11l111l_opy_:
        bstack11l1l111ll_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᭕"), bstack11ll111_opy_ (u"ࠬ࠶ࠧ᭖"))
        bstack11llll11ll_opy_ = {bstack11ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᭗"): test_name, bstack11ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᭘"): bstack11l11lll111_opy_, bstack11ll111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᭙"): bstack11l1l111ll_opy_}
        bstack11l1ll1ll11_opy_ = []
        bstack11l1lll1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ᭚"))
        if os.path.exists(bstack11l1lll1l11_opy_):
            with open(bstack11l1lll1l11_opy_) as f:
                bstack11l1ll1ll11_opy_ = json.load(f)
        bstack11l1ll1ll11_opy_.append(bstack11llll11ll_opy_)
        with open(bstack11l1lll1l11_opy_, bstack11ll111_opy_ (u"ࠪࡻࠬ᭛")) as f:
            json.dump(bstack11l1ll1ll11_opy_, f)
    else:
        bstack11llll11ll_opy_ = {bstack11ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᭜"): test_name, bstack11ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᭝"): bstack11l11lll111_opy_, bstack11ll111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ᭞"): str(multiprocessing.current_process().name)}
        if bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ᭟") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11llll11ll_opy_)
  except Exception as e:
      logger.warn(bstack11ll111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ᭠").format(e))
def bstack1l1ll1l1l1_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1l1lll1l_opy_ = []
    bstack11llll11ll_opy_ = {bstack11ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᭡"): test_name, bstack11ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᭢"): error_message, bstack11ll111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ᭣"): index}
    bstack11l11ll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭᭤"))
    if os.path.exists(bstack11l11ll11ll_opy_):
        with open(bstack11l11ll11ll_opy_) as f:
            bstack11l1l1lll1l_opy_ = json.load(f)
    bstack11l1l1lll1l_opy_.append(bstack11llll11ll_opy_)
    with open(bstack11l11ll11ll_opy_, bstack11ll111_opy_ (u"࠭ࡷࠨ᭥")) as f:
        json.dump(bstack11l1l1lll1l_opy_, f)
  except Exception as e:
    logger.warn(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ᭦").format(e))
def bstack11l1lll11_opy_(bstack1l1l111l11_opy_, name, logger):
  try:
    bstack11llll11ll_opy_ = {bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭᭧"): name, bstack11ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᭨"): bstack1l1l111l11_opy_, bstack11ll111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ᭩"): str(threading.current_thread()._name)}
    return bstack11llll11ll_opy_
  except Exception as e:
    logger.warn(bstack11ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣ᭪").format(e))
  return
def bstack11l1l1l1l11_opy_():
    return platform.system() == bstack11ll111_opy_ (u"ࠬ࡝ࡩ࡯ࡦࡲࡻࡸ࠭᭫")
def bstack11111ll1l_opy_(bstack11ll1111l11_opy_, config, logger):
    bstack11l11llll1l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11ll1111l11_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡱࡺࡥࡳࠢࡦࡳࡳ࡬ࡩࡨࠢ࡮ࡩࡾࡹࠠࡣࡻࠣࡶࡪ࡭ࡥࡹࠢࡰࡥࡹࡩࡨ࠻ࠢࡾࢁ᭬ࠧ").format(e))
    return bstack11l11llll1l_opy_
def bstack11l1l11llll_opy_(bstack11l11llllll_opy_, bstack11l1lllll11_opy_):
    bstack11l1ll111ll_opy_ = version.parse(bstack11l11llllll_opy_)
    bstack11l1l11lll1_opy_ = version.parse(bstack11l1lllll11_opy_)
    if bstack11l1ll111ll_opy_ > bstack11l1l11lll1_opy_:
        return 1
    elif bstack11l1ll111ll_opy_ < bstack11l1l11lll1_opy_:
        return -1
    else:
        return 0
def bstack111l11l1l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11ll111l1l1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11ll111lll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11l1l11ll_opy_(options, framework, bstack1l1l1l1ll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11ll111_opy_ (u"ࠧࡨࡧࡷࠫ᭭"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1lll1l1l1l_opy_ = caps.get(bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᭮"))
    bstack11l1l1l1lll_opy_ = True
    bstack111l1ll11_opy_ = os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ᭯")]
    if bstack11l1ll1l1l1_opy_(caps.get(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪ࡝࠳ࡄࠩ᭰"))) or bstack11l1ll1l1l1_opy_(caps.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫ᭱"))):
        bstack11l1l1l1lll_opy_ = False
    if bstack1l1lll111_opy_({bstack11ll111_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧ᭲"): bstack11l1l1l1lll_opy_}):
        bstack1lll1l1l1l_opy_ = bstack1lll1l1l1l_opy_ or {}
        bstack1lll1l1l1l_opy_[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᭳")] = bstack11ll111lll1_opy_(framework)
        bstack1lll1l1l1l_opy_[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᭴")] = bstack1l1ll1ll1l1_opy_()
        bstack1lll1l1l1l_opy_[bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᭵")] = bstack111l1ll11_opy_
        bstack1lll1l1l1l_opy_[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᭶")] = bstack1l1l1l1ll_opy_
        if getattr(options, bstack11ll111_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ᭷"), None):
            options.set_capability(bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᭸"), bstack1lll1l1l1l_opy_)
        else:
            options[bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᭹")] = bstack1lll1l1l1l_opy_
    else:
        if getattr(options, bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧ᭺"), None):
            options.set_capability(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᭻"), bstack11ll111lll1_opy_(framework))
            options.set_capability(bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᭼"), bstack1l1ll1ll1l1_opy_())
            options.set_capability(bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᭽"), bstack111l1ll11_opy_)
            options.set_capability(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᭾"), bstack1l1l1l1ll_opy_)
        else:
            options[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᭿")] = bstack11ll111lll1_opy_(framework)
            options[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᮀ")] = bstack1l1ll1ll1l1_opy_()
            options[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᮁ")] = bstack111l1ll11_opy_
            options[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᮂ")] = bstack1l1l1l1ll_opy_
    return options
def bstack11l1lllllll_opy_(bstack11l1l11l11l_opy_, framework):
    bstack1l1l1l1ll_opy_ = bstack11lll1l1l_opy_.get_property(bstack11ll111_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥᮃ"))
    if bstack11l1l11l11l_opy_ and len(bstack11l1l11l11l_opy_.split(bstack11ll111_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᮄ"))) > 1:
        ws_url = bstack11l1l11l11l_opy_.split(bstack11ll111_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᮅ"))[0]
        if bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᮆ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11ll111ll11_opy_ = json.loads(urllib.parse.unquote(bstack11l1l11l11l_opy_.split(bstack11ll111_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᮇ"))[1]))
            bstack11ll111ll11_opy_ = bstack11ll111ll11_opy_ or {}
            bstack111l1ll11_opy_ = os.environ[bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᮈ")]
            bstack11ll111ll11_opy_[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᮉ")] = str(framework) + str(__version__)
            bstack11ll111ll11_opy_[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᮊ")] = bstack1l1ll1ll1l1_opy_()
            bstack11ll111ll11_opy_[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᮋ")] = bstack111l1ll11_opy_
            bstack11ll111ll11_opy_[bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᮌ")] = bstack1l1l1l1ll_opy_
            bstack11l1l11l11l_opy_ = bstack11l1l11l11l_opy_.split(bstack11ll111_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᮍ"))[0] + bstack11ll111_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᮎ") + urllib.parse.quote(json.dumps(bstack11ll111ll11_opy_))
    return bstack11l1l11l11l_opy_
def bstack1lll111lll_opy_():
    global bstack1l1lll111l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1lll111l_opy_ = BrowserType.connect
    return bstack1l1lll111l_opy_
def bstack1llll111_opy_(framework_name):
    global bstack111lll1l_opy_
    bstack111lll1l_opy_ = framework_name
    return framework_name
def bstack1l1l1lll1_opy_(self, *args, **kwargs):
    global bstack1l1lll111l_opy_
    try:
        global bstack111lll1l_opy_
        if bstack11ll111_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᮏ") in kwargs:
            kwargs[bstack11ll111_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᮐ")] = bstack11l1lllllll_opy_(
                kwargs.get(bstack11ll111_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᮑ"), None),
                bstack111lll1l_opy_
            )
    except Exception as e:
        logger.error(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤᮒ").format(str(e)))
    return bstack1l1lll111l_opy_(self, *args, **kwargs)
def bstack11l1ll111l1_opy_(bstack11l1llll111_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111lllll1_opy_(bstack11l1llll111_opy_, bstack11ll111_opy_ (u"ࠥࠦᮓ"))
        if proxies and proxies.get(bstack11ll111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᮔ")):
            parsed_url = urlparse(proxies.get(bstack11ll111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᮕ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩᮖ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᮗ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᮘ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᮙ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l1l1l1l1_opy_(bstack11l1llll111_opy_):
    bstack11l1l1111ll_opy_ = {
        bstack11ll1l111ll_opy_[bstack11ll1111lll_opy_]: bstack11l1llll111_opy_[bstack11ll1111lll_opy_]
        for bstack11ll1111lll_opy_ in bstack11l1llll111_opy_
        if bstack11ll1111lll_opy_ in bstack11ll1l111ll_opy_
    }
    bstack11l1l1111ll_opy_[bstack11ll111_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᮚ")] = bstack11l1ll111l1_opy_(bstack11l1llll111_opy_, bstack11lll1l1l_opy_.get_property(bstack11ll111_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᮛ")))
    bstack11ll1111111_opy_ = [element.lower() for element in bstack11ll11l1lll_opy_]
    bstack11ll111l11l_opy_(bstack11l1l1111ll_opy_, bstack11ll1111111_opy_)
    return bstack11l1l1111ll_opy_
def bstack11ll111l11l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11ll111_opy_ (u"ࠧ࠰ࠪࠫࠬࠥᮜ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11ll111l11l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11ll111l11l_opy_(item, keys)
def bstack1ll111l1ll1_opy_():
    bstack11l11lll11l_opy_ = [os.environ.get(bstack11ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣᮝ")), os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠢࡿࠤᮞ")), bstack11ll111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᮟ")), os.path.join(bstack11ll111_opy_ (u"ࠩ࠲ࡸࡲࡶࠧᮠ"), bstack11ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᮡ"))]
    for path in bstack11l11lll11l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11ll111_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦᮢ") + str(path) + bstack11ll111_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣᮣ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11ll111_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥᮤ") + str(path) + bstack11ll111_opy_ (u"ࠢࠨࠤᮥ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11ll111_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣᮦ") + str(path) + bstack11ll111_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢᮧ"))
            else:
                logger.debug(bstack11ll111_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧᮨ") + str(path) + bstack11ll111_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣᮩ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11ll111_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲ᮪ࠡࠩࠥ") + str(path) + bstack11ll111_opy_ (u"ࠨࠧ࠯ࠤ᮫"))
            return path
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤࠧᮬ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤᮭ"))
    logger.debug(bstack11ll111_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨᮮ"))
    return None
@measure(event_name=EVENTS.bstack11ll11lll1l_opy_, stage=STAGE.bstack111lllll_opy_)
def bstack1ll1lll1l11_opy_(binary_path, bstack1lll11l1l11_opy_, bs_config):
    logger.debug(bstack11ll111_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤᮯ").format(binary_path))
    bstack11ll1111l1l_opy_ = bstack11ll111_opy_ (u"ࠫࠬ᮰")
    bstack11l1ll1111l_opy_ = {
        bstack11ll111_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᮱"): __version__,
        bstack11ll111_opy_ (u"ࠨ࡯ࡴࠤ᮲"): platform.system(),
        bstack11ll111_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣ᮳"): platform.machine(),
        bstack11ll111_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ᮴"): bstack11ll111_opy_ (u"ࠩ࠳ࠫ᮵"),
        bstack11ll111_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤ᮶"): bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ᮷")
    }
    bstack11l1ll1l111_opy_(bstack11l1ll1111l_opy_)
    try:
        if binary_path:
            bstack11l1ll1111l_opy_[bstack11ll111_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ᮸")] = subprocess.check_output([binary_path, bstack11ll111_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ᮹")]).strip().decode(bstack11ll111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᮺ"))
        response = requests.request(
            bstack11ll111_opy_ (u"ࠨࡉࡈࡘࠬᮻ"),
            url=bstack1l111ll1l_opy_(bstack11ll1l11ll1_opy_),
            headers=None,
            auth=(bs_config[bstack11ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᮼ")], bs_config[bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᮽ")]),
            json=None,
            params=bstack11l1ll1111l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11ll111_opy_ (u"ࠫࡺࡸ࡬ࠨᮾ") in data.keys() and bstack11ll111_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩࡥࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᮿ") in data.keys():
            logger.debug(bstack11ll111_opy_ (u"ࠨࡎࡦࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡣ࡫ࡱࡥࡷࡿࠬࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰ࠽ࠤࢀࢃࠢᯀ").format(bstack11l1ll1111l_opy_[bstack11ll111_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᯁ")]))
            if bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫᯂ") in os.environ:
                logger.debug(bstack11ll111_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡡࡴࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠢ࡬ࡷࠥࡹࡥࡵࠤᯃ"))
                data[bstack11ll111_opy_ (u"ࠪࡹࡷࡲࠧᯄ")] = os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧᯅ")]
            bstack11l1lll1l1l_opy_ = bstack11l1l1ll111_opy_(data[bstack11ll111_opy_ (u"ࠬࡻࡲ࡭ࠩᯆ")], bstack1lll11l1l11_opy_)
            bstack11ll1111l1l_opy_ = os.path.join(bstack1lll11l1l11_opy_, bstack11l1lll1l1l_opy_)
            os.chmod(bstack11ll1111l1l_opy_, 0o777) # bstack11l1ll1lll1_opy_ permission
            return bstack11ll1111l1l_opy_
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡱࡩࡼࠦࡓࡅࡍࠣࡿࢂࠨᯇ").format(e))
    return binary_path
def bstack11l1ll1l111_opy_(bstack11l1ll1111l_opy_):
    try:
        if bstack11ll111_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ᯈ") not in bstack11l1ll1111l_opy_[bstack11ll111_opy_ (u"ࠨࡱࡶࠫᯉ")].lower():
            return
        if os.path.exists(bstack11ll111_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᯊ")):
            with open(bstack11ll111_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᯋ"), bstack11ll111_opy_ (u"ࠦࡷࠨᯌ")) as f:
                bstack11l11lllll1_opy_ = {}
                for line in f:
                    if bstack11ll111_opy_ (u"ࠧࡃࠢᯍ") in line:
                        key, value = line.rstrip().split(bstack11ll111_opy_ (u"ࠨ࠽ࠣᯎ"), 1)
                        bstack11l11lllll1_opy_[key] = value.strip(bstack11ll111_opy_ (u"ࠧࠣ࡞ࠪࠫᯏ"))
                bstack11l1ll1111l_opy_[bstack11ll111_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨᯐ")] = bstack11l11lllll1_opy_.get(bstack11ll111_opy_ (u"ࠤࡌࡈࠧᯑ"), bstack11ll111_opy_ (u"ࠥࠦᯒ"))
        elif os.path.exists(bstack11ll111_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡤࡰࡵ࡯࡮ࡦ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᯓ")):
            bstack11l1ll1111l_opy_[bstack11ll111_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬᯔ")] = bstack11ll111_opy_ (u"࠭ࡡ࡭ࡲ࡬ࡲࡪ࠭ᯕ")
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡥ࡫ࡶࡸࡷࡵࠠࡰࡨࠣࡰ࡮ࡴࡵࡹࠤᯖ") + e)
@measure(event_name=EVENTS.bstack11ll11ll111_opy_, stage=STAGE.bstack111lllll_opy_)
def bstack11l1l1ll111_opy_(bstack11ll111llll_opy_, bstack11l1ll1l11l_opy_):
    logger.debug(bstack11ll111_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭࠻ࠢࠥᯗ") + str(bstack11ll111llll_opy_) + bstack11ll111_opy_ (u"ࠤࠥᯘ"))
    zip_path = os.path.join(bstack11l1ll1l11l_opy_, bstack11ll111_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪ࡟ࡧ࡫࡯ࡩ࠳ࢀࡩࡱࠤᯙ"))
    bstack11l1lll1l1l_opy_ = bstack11ll111_opy_ (u"ࠫࠬᯚ")
    with requests.get(bstack11ll111llll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11ll111_opy_ (u"ࠧࡽࡢࠣᯛ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11ll111_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠣᯜ"))
    with zipfile.ZipFile(zip_path, bstack11ll111_opy_ (u"ࠧࡳࠩᯝ")) as zip_ref:
        bstack11l1ll11ll1_opy_ = zip_ref.namelist()
        if len(bstack11l1ll11ll1_opy_) > 0:
            bstack11l1lll1l1l_opy_ = bstack11l1ll11ll1_opy_[0] # bstack11l1l11111l_opy_ bstack11ll1l1l1l1_opy_ will be bstack11l1lll1ll1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1ll1l11l_opy_)
        logger.debug(bstack11ll111_opy_ (u"ࠣࡈ࡬ࡰࡪࡹࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡥࡹࡶࡵࡥࡨࡺࡥࡥࠢࡷࡳࠥ࠭ࠢᯞ") + str(bstack11l1ll1l11l_opy_) + bstack11ll111_opy_ (u"ࠤࠪࠦᯟ"))
    os.remove(zip_path)
    return bstack11l1lll1l1l_opy_
def get_cli_dir():
    bstack11l1l1llll1_opy_ = bstack1ll111l1ll1_opy_()
    if bstack11l1l1llll1_opy_:
        bstack1lll11l1l11_opy_ = os.path.join(bstack11l1l1llll1_opy_, bstack11ll111_opy_ (u"ࠥࡧࡱ࡯ࠢᯠ"))
        if not os.path.exists(bstack1lll11l1l11_opy_):
            os.makedirs(bstack1lll11l1l11_opy_, mode=0o777, exist_ok=True)
        return bstack1lll11l1l11_opy_
    else:
        raise FileNotFoundError(bstack11ll111_opy_ (u"ࠦࡓࡵࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡺࡨࡦࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾ࠴ࠢᯡ"))
def bstack1lll1l1l11l_opy_(bstack1lll11l1l11_opy_):
    bstack11ll111_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡳࠦࡡࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠢࠣࠤᯢ")
    bstack11l1l1ll1ll_opy_ = [
        os.path.join(bstack1lll11l1l11_opy_, f)
        for f in os.listdir(bstack1lll11l1l11_opy_)
        if os.path.isfile(os.path.join(bstack1lll11l1l11_opy_, f)) and f.startswith(bstack11ll111_opy_ (u"ࠨࡢࡪࡰࡤࡶࡾ࠳ࠢᯣ"))
    ]
    if len(bstack11l1l1ll1ll_opy_) > 0:
        return max(bstack11l1l1ll1ll_opy_, key=os.path.getmtime) # get bstack11ll11l11ll_opy_ binary
    return bstack11ll111_opy_ (u"ࠢࠣᯤ")
def bstack1ll1ll11111_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1ll11111_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d