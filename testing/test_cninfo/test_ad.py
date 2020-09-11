import pytest
from numpy.testing import assert_almost_equal
import pandas as pd
# 网站输出数据已经过滤掉测试时点已经退市的股票
# 采用过滤测试
filter_coses = ['000001', '000002', '600000', '300001', '000004', '000529']


@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.parametrize(
    "level, start, end, expected_rows,f_rows",
    [
        ('21', '2019-04-01', '2019-06-30', 110, 1),
        ('22', '2019-04-01', '2019-06-30', 5175, 8),
        ('23', '2019-04-01', '2019-06-30', 3449, 12),
        ('24', '2019-04-01', '2019-06-30', 5429, 12),
        ('25', '2019-04-01', '2019-06-30', 3737, 7),
        ('3', '2018-10-01', '2018-12-31', 15086, 0),
        # ('41', '2019-04-01', '2019-06-30', 1905),
        # # 全年
        # ('5', '2018-01-01', '2018-12-31', 7322),
        # # 期间
        # ('61', '2019-04-01', '2019-06-30', 181),
        # ('62', '2019-04-01', '2019-06-30', 134),
        # ('63', '2019-04-01', '2019-06-30', 12),
        # ('64', '2019-04-01', '2019-06-30', 5),
        # # 季度财报
        # ('711', '2019-04-01', '2019-06-30', 3895),
        # ('712', '2019-04-01', '2019-06-30', 3895),
        # # 网站bug 三张表应该一致 行数统一才对
        # ('713', '2019-04-01', '2019-06-30', 3894),
        # ('721', '2019-04-01', '2019-06-30', 3893),
        # ('722', '2019-04-01', '2019-06-30', 3946),
        # ('731', '2019-04-01', '2019-06-30', 3692),
        # ('732', '2019-04-01', '2019-06-30', 3692),
        # ('733', '2019-04-01', '2019-06-30', 3692),
        # ('741', '2019-04-01', '2019-06-30', 3737),
        # ('742', '2019-04-01', '2019-06-30', 3737)
    ])
def test_fetch_data(advance_api, level, start, end, expected_rows, f_rows):
    factor = 1000
    data = advance_api.get_data(level, start, end)
    assert_almost_equal(len(data) / factor, expected_rows / factor, 2)
    f_data = [d for d in data if d['股票代码'] in filter_coses]
    assert len(f_data) == f_rows


@pytest.mark.parametrize(
    "name, expected",
    [
        ('基本资料', None),
        # 2
        ('公司股东实际控制人', 'QD'),
        ('公司股本变动', 'QD'),
        ('上市公司高管持股变动', 'QD'),
        ('股东增（减）持情况', 'QD'),
        ('持股集中度', 'QQ'),
        # 3
        ('投资评级', 'MD'),
        # 4
        ('上市公司业绩预告', 'QQ'),
        # 5
        ('分红指标', 'YY'),
        # 6
        ('公司增发股票预案', 'QD'),
        ('公司增发股票实施方案', 'QD'),
        ('公司配股预案', 'QD'),
        ('公司配股实施方案', 'QD'),
        ('公司首发股票', None),
        # 7 报告期
        ('个股报告期资产负债表', 'QQ'),
        ('个股报告期利润表', 'QQ'),
        ('个股报告期现金表', 'QQ'),
        ('金融类资产负债表2007版', 'QQ'),
        ('金融类利润表2007版', 'QQ'),
        ('金融类现金流量表2007版', 'QQ'),
        # 7 指标
        ('个股报告期指标表', 'QQ'),
        ('财务指标行业排名', 'QQ'),
        # 7 单季
        ('个股单季财务利润表', 'QQ'),
        ('个股单季现金流量表', 'QQ'),
        ('个股单季财务指标', 'QQ'),
        # 7 TTM
        ('个股TTM财务利润表', 'QQ'),
        ('个股TTM现金流量表', 'QQ'),
    ])
def test_current_period_type(advance_api, name, expected):
    level = advance_api.name_to_level(name)
    advance_api.to_level(level)
    actual = advance_api._current_period_type()
    assert expected == actual


@pytest.mark.parametrize(
    "name, start, end, expected",
    [
        # 没有限定期间
        ('基本资料', '2019-04-01', '2019-06-30', [(None, None)]),
        # 按季度循环
        ('公司股东实际控制人', '2019-01-03', '2019-06-30', [
            ('2019-01-03', '2019-03-31'), ('2019-04-01', '2019-06-30')
        ]),
        # 按月循环
        ('投资评级', '2019-01-03', '2019-03-15', [('2019-01-03', '2019-01-31'),
                                              ('2019-02-01', '2019-02-28'),
                                              ('2019-03-01', '2019-03-15')]),
        # 按季度循环，表达为 年、季
        ('个股报告期利润表', '2018-01-03', '2018-07-15', [(2018, 1), (2018, 2),
                                                  (2018, 3)]),
        # 按年循环
        ('分红指标', '2018-01-03', '2020-03-15', [(2018, None), (2019, None),
                                              (2020, None)]),
    ])
def test_internal_ps(advance_api, name, start, end, expected):
    level = advance_api.name_to_level(name)
    advance_api.to_level(level)
    actual = advance_api._internal_ps(pd.Timestamp(start), pd.Timestamp(end))
    assert actual == expected
