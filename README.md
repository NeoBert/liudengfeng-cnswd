# A股网络数据工具
包含网络数据提取、整理、后台自动刷新流程。数据源自深证信、网易、新浪、巨潮、同花顺等。
+ `python`语言编写
    + `requests`及`seleniumwire`提取数据
    + `bs4`、`json`解析
+ `windows`后台计划任务自动刷新

以下介绍均基于`windows`操作系统。

## 数据项目
| 类别   | 网站       | 项目           | 完成状态 |
|:-------|------------|:---------------|:--------:|
| 信息类 | 深证信     | 股票分类       |    ✅     |
|        |            | 公司概况       |    ✅     |
|        |            | 股东股本       |    ✅     |
|        |            | 投资评级       |    ✅     |
|        |            | 业绩预告       |    ✅     |
|        |            | 分红派息       |    ✅     |
|        |            | 筹资指标       |    ✅     |
|        |            | 财务指标       |    ✅     |
|        | 同花顺     | 股票概念       |    ✅     |
|        | 腾讯       | 股票概念       |    ✅     |
|        | 巨潮       | 公司公告       |    ✅     |
|        | 新浪       | 24小时财经消息 |    ✅     |
|        | 中债       | 国债利率       |    ✅     |
|        | 雅虎       | 估值指标       |    ✅     |
| 交易类 | 网易       | 股票日线       |    ✅     |
|        |            | 指数日线       |    ✅     |
|        |            | 股票成交明细   |    ✅     |
|        | 深证信     | 日线数据       |    ✅     |
|        |            | 指数日线       |    ✅     |
|        |            | 融资融券       |    ✅     |
|        | 新浪       | 实时报价       |    ✅     |
| 其他   | 国家统计局 | 指标查询       |    ❓     |

## 存储
根据数据变化特点，可分为动态与静态。静态数据采用覆盖式刷新，而动态数据则使用添加模式。

使用`mongodb`存储数据。部分查询时间长的**热**数据也可使用该程序存储。


## 安装及使用
### 准备
+ 复制`geckodriver.exe`(`resources/tools`)到`c:\tools`
+ 复制国库券利率数据`*.xlsx`
+ 安装浏览器`Firefox`
+ `pip install https://github.com/liudengfeng/yahooquery/archive/2.2.4.tar.gz`
### 安装
```cmd
pip install -r req_dev.txt
pip install .

# 开发模式
pip install -e .

# 有关存储路径设置，请修改`setting/config.py/DEFAULT_CONFIG`，然后安装
```
### 命令行
```cmd
> stock --help

Usage: stock [OPTIONS] COMMAND [ARGS]...

  股票数据管理工具

      1. 市场数据

      2. 财经消息

      3. 股票交易数据

      4. 财务报告及指标

      5. 数据整理工具

Options:
  --help  Show this message and exit.

Commands:
  asr      刷新【深证信】数据浏览项目数据
  cjmx     刷新【网易】近期成交明细
  cld      交易日历【网易】
  clean    清理临时数据
  clsf     【深证信】股票分类及BOM表
  cnmeta   刷新深证信元数据
  codes    股票代码列表
  dscl     【巨潮】刷新公司公告
  margin   刷新【深证信】融资融券
  quote    【新浪】股票实时报价
  snnews   【新浪】财经消息
  tctgn    刷新【腾讯】概念股票列表
  tctm     刷新【腾讯】分钟级别交易数据
  thsgn    刷新【同花顺】概念股票列表
  thsnews  【同花顺】财经消息
  trs      刷新国库券利率数据
  wyi      刷新【网易】股票指数日线数据
  wys      刷新【网易】股票日线数据
  yh       刷新雅虎财经数据

# 刷新【网易】股票指数日线数据（重点指数）
> stock wyi
```


## 后台计划任务
影响网络数据的提取质量取决于多个因素，如网速、网站稳定性等等。为减少日常工作量及提高数据质量，
使用后台任务计划自动刷新数据。

| 任务     | 描述                         | 刷新频率 |   刷新时间   |速度|
|:---------|:-----------------------------|:--------:|:------------:|:-|
| 股票分类 | 申万、国证、证监会、地区分类 |   周六   |    02：00    |快|
| 定期清理 | 清除临时文件、数据检查、备份 |   周六   |    03：00    ||
| 公司公告 | 日内重复三次                 |   每日   |  8、16、18   |快|
| 财经消息 | 白天每半小时一次             |   每日   |     8~20     |极快|
| 实时报价 | 交易时段                     |  交易日  | 9：30~15：00 |极快|
| 成交明细 |                              |  交易日  |    18：00    |快|
| 数据浏览 | 深证信数据浏览高级搜索       |   每日   |    18：00    |慢|
| 融资融券 | 深证信专题统计               |  交易日  |  次日09：00  |快|
| 股票概念 | 同花顺                       |   周六   |    04：00    |较慢|
|          | 腾讯                         |  交易日  |    20：00    |极快|
| 交易日历 |                              |  工作日  |    09：35    |快|
| 国债利率 |                              |  交易日  |    17：00    |慢|
| 网易日线 | 股票、主要指数               |  交易日  |    18：00    |极快|
| 雅虎财经 | 次日凌晨                     |  工作日  |    01：00    |慢|

注：
1. 批处理文件参考`bats/`目录
2. 参考[如何设置后台任务计划](https://blog.csdn.net/mao_mao37/article/details/82592603)
