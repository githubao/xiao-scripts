#!/usr/bin/env python
# encoding: utf-8

"""
@description: 操作sql

@author: baoqiang
@time: 2019-04-16 14:47
"""

from pyspark.sql import functions as F
from pyspark import HiveContext, SparkContext
import pandasql as ps


def process_sql():
    filename = '/Users/baoqiang/Downloads/1.txt'

    sc = SparkContext()
    sql_ctx = HiveContext(sc)
    df = sql_ctx.read.json(filename)

    # keywords = ["小包", "小钰"]
    # keywords = ['"{}"'.format(keyword) for keyword in keywords]
    # df = df.where('score > 5 or keyword in ({})'.format(', '.join(keywords)))

    token = '2ZDMkVAQVjN'
    # df = df.where('token = "{}" and get_json_object(share_data, "$.[0].ShareCategory") = 2'.format(token))
    # df = df.where('token = "{}"'.format(token))
    # df.show()

    df.registerTempTable("events")
    q1 = 'SELECT get_json_object(share_data, "$.[0].ShareCategory"),token FROM events where token = "{}"'.format(token)

    res = sql_ctx.sql(q1)

    res.show()


def process_sql_sample():
    filename = '/Users/baoqiang/Downloads/3.txt'

    sc = SparkContext()
    sql_ctx = HiveContext(sc)
    df = sql_ctx.read.json(filename)

    df.registerTempTable("events")
    # q1 = 'SELECT get_json_object(students, "$.[0].name") as name,* FROM events' \
    #      'lateral view explode(split(userl_ids,"[[[")) snTable as user_id  where id = {}'.format(1)

    q1 = "select explode(split(substring(students,3,length(students)-4),'\\\\},\\\\{')) as student from events"

    q2 = "select id,concat('{',student,'}') as entities from (select * from events) a " \
         "lateral view explode(split(substring(students,3,length(students)-4),'\\\\},\\\\{')) b as student"

    q3 = "select id,get_json_object(entities,'$.name') as name from (" \
         "select id,concat('{',student,'}') as entities from (select * from events) a " \
         "lateral view explode(split(substring(students,3,length(students)-4),'\\\\},\\\\{')) b as student )"

    res = sql_ctx.sql(q3)

    res.show()


if __name__ == '__main__':
    # process_sql()
    process_sql_sample()
