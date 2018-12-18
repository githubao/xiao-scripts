#!/usr/bin/env python
# encoding: utf-8

"""
@description: 利用pandas合并两个数据表格的数据

@author: baoqiang
@time: 2018/8/7 下午5:25
"""

import pandas as pd
import json
import sys

# from pyspark.sql import functions as F
# from pyspark import HiveContext, SparkContext

# root_path = '/data01/home/baoqiang/repos/toutiao/app/data'
# root_path = '/Users/baoqiang/Downloads/分成策略V3'
root_path = '/Users/baoqiang/Downloads/'


# root_path = '/Users/baoqiang/repos/toutiao/app/data'

def main():
    # compare_data()
    # run_item()
    # data_vlookup()
    # find_json_top()
    # find_null()
    # test_isin()
    # test_fmt()
    # to_excel_danke()
    # to_excel_ziru()
    # to_excel_miui()
    # bookmarks_parse()
    to_excel_jike()


def to_excel_jike():
    input_file = root_path + 'jike.json'
    out_file = root_path + 'jike.xlsx'

    df = read_json(input_file)

    # 指定列的顺序
    cols = ['topic_id', 'id', 'name', 'desc', 'count', 'web_url', 'topic_type',
            'app_url', 'from_url', 'create_at', 'lastpost_at', 'update_at']
    df = df.ix[:, cols]

    # 去重id重复的记录
    df = df.drop_duplicates('id')

    # 按照多个字段排序
    df = df.sort_values(by=['count'], ascending=[False])

    df.to_excel(out_file, index=False)


def bookmarks_parse():
    input_file = root_path + 'Bookmarks.txt'

    with open(input_file, 'r', encoding='utf-8') as f:
        dic = json.loads(f.read())

    for item in dic['roots']['bookmark_bar']['children'][16]['children']:
        print(item['url'])


def to_excel_miui():
    """
    小米主题的数据
    :return:
    """
    input_file = root_path + 'miui.json'
    out_file = root_path + 'miui.xlsx'

    df = read_json(input_file)

    # 指定列的顺序
    cols = ['id', 'title', 'comment', 'price', 'url', 'rank']
    df = df.ix[:, cols]

    # 去重id重复的记录
    df = df.drop_duplicates('id')

    # 修改免费的记录
    df['price'] = df['price'].map(lambda x: float('{}'.format(x).replace('免费', '0')))

    # 只取comment不小于10的
    df = df[df['comment'] >= 10]

    # 按照多个字段排序
    df = df.sort_values(by=['price', 'comment'], ascending=[True, False])

    df.to_excel(out_file, index=False)


def to_excel_ziru():
    """
    自如接口爬虫来的数据
    :return:
    """
    house_url_fmt = 'http://www.ziroom.com/z/vr/{}.html'

    input_file = root_path + 'ziru3.json'
    out_file = root_path + 'ziru3.xlsx'

    df = read_json(input_file)

    # 添加url
    df['url'] = df['id'].map(lambda x: house_url_fmt.format(x))

    # 指定列的顺序
    cols = ['id', 'subway_line_code_first', 'subway_station_code_first', 'sell_price',
            'usage_area', 'house_facing', 'title', 'room_name', 'url', 'resblock_name',
            'build_size', 'dispose_bedroom_amount', 'walking_distance_dt_first']
    df = df.ix[:, cols]

    # 去重id重复的记录
    df = df.drop_duplicates('id')

    # 去除"约"
    df['usage_area'] = df['usage_area'].map(lambda x: float('{}'.format(x).replace('约', '')))
    df['build_size'] = df['build_size'].map(lambda x: float('{}'.format(x).replace('约', '')))

    df.to_excel(out_file, index=False)


