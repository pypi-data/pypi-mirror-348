"""
素材数据采集
"""

from DrissionPage import Chromium
from DrissionPage._pages.mix_tab import MixTab

from .._browser_utils import BrowserUtils
from .._utils import Utils
from ._utils import (
    download__report,
    pick__custom_date_range,
    wait__general_query_packet,
)


class Urls:
    material_analysis = 'https://qianchuan.jinritemai.com/dataV2/roi2-material-analysis?aavid=1810072296114372'
    """素材分析页面URL (默认为视频素材 Tab)"""


class DataPacketUrl:
    general_query = 'qianchuan.jinritemai.com/ad/api/data/v1/common/statQuery'
    """通用数据查询接口"""


class Material:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._timeout = 15

    def _wait__video__push_product__detail_packet(
        self, page: MixTab, timeout: float = None
    ):
        """等待 [视频素材-推商品] 表格数据返回"""

        return wait__general_query_packet(
            page, 'roi2_material_list', 'roi2_video_material_analysis', timeout
        )

    def _wait__picture__detail_packet(self, page: MixTab, timeout: float = None):
        """等待 [图片素材] 表格数据返回"""

        return wait__general_query_packet(
            page, 'roi2_material_list', 'roi2_pic_material_analysis_v2', timeout
        )

    def get__video__push_product__detail(
        self, begin_date: str, end_date: str, raw=False, timeout: float = None
    ):
        """
        获取 [视频素材-推商品] 表格数据

        Args:
            raw: 如果为 True 则返回下载报表的文件路径, 否则返回处理后的数据字典列表
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = BrowserUtils.get__main_page(self._browser)
        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        page.get(Urls.material_analysis)
        if not self._wait__video__push_product__detail_packet(page, _timeout):
            raise RuntimeError('首次进入页面获取数据包超时')

        data_dimension_btn_ele = page.ele(
            't:div@@class^ovui-radio-item@@text()=推商品', timeout=3
        )
        if not data_dimension_btn_ele:
            raise ValueError('未找到数据维度 [推商品] 按钮')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        data_dimension_btn_ele.click(by_js=True)
        if not self._wait__video__push_product__detail_packet(page, _timeout):
            raise RuntimeError('切换数据维度后获取数据超时')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        pick__custom_date_range(begin_date, end_date, page)
        if not self._wait__video__push_product__detail_packet(page, _timeout):
            raise RuntimeError('修改日期后获取数据包超时')

        report_path = download__report(page)
        if raw is True:
            return report_path

        raw_data_list = Utils.xlsx_read(report_path)
        data_list: list[dict] = []
        for data in raw_data_list:
            _record = Utils.dict_format__strip(data, suffix=['%'])
            _record = Utils.dict_format__number(_record, exclude_fields=['素材ID'])
            data_list.append(_record)

        Utils.file_remove(report_path)

        return data_list

    def get__picture__detail(
        self, begin_date: str, end_date: str, raw=False, timeout: float = None
    ):
        """
        获取 [图片素材] 表格数据

        Args:
            raw: 如果为 True 则返回下载报表的文件路径, 否则返回处理后的数据字典列表
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = BrowserUtils.get__main_page(self._browser)
        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        page.get(Urls.material_analysis)
        target_tab_ele = page.ele('t:div@@text()=图片素材', timeout=8)
        if not target_tab_ele:
            raise ValueError('未找到 [图片素材] 标签页')
        target_tab_ele.click(by_js=True)

        if not self._wait__picture__detail_packet(page, _timeout):
            raise RuntimeError('首次进入页面获取数据包超时')

        page.listen.start(
            targets=DataPacketUrl.general_query, method='POST', res_type='XHR'
        )
        pick__custom_date_range(begin_date, end_date, page)
        if not self._wait__picture__detail_packet(page, _timeout):
            raise RuntimeError('修改日期后获取数据包超时')

        report_path = download__report(page)
        if raw is True:
            return report_path

        raw_data_list = Utils.xlsx_read(report_path)
        data_list: list[dict] = []
        for data in raw_data_list:
            _record = Utils.dict_format__strip(data, suffix=['%'])
            _record = Utils.dict_format__number(
                _record, exclude_fields=['素材ID', '素材名称']
            )
            data_list.append(_record)

        Utils.file_remove(report_path)

        return data_list
