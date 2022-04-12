# Parsing toolkit for Python
from lark import Lark
import pandas as pd
import numpy as np


def get_list(t):
    i = 0
    lst = []
    while True:
        try:
            lst.append(t.children[i].children[0])
            i = i + 1
        except:
            break
    return lst


def get_df(t):
    key_name = t.children[0]
    if t.children[1].data == "string_list":
        lst = get_list(t.children[1])

    data = {'Name': ['Tom', 'Joseph', 'Krish', 'John', 'Maria', 'Ion', 'Andreea'], 'Age': [20, 21, 19, 18, 21, 18, 21]}
    df = pd.DataFrame(data)

    if lst:
        df = df[lst]

    return df


def computation(t):

    if t.children[0].children[0].children[0] == "mean":
        df = get_df(t.children[0].children[1])
        # in case int after the specified dataframe
        if t.children[0].children[2] and t.children[0].children[2].isdigit():
            each = int(t.children[0].children[2])
            df_each_x = df.groupby(np.arange(len(df))//3).mean()
            df = df_each_x
        print(df)


def run_instruction(t):
    if t.data == 'affirmation':
        run_instruction(t.children[0])

    elif t.data == 'assignment':

        run_instruction(t.children[0])
        key = t.children[0].children[0]

        if t.children[1].data == 'data_extraction':
            print("data extraction")
        elif t.children[1].data == 'computation':
            computation(t.children[1])


def run_parser(program):
    parse_tree = parser.parse(program)
    # print(parse_tree)
    for inst in parse_tree.children:
        run_instruction(inst)
    return parse_tree


def test():
    with open("source_code2.txt") as source_code:
        source_code = source_code.read()
    run_parser(source_code)


with open("grammar.lark") as grammar:
    grammar = grammar.read()

parser = Lark(grammar)

if __name__ == '__main__':
    test()
