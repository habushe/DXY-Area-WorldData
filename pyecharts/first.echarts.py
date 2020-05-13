import pyecharts
from pyecharts.charts import Bar
import datetime
import pandas

todaydate = str(datetime.date.today())
print(todaydate)
input_file = "data/out_"+str(todaydate)+".csv"
output_file = todaydate+"疫情数据及分析.html"

# 显示所有列
pandas.set_option('display.max_columns', None)
# 显示所有行
pandas.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pandas.set_option('max_colwidth', 200)




class Test01:

    def test(self):
        pyecharts.charts.set_global_options
        pandas.read_csv(input_file)

        bar = Bar()
        bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
        # 也可以传入路径参数，如 bar.render("mycharts.html")
        bar.render()


