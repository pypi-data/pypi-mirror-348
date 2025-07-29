"""
数据模块页面采集
"""

from DrissionPage import Chromium

from .material import Material
from .site_promotion import SitePromotion


class Data:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._site_promotion = None
        self._material = None

    @property
    def site_promotion(self):
        """全域推广数据采集"""

        if not self._site_promotion:
            self._site_promotion = SitePromotion(self._browser)

        return self._site_promotion

    @property
    def material(self):
        """素材数据采集"""

        if not self._material:
            self._material = Material(self._browser)

        return self._material
