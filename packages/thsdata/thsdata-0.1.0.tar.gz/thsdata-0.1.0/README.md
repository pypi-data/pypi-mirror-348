# THSData

**THSData** 提供了一种从thsdk中获取金融和市场数据的Pythonic方式。

<a target="new" href="https://pypi.python.org/pypi/thsdata"><img border=0 src="https://img.shields.io/pypi/pyversions/thsdata.svg" alt="Python version"></a>
<a target="new" href="https://github.com/bensema/thsdata"><img border=0 src="https://img.shields.io/github/stars/bensema/thsdata.svg?style=social&label=Star&maxAge=60" alt="Star this repo"></a>

# 安装

```bash
pip install --upgrade thsdata
```

# 使用

三行代码查询股票历史数据

```python
from thsdata import THSData

with THSData() as td:
    print(td.download("600519", start=20240101, end=20250101))


```

执行结果：

```
          time     open     high      low    close   volume    turnover
0   2024-01-02  1715.00  1718.19  1678.10  1685.01  3215644  5440082500
1   2024-01-03  1681.11  1695.22  1676.33  1694.00  2022929  3411400700
2   2024-01-04  1693.00  1693.00  1662.93  1669.00  2155107  3603970100
3   2024-01-05  1661.33  1678.66  1652.11  1663.36  2024286  3373155600
4   2024-01-08  1661.00  1662.00  1640.01  1643.99  2558620  4211918600
..         ...      ...      ...      ...      ...      ...         ...
237 2024-12-25  1538.80  1538.80  1526.10  1530.00  1712339  2621061900
238 2024-12-26  1534.00  1538.78  1523.00  1527.79  1828651  2798840000
239 2024-12-27  1528.90  1536.00  1519.50  1528.97  2075932  3170191400
240 2024-12-30  1533.97  1543.96  1525.00  1525.00  2512982  3849542600
241 2024-12-31  1525.40  1545.00  1522.01  1524.00  3935445  6033540400

[242 rows x 7 columns]
```
