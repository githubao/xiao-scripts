#!/usr/bin/env python
# encoding: utf-8

"""
@description: 找到excel表格里面包含问题的上下文数据

@author: baoqiang
@time: 2018/10/28 上午11:16
"""

import pandas as pd
import numpy as np
from collections import OrderedDict

root_path = '/Users/baoqiang/Downloads'


def run():
    questions = read_file('{}/question.txt'.format(root_path))
    out_file = '{}/dialog_out.xlsx'.format(root_path)
    outputs = []

    df = pd.read_excel('{}/dialog.xlsx'.format(root_path))
    datas = np.array(df).tolist()
    for did, dialog in datas:
        chats = dialog.split('\n')
        for idx, chat in enumerate(chats):
            for ques in questions:
                if ques in chat:
                    if idx < len(chats) - 1:
                        outputs.append(build_dic(did, ques, '\n'.join([chat, chats[idx + 1]])))
                    else:
                        outputs.append(build_dic([did, ques, '\n'.join([chat, 'NONE'])]))

    outdf = pd.DataFrame(outputs)
    outdf.to_excel(out_file, index=False)


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]


def build_dic(did, ques, dialogs):
    return OrderedDict(
        {
            "did": did,
            "ques": ques,
            "dialogs": dialogs,
        }
    )


if __name__ == '__main__':
    run()