def to_excel2():
    """
    把json转成excel, 处理studygolang的文件
    :return:
    """
    input_file = root_path + 'study_go.json'
    out_file = root_path + 'study_go.xlsx'

    df = read_json(input_file)

    # 指定列的顺序
    cols = ['id', 'title', 'read', 'tags', 'url', 'from_url', 'date']
    df = df.ix[:, cols]

    # 倒序排列
    df.sort_values("read", inplace=True, ascending=False)

    # 格式化tags
    # df['tag'] = df['tag'].map(lambda x: str(x))

    # df.to_excel(out_file, index=False)
    writer = pd.ExcelWriter(out_file, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()


def to_excel_danke():
    """
    把json转成excel
    :return:
    """
    input_file = root_path + 'danke.json'
    out_file = root_path + 'danke.xlsx'

    df = read_json(input_file)

    # 指定列的顺序
    cols = ['id', 'subway', 'community', 'price', 'direction', 'size',
            'shared', 'town', 'area', 'url', 'from_url', 'floor', 'structure']
    df = df.ix[:, cols]

    # 去重id重复的记录
    df = df.drop_duplicates('id')

    df.to_excel(out_file, index=False)


def sum_group_by():
    root_path = ''

    for i in range(13, 19):
        pass


def run_fmt():
    a = 'category in ({})'.format(','.join(map(str, [1, 2, 3])))
    print(a)


def run_isin():
    filename = '/Users/baoqiang/Downloads/1.txt'

    keywords = ["小包", "小钰"]

    sc = SparkContext()
    sql_ctx = HiveContext(sc)
    df = sql_ctx.read.json(filename)

    keywords = ['"{}"'.format(keyword) for keyword in keywords]
    df = df.where('score > 5 or keyword in ({})'.format(', '.join(keywords)))

    df.show()

    # df2 = pd.DataFrame()


def find_null():
    filename = '/Users/baoqiang/Downloads/2.txt'

    # df = read_multilinejson_to_df()
    # df = df[df['lk_category1'].apply(lambda x: None not in x) & df['lk_category3'].apply(lambda x: None not in x)]
    # print(df.shape)

    contains_null = F.udf(lambda d: None not in d)

    sc = SparkContext()
    sql_ctx = HiveContext(sc)

    df = sql_ctx.read.json(filename)

    # for i in range(1, 4):
    #     key = 'lk_category{}'.format(i)
    #     appear_key = '{}_appear'.format(key)
    #     df = df.withColumn(appear_key, has_column(key))
    #     df = df.where('{} != null'.format(appear_key))
    #
    #     df.show()

    # df = df.filter("lk_category1 <> null and lk_category2 <> null and lk_category3 <> null")
    df = df.na.drop()

    for i in range(1, 4):
        key = 'lk_category{}'.format(i)
        exist_key = '{}_exist'.format(key)
        df = df.withColumn(exist_key, contains_null(key))
        df = df.where('{} = true'.format(exist_key))

        df.show()


def find_json_top():
    my_path = '/Users/baoqiang/Documents'
    with open('{}/tmp.json'.format(my_path), 'r', encoding='utf-8') as f:
        datas = f.read()
        json_data = json.loads(datas)

    # 读取
    df = pd.read_json(json.dumps(json_data['device_brand']))

    # # 算分
    # df['score'] = df['completePeople'] + df['learnedPeople'] + df['currentPeople']
    #
    # # 过滤
    # flt = ['courseId', 'courseName', 'mainContent', 'score', 'isSelected']
    # df = df.filter(flt)

    # 排序
    df = df.sort_values(by=['score'], ascending=False)

    # 指定格式
    df['score'] = df['score'].map(lambda x: '{:,d}'.format(x))

    # 保存
    df.to_excel('{}/tmp.xlsx'.format(my_path), index=False)


def data_vlookup():
    for dt in ['0810', '0811']:
        item_vlookup(dt)


def item_vlookup(dt):
    filename1 = '{}/{}'.format(root_path, '新旧分成策略对比-{}-old.xlsx'.format(dt))
    filename2 = '{}/{}'.format(root_path, '新旧分成策略对比-{}.xlsx'.format(dt))

    df1 = flt_df(filename1)
    df2 = flt_df(filename2)

    # media = '媒体id'.decode('utf-8')
    media = '媒体id'

    df = pd.merge(df1, df2, on=media, suffixes=['_old', '_new'], how='outer')

    out_file = '{}/{}.xlsx'.format(root_path, dt)
    df.to_excel(out_file, index=False)

    print('process {} finished'.format(dt))
    sys.stdout.flush()


def flt_df(filename):
    media_ids = get_media_ids()
    # media = '媒体id'.decode('utf-8')
    media = '媒体id'

    df = read_excel(filename)
    df = df[df[media].isin(media_ids)]

    # flt = ['媒体id'.decode('utf-8'), '总阅读收益_new'.decode('utf-8')]
    flt = ['媒体id', '总阅读收益_new']
    df = df.filter(flt)

    return df


def run_item():
    filenames = ['1590912666757134', '3805425585', '6579376245']

    flt_dic = {
        'old': ['item_id', 'group_id', 'media_id', 'all_read_count_modified', 'media_decrease_ladder', 'media_level',
                'tag', 'quality_level', 'article_factor', 'gallery', 'original', 'media_punish_factor', 'income'],
        'new': ['item_id', 'group_id', 'media_id', 'all_read_count_modified', 'media_decrease_ladder',
                'media_level_v2', 'quality_level', 'article_factor', 'gallery', 'original', 'media_punish_factor',
                'income']
    }

    for filename in filenames:
        for name in ['old', 'new']:
            input_file = '{}/{}-{}.txt'.format(root_path, filename, name)
            flt = flt_dic.get(name)
            out_file = '{}/{}-{}.xlsx'.format(root_path, filename, name)
            run_df(input_file, flt, out_file)

            print('process {} succeed'.format(input_file))
            sys.stdout.flush()


def read_json(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        datas = (line.strip() for line in f)
        datas = '[{}]'.format(','.join(datas))

    return pd.read_json(datas)


def run_df(input_file, filter_rule, out_file):
    with open(input_file, 'r') as f:
        datas = (line.strip() for line in f)
        datas = '[{}]'.format(','.join(datas))

    df = pd.read_json(datas)

    df = df.filter(filter_rule)

    df['item_id'] = df['item_id'].map(lambda x: "'{}".format(x))
    df['group_id'] = df['group_id'].map(lambda x: "'{}".format(x))
    df['media_id'] = df['media_id'].map(lambda x: "'{}".format(x))

    df.to_excel(out_file)


def compare_data():
    for date in ['0810', '0811']:
        old_vs_new(date)


def old_vs_new(date):
    old_file = '{}/{}-old.xls'.format(root_path, date)
    new_file = '{}/{}-new.xls'.format(root_path, date)

    out_file = '{}/新旧分成策略对比-{}.xlsx'.format(root_path, date)

    flt1 = ['媒体id', '媒体名称', '账号类型', '图文原创标签', '分成类型', '老最高评级', '新评级全局评级', '阶梯图文阅读量', '阶梯组图阅读量', '总阅读收益']
    flt2 = ['媒体id', '新评级', '阶梯图文阅读量', '阶梯组图阅读量', '总阅读收益']

    # flt1 = [item.decode('utf-8') for item in flt1]
    # flt2 = [item.decode('utf-8') for item in flt2]

    df1 = read_excel(old_file)
    df2 = read_excel(new_file)

    # media_id前面添加 单引号
    # media = '媒体id'.decode('utf-8')
    media = '媒体id'
    df1[media] = df1[media].map(lambda x: "'{}".format(x))

    df1 = df1.filter(flt1)
    df2 = df2.filter(flt2)

    # df = pd.merge(df1, df2, on='媒体id'.decode('utf-8'), suffixes=['_old', '_new'], how='outer')
    df = pd.merge(df1, df2, on=media, suffixes=['_old', '_new'], how='outer')

    df.to_excel(out_file)

    print(df)


def read_excel(file_path):
    xls_file = pd.ExcelFile(file_path)

    sheet_names = xls_file.sheet_names
    df_all = pd.DataFrame()
    for i in sheet_names:
        # skiprows=0代表读取跳过的行数为0行，不写代表不跳过标题
        # df = pd.read_excel(file_path, sheetname=i, skiprows=2, index=False, encoding='utf8')
        df = xls_file.parse(i)

        df_all = df_all.append(df)

    return df_all


def get_media_ids():
    filename = '/Users/baoqiang/repos/toutiao/app/pgc/scripts/pgc_income_v2/ad_boost_list'
    with open(filename, 'r') as f:
        return ["'{}".format(line.strip()) for line in f]


if __name__ == '__main__':
    main()
