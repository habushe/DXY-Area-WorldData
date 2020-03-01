"""
@ProjectName: DXY-2019-nCoV-Crawler
@FileName: script.py
@Author: Jiabao Lin
@Date: 2020/1/31
"""
from git import Repo
from pymongo import MongoClient
import os
import json
import time
import logging
import datetime
import requests
import pandas as pd


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
collections = {
    'foreignArea': 'area?latest=0'
}
time_types = ('pubDate', 'createTime', 'modifyTime', 'dataInfoTime', 'crawlTime', 'updateTime')


def git_manager(changed_files):
    repo = Repo(path=os.path.split(os.path.realpath(__file__))[0])
    print(os.path.split(os.path.realpath(__file__))[0])
    repo.index.add(changed_files)
    repo.index.commit(message='{datetime} - Change detected!'.format(datetime=datetime.datetime.now()))
    origin = repo.remote('origin')
    origin.push()
    logger.info('Pushing to GitHub successfully!')



def listenerrun():
    while True:
        listener()
        time.sleep(3600)

def listener():
    changed_files = list()
    for collection in collections:
        json_file = open(
            os.path.join(
                os.path.split(os.path.realpath(__file__))[0], 'foreign/json', collection + '.json'),
            'r', encoding='utf-8'
        )
        static_data = json.load(json_file)
        json_file.close()
        while True:
            request = requests.get(url='https://lab.isaaclin.cn/nCoV/api/' + collections.get(collection))
            if request.status_code == 200:
                current_data = request.json()
                print("request请求成功")
                break
            else:
                print("request请求失败")
                continue

        if static_data != current_data:
            json_dumper(collection=collection, content=current_data)
            # changed_files.append('foreign/json/' + collection + '.json')
            print("json_dumper更新完成")
            csv_dumper(collection=collection, content=current_data)
            # changed_files.append('foreign/csv/' + collection + '.csv')
            logger.info('{collection} updated!'.format(collection=collection))
        # if changed_files:
        #         git_manager(changed_files=changed_files)

def json_dumper(collection, content):
    json_file = open(
        os.path.join(
            os.path.split(os.path.realpath(__file__))[0], 'foreign/json', collection + '.json'),
        'w', encoding='utf-8'
    )
    json.dump(content, json_file, ensure_ascii=False, indent=4)
    json_file.close()

def csv_dumper(collection, content):
    if collection == 'foreignArea':
        foreign_structured_results = list()
        foreign_results = content['results']
        for province_dict in foreign_results:
            all_result = dict()
            # if not province_dict.get('cities', None):
            all_result['provinceName'] = province_dict['provinceName']
            # all_result['continentName'] = province_dict['continentName']
            # all_result['continentEnglishName'] = province_dict['continentEnglishName']
            all_result['countryName'] = province_dict['countryName']
            # all_result['countryEnglishName'] = province_dict['countryEnglishName']
            # all_result['currentConfirmedCount'] = province_dict['currentConfirmedCount']
            all_result['confirmedCount'] = province_dict['confirmedCount']
            all_result['suspectedCount'] = province_dict['suspectedCount']
            all_result['curedCount'] = province_dict['curedCount']
            all_result['deadCount'] = province_dict['deadCount']

            all_result['updateTime'] = datetime.datetime.fromtimestamp(province_dict['updateTime'] / 1000)
            print(all_result)
            foreign_structured_results.append(all_result)

            df2 = pd.DataFrame(foreign_structured_results)
            df2 = df2.dropna()
            df2.to_csv(
                path_or_buf=os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], 'foreign/csv', 'foreignArea.csv'),
                index=False, encoding='utf_8_sig'
            )
            logger.info('foreign/csv updated!'.format(collection=collection))


if __name__ == '__main__':
    listenerrun()
