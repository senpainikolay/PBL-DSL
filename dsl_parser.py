# Parsing toolkit for Python
from lark import Lark
import pandas as pd
import numpy as np

def children_exists(t):
    try:
        t
    except:
        var_exists = False
    else:
        var_exists = True
    return var_exists


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
    try:
        if children_exists(t.children[1].data):
            if t.children[1].data == "string_list":
                lst = get_list(t.children[1])
    except:
        lst = []

    data = {'Name': ['Tom', 'Joseph', 'Krish', 'John', 'Maria', 'Ion', 'Andreea'], 'Age': [20, 21, 19, 18, 21, 18, 21]}
    df = pd.DataFrame(data)

    if len(lst) > 0:
        df = df[lst]

    return df


def computation(t):
    if t.children[0].data == "measure":
        if t.children[0].children[0].children[0] == "mean":
            df = get_df(t.children[0].children[1])
            df_mean = 0

            var_exists = False
            try:
                t.children[0].children[2]
            except:
                var_exists = False
            else:
                var_exists = True

            if var_exists:
                if t.children[0].children[2].isdigit():
                    each = int(t.children[0].children[2])
                    df_each_x = df.groupby(np.arange(len(df))//each).mean()
                    df_mean = df_each_x
            else:
                mean = df.mean()
                df_mean = pd.DataFrame(mean, columns=['mean'])
            print(df_mean)
            return df_mean

    elif t.children[0].data == "percentage":
        print("percentage")
        df_percentage = 0
        df = get_df(t.children[0].children[1])

        # gen only numerical columns
        cols = np.where(df.dtypes != 'O')
        df_int = df[df.columns[cols]]

        # number of percents
        percents = t.children[0].children[0]
        percents = int(percents) / 100

        try:
            if children_exists(t.children[0].children[1].data):
                # if a range is given
                if t.children[0].children[1].data == "range":
                    start = t.children[0].children[1].children[0]
                    end = t.children[0].children[1].children[1]
                    start = int(start)
                    end = int(end) + 1

                    df_percentage = df_int.iloc[start:end] * percents
                    print(df_percentage)

                # no range given
                elif t.children[0].children[1].data == "df":
                    df_percentage = df_int * percents
                    print(df_percentage)
        except:
            print("Exception. No range or dataframe given!")
    return df_percentage

def run_instruction(t):
    if t.data == 'affirmation':
        run_instruction(t.children[0])

    elif t.data == 'assignment':

        key = t.children[0].children[0]

        if t.children[1].data == 'data_extraction':
            print("data extraction")
        elif t.children[1].data == 'computation':
            print("computation")
            computation(t.children[1])


def run_parser(program):
    parse_tree = parser.parse(program)
    print(parse_tree.pretty())
    for inst in parse_tree.children:
        run_instruction(inst)
    return parse_tree


def test():
    with open("source_code.txt") as source_code:
        source_code = source_code.read()
    run_parser(source_code)


with open("grammar.lark") as grammar:
    grammar = grammar.read()

parser = Lark(grammar)

if __name__ == '__main__':
    test()
