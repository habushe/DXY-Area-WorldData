# DXY-Area-WorldData
# 2019新型冠状病毒疫情时间序列数据仓库

简体中文 | [English](README.en.md)

本项目为对Blankerl [2019新型冠状病毒（COVID-19/2019-nCoV）疫情状况的时间序列数据仓库](https://github.com/BlankerL/DXY-COVID-19-Data)项目的修改，数据来源为[丁香园](https://3g.dxy.cn/newh5/view/pneumonia)。

数据由[丁香园对外开放数据接口API](https://lab.isaaclin.cn/nCoV/api/area)获得，每小时检测一次更新，若有更新则推送至数据仓库中。

### 代码说明
[script2.py](script2.py)为请求[丁香园对外开放数据接口API](https://lab.isaaclin.cn/nCoV/api/area)并进行解析处理

[csvfiter.py](csvfiter.py)为对[script2.py](script2.py)得到的数据文件[foreign\csv\foreignArea.csv](foreign\csv\foreignArea.csv)进行去重和数据修补处理

[csv_conpute.py](csv_conpute.py)为对[csvfiter.py](csvfiter.py) 去重和修补后的数据[out1.csv](out1.csv)进行确诊、治愈、死亡的新增统计计算

#### CSV文件列表
1. 世界数据[foreign\csv\foreignArea.csv](foreign\csv\foreignArea.csv)


#### JSON文件列表
由于API接口时常不稳定，因此此项目也会定时向`json`文件夹中推送静态的JSON文件更新。JSON文件与API中提供的JSON完全一致。

由于本人精力有限（且为小白），不接受数据定制。如对数据有更多的要求，烦请自行处理。

###  本项目代码借鉴说明

本项目代码借鉴了
  Blankerl 的[2019新型冠状病毒（COVID-19/2019-nCoV）疫情状况的时间序列数据仓库](https://github.com/BlankerL/DXY-COVID-19-Data)项目代码
  
  Avens666 的[Avens666/COVID-19-2019-nCoV-Infection-Data-cleaning-](https://github.com/Avens666/COVID-19-2019-nCoV-Infection-Data-cleaning-)项目代码

