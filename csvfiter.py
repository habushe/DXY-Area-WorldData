import pandas
from datetime import timedelta
import time

input_file = "foreign/csv/foreignArea.csv"
output_file = "out3.csv"


# def Csvtiterrun():
#     while True:
#         csvtiter()
#         time.sleep(3600)

def csvtiter():
    # pandas显示配置 方便调试
    # 显示所有列
    pandas.set_option('display.max_columns', None)
    # 显示所有行
    pandas.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pandas.set_option('max_colwidth', 200)

    # ！！！ 根据需要选择合适的字符集
    try:
        dataf = pandas.read_csv(input_file, encoding='UTF-8')
    except:
        dataf = pandas.read_csv(input_file, encoding='gb2312')

    dataf['updateTime'] = pandas.to_datetime(dataf['updateTime'])
    dataf['date'] = dataf['updateTime'].apply(lambda x: x.strftime('%Y-%m-%d'))
    dataf['date'] = pandas.to_datetime(dataf['date'])
    # print(type(dataf))  print(dataf.dtypes)   print(dataf.head())

    # 提取省列表
    df_t = dataf['provinceName']
    df_province = df_t.drop_duplicates()  # 去重 这个返回Series对象
    # df_province = df_t.unique()  # 去重 这个返回 ndarray

    df = pandas.DataFrame(index=None)

    df_t = dataf['date']
    df_date = df_t.drop_duplicates()  # 去重 返回Series对象
    df_date = df_date.sort_values()
    for date_t in df_date:
        for name in df_province:
            print(date_t.strftime('%Y-%m-%d') + name)  # 输出处理进度
            df1 = dataf.loc[(dataf['provinceName'].str.contains(name)) & (dataf['date'] == date_t), :]

            df1 = df1.loc[(df1['updateTime'] == df1['updateTime'].max()), :]  # 筛出省的最后数据 避免之前时间的市数据干扰，产生孤立值

            df_c = df1['countryName']
            df_country = df_c.drop_duplicates()  # 去重 这个返回Series对象
            confirmedCount = df1['confirmedCount'].max()
            suspectedCount = df1['suspectedCount']
            curedCount = df1['curedCount'].max()
            deadCount = df1['deadCount'].max()
            # updateTime2=df1['updateTime'].max()

            for country in df_country:
                df2 = df1.loc[(df1['countryName'].str.contains(country)), :]  # df2筛选出某个市的数据

                # 使用当天最后时间的数据，注释这行，则使用当天最大值提取数据
                df2 = df2.loc[(df2['updateTime'] == df2['updateTime'].max()), :]

                new = pandas.DataFrame({'地区': name,
                                        '国家': country,
                                        '确诊': confirmedCount,
                                        '疑似': suspectedCount,
                                        '治愈': curedCount,
                                        '死亡': deadCount,
                                        '日期': date_t},
                                       # '更新时间':updateTime2},
                                       pandas.Index(range(1)))
                #            print(new.head())
                df = df.append(new)

    # 补齐一个地区的空数据
    # #
    for date_t in df_date:
        #    print(date_t.strftime('%Y-%m-%d') + name)  # 输出处理进度
        if date_t == df_date.max():  # 最后一天不处理
            continue
        date_add = date_t + timedelta(days=1)
        for name in df_province:
            df1 = df.loc[(df['地区'].str.contains(name)) & (df['日期'] == date_t), :]
            if df1.shape[0] > 0:
                df2 = df.loc[
                      (df['地区'].str.contains(name)) & (df['日期'] == date_add),
                      :]
                if df2.shape[0] == 0:  # 后面一天省数据为空 把当前数据填到后一天
                    print('追加 ' + date_add.strftime('%Y-%m-%d') + name)  # 输出处理进度

                    for index, data in df1.iterrows():  # 改变值 使用索引
                        df1.loc[index, '日期'] = date_add
                    df = df.append(df1)

    # print(df)

    df.to_csv(output_file, encoding="utf_8_sig", index=False)  # 为保证excel打开兼容，输出为UTF8带签名格式


if __name__ == '__main__':
    csvtiter()
