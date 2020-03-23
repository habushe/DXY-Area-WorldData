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

uri = 'mongodb://localhost:27017/'
client = MongoClient(uri)
db = client['2019-nCoV']

collections = {
    # 'DXYOverall': 'overall',
    'DXYArea': 'area',
    # 'DXYNews': 'news',
    # 'DXYRumors': 'rumors'
}
time_types = ('pubDate', 'createTime', 'modifyTime', 'dataInfoTime', 'crawlTime', 'updateTime')


def git_manager(changed_files):
    repo = Repo(path=os.path.split(os.path.realpath(__file__))[0])
    repo.index.add(changed_files)
    repo.index.commit(message='{datetime} - Change detected!'.format(datetime=datetime.datetime.now()))
    origin = repo.remote('origin')
    origin.push()
    logger.info('Pushing to GitHub successfully!')


class DB:
    def __init__(self):
        self.db = db

    def count(self, collection):
        return self.db[collection].count_documents(filter={})

    def dump(self, collection):
        return self.db[collection].aggregate(
            pipeline=[
                {
                    '$sort': {
                        'updateTime': -1,
                        'crawlTime': -1
                    }
                }
            ]
        )


class Listener:
    def __init__(self):
        self.db = DB()

    def run(self):
        while True:
            self.listener()
            time.sleep(3600)

    def listener(self):
        for collection in collections:
            changed_files = list()
            self.csv_dumper(collection=collection)

    def csv_dumper(self, collection):
        if collection == 'DXYArea':
            foreign_structured_results = list()
            foreign_results = self.db.dump(collection=collection)
            for province_dict in foreign_results:
                all_result = dict()
                # if not province_dict.get('cities', None):
                all_result['provinceName'] = province_dict['provinceName']
                # all_result['continentName'] = province_dict['continentName']
                # all_result['continentEnglishName'] = province_dict['continentEnglishName']
                try:
                    all_result['countryName'] = province_dict['countryName']
                except KeyError:
                    all_result['countryName'] = None#中国
               # all_result['countryName'] = province_dict['countryName']
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
    listener = Listener()
    listener.run()

