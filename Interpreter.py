from Variable import Variable
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


class Interpreter:
    tree = ''  # name

    def __init__(self, tree):
        self.tree = tree

    def children_exists(self, t):
        try:
            t
        except:
            var_exists = False
        else:
            var_exists = True
        return var_exists

    def get_list(self, t):
        i = 0
        lst = []
        while True:
            try:
                lst.append(t.children[i].children[0])
                i = i + 1
            except:
                break
        return lst

    def get_df(self, t):
        key_name = t.children[0]
        try:
            if self.children_exists(t.children[1].data):
                if t.children[1].data == "string_list":
                    lst = self.get_list(t.children[1])
        except:
            lst = []

        data = {'Name': ['Tom', 'Joseph', 'Krish', 'John', 'Maria', 'Ion', 'Andreea'],
                'Age': [20, 21, 19, 18, 21, 18, 21]}
        df = pd.DataFrame(data)

        if len(lst) > 0:
            df = df[lst]

        return df

    def compute_measure(self, t, measure):
        df = self.get_df(t.children[0].children[1])
        df_res = 0

        try:
            t.children[0].children[2]
        except:
            var_exists = False
        else:
            var_exists = True

        if measure != "mode":

            if var_exists:
                if t.children[0].children[2].isdigit():
                    each = int(t.children[0].children[2])
                    if measure == "mean":
                        df_each_x = df.groupby(np.arange(len(df)) // each).mean()
                    elif measure == "stdev":
                        df_each_x = df.groupby(np.arange(len(df)) // each).std()
                    elif measure == "max":
                        df_each_x = df.groupby(np.arange(len(df)) // each).max()
                    elif measure == "min":
                        df_each_x = df.groupby(np.arange(len(df)) // each).min()
                    elif measure == "median":
                        df_each_x = df.groupby(np.arange(len(df)) // each).median()
                    elif measure == "sum":
                        df_each_x = df.groupby(np.arange(len(df)) // each).sum()
                    try:
                        df_res = df_each_x
                        return df_res
                    except:
                        print("An error occurred when trying to compute", measure)
            else:
                if measure == "mean":
                    temp_df = df.mean()
                elif measure == "stdev":
                    temp_df = df.std()
                elif measure == "max":
                    temp_df = df.max()
                elif measure == "min":
                    temp_df = df.min()
                elif measure == "median":
                    temp_df = df.median()
                elif measure == "sum":
                    temp_df = df.sum()
                df_res = pd.DataFrame(temp_df, columns=[measure])
                return df_res

        elif measure == "mode" and var_exists == True:
            print("This action cannot be performed with measure mean")
        else:
            df_res = df.mode()
            return df_res

    def compute_percentage(self, t):
        df_percentage = 0
        df = self.get_df(t.children[1])

        # gen only numerical columns
        cols = np.where(df.dtypes != 'O')
        df_int = df[df.columns[cols]]

        # number of percents
        percents = t.children[0]
        percents = int(percents) / 100

        try:
            if self.children_exists(t.children[1].data):
                # if a range is given
                if t.children[1].data == "range":
                    start = t.children[1].children[0]
                    end = t.children[1].children[1]
                    start = int(start)
                    end = int(end) + 1

                    df_percentage = df_int.iloc[start:end] * percents

                # no range given
                elif t.children[1].data == "df":
                    df_percentage = df_int * percents
        except:
            print("Exception. No range or dataframe given!")
        return df_percentage

    def computation(self, t):
        if t.children[0].data == "measure":
            if t.children[0].children[0].children[0] == "mean":
                result = self.compute_measure(t, "mean")
                return result
            elif t.children[0].children[0].children[0] == "stdev":
                result = self.compute_measure(t, "stdev")
                return result
            elif t.children[0].children[0].children[0] == "max":
                result = self.compute_measure(t, "max")
                return result
            elif t.children[0].children[0].children[0] == "min":
                result = self.compute_measure(t, "min")
                return result
            elif t.children[0].children[0].children[0] == "median":
                result = self.compute_measure(t, "median")
                return result
            elif t.children[0].children[0].children[0] == "mode":
                result = self.compute_measure(t, "mode")
                return result
            elif t.children[0].children[0].children[0] == "sum":
                result = self.compute_measure(t, "sum")
                return result

        elif t.children[0].data == "percentage":
            result = self.compute_percentage(t.children[0])
            return result

    def plot_df(self, t):

        df = self.get_df(t.children[1])

        if t.children[0] == "lmplot" or t.children[0] == "scatterplot" or t.children[0] == "barplot":
            if t.children[2].data == "columns":

                X = t.children[2].children[0]
                Y = t.children[2].children[1]

                if t.children[0] == "lmplot":

                    # encoding categorial values
                    replace_map = {}
                    df1 = df.copy()
                    for i in df.columns:
                        if df[i].dtypes == 'O':
                            labels = df[i].astype('category').cat.categories.tolist()
                            replace_map = {i: {k: v for k, v in zip(labels, list(range(0, len(labels))))}}
                    df1.replace(replace_map, inplace=True)

                    print("LMPLOT REPLACED VALUES:")
                    print(replace_map)
                    print()
                    sns.lmplot(x=X, y=Y, data=df1)
                    plt.show()
                elif t.children[0] == "scatterplot":
                    sns.scatterplot(x=X, y=Y, data=df)
                    plt.show()
                elif t.children[0] == "barplot":
                    sns.barplot(x=X, y=Y, data=df)
                    plt.show()

            else:
                print("WARNING! Columns X and Y need to be specified!")

        elif t.children[0] == "displot" or t.children[0] == "countplot":
            if t.children[2].data == "column":

                X = t.children[2].children[0]

                if t.children[0] == "displot":
                    sns.displot(x=X, data=df)
                    plt.show()
                elif t.children[0] == "countplot":
                    sns.countplot(x=X, data=df)
                    plt.show()
            else:
                print("WARNING! Only X column needs to be specified!")

        # child[1] = dataframe which is plotted
        # if t.children[2].data = column : else:
        # x = t.children[2].children[0]
        # y = t.children[2].children[1]
        #print(t.children[2].children[0])
        return

    def run_instruction(self, t):
        if t.data == 'affirmation':
            self.run_instruction(t.children[0])
            if t.children[0].data == "plot":
                self.plot_df(t.children[0])

        elif t.data == 'assignment':
            key = t.children[0].children[0]
            value = int()

            if t.children[1].data == 'data_extraction':
                print("data extraction")
            elif t.children[1].data == 'computation':
                value = self.computation(t.children[1])

            # assigning value to the variable
            globals()[key] = Variable(key, value)
            print(value)

    def run_interpreter(self):
        for inst in self.tree.children:
            self.run_instruction(inst)
