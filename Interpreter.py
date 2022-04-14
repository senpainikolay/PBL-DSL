from Variable import Variable
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


class Interpreter:
    # class which contains functions for code interpretation

    tree = ''  # name

    def __init__(self, tree):
        """
            The constructor of the Class
                :param tree: lark tree
                    The generated tree after parsing
        """
        self.tree = tree

    def children_exists(self, t):
        """
            Function to check if a given subtree / variable exists
                :param t:  lark tree
                    the subtree or variable
                :return: boolean
                    True if the value exists, False otherwise
        """

        try:
            t
        except:
            var_exists = False
        else:
            var_exists = True

        return var_exists

    def get_list(self, t):
        """
            Function to get the items contained in a list
                :param t: lark subtree
                :return: 1d list
        """
        # initate an empty list lst and its length i = 0
        i = 0
        lst = []

        # cycle to add values to the list
        while True:
            try:
                lst.append(t.children[i].children[0])
                i = i + 1
            except:
                break

        return lst

    def get_df(self, t):
        """
            Function to get the value of the specified dataframe
                :param t: lark tree
                :return: pandas dataframe
        """
        # getting the identifier of the dataframe
        if t.data == "df":
            key = t.children[0]

        # gets the list of columns if only some columns of the dataframe were specified
        try:
            if self.children_exists(t.children[1].data):
                if t.children[1].data == "string_list":
                    lst = self.get_list(t.children[1])
        except:
            lst = []

        # data to test the current functions of the DSL, since data extraction is not yet integrated (in progress)
        data = {'Name': ['Tom', 'Joseph', 'Krish', 'John', 'Maria', 'Ion', 'Andreea'],
                'Age': [20, 21, 19, 18, 21, 18, 21]}
        df = pd.DataFrame(data)
        if key == "a":
            globals()[key] = Variable(key, df)

        # getting the value of the df
        value = globals()[key].value

        # get the columns if only one part of the dataframe should be used
        if len(lst) > 0:
            df = value[lst]

        return df

    def compute_measure(self, t, measure):
        """
            :param t: lark tree
            :param measure: string
                The measure which needs to be computed
            :return: pandas df
                Dataframe with the computed value(s)
        """
        # getting the dataframe on which the computation should be performed
        df = self.get_df(t.children[0].children[1])

        # initiating a variable for storng the result
        df_res = 0

        # checking if there is code specifying which rows should be grouped
        try:
            t.children[0].children[2]
        except:
            var_exists = False
        else:
            var_exists = True

        # computing the desired value for all kind of measures except mode
        if measure != "mode":
            # if some rows should be grouped
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

            # code for computing measures without grouping rows
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

        # if measure == mode and columns should be grouped print error
        elif measure == "mode" and var_exists == True:
            print("This action cannot be performed with measure mean")

        # if measure == mode and no errors, compute mode
        elif measure == "mode":
            df_res = df.mode()
            return df_res

    def compute_percentage(self, t):
        """
            Function for computing the percentage
                :param t: lark tree
                :return: pandas dataframe
        """
        # initiate a variable for storing the result
        df_percentage = 0

        # getting the df in case no range is specified
        if t.children[1].data == "df":
            df = self.get_df(t.children[1])

        # getting the df in case there is a specified range
        else:
            df = self.get_df(t.children[2])

        # gen only numerical columns
        cols = np.where(df.dtypes != 'O')
        df_int = df[df.columns[cols]]

        # getting the number of percents
        percents = t.children[0]
        percents = int(percents) / 100

        try:
            if self.children_exists(t.children[1].data):
                # compute percentage if a range is given
                if t.children[1].data == "range":
                    try:
                        # compute percentage from start to finish
                        start = t.children[1].children[0]
                        end = t.children[1].children[1]
                        start = int(start)
                        end = int(end) + 1
                        df_percentage = df_int.iloc[start:end] * percents
                    except:
                        # compute percentage on a single specified row
                        start = t.children[1].children[0]
                        start = int(start)
                        df_percentage = df_int.iloc[start] * percents

                # compute percentage in case no range given
                elif t.children[1].data == "df":
                    df_percentage = df_int * percents
        except:
            # print error
            print("Exception. No range or dataframe given!")

        return df_percentage

    def computation(self, t):
        """
            Function for detecting the computation to be performed
            :param t: lark tree
            :return: pandas df
        """
        # in case measure needs to be computed, find the value and call the function compute_measure with correct params
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

        # in case percentage needs to be computed, call function compute_percentage
        elif t.children[0].data == "percentage":
            result = self.compute_percentage(t.children[0])
            return result

    def plot_df(self, t):
        """
            Function for plotting dataframes
                :param t: lark tree
        """

        # getting the df which would be plotted
        df = self.get_df(t.children[1])

        # in case type of the plot needs both x and y columns specified
        if t.children[0] == "lmplot" or t.children[0] == "scatterplot" or t.children[0] == "barplot":

            # get the column names in case 2 columns are specified
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

                    # printing the replaced values for lmplot since it doesn't work on string values
                    print("LMPLOT REPLACED VALUES:")
                    print(replace_map)
                    print()

                    # showing the plot
                    sns.lmplot(x=X, y=Y, data=df1)
                    plt.show()

                elif t.children[0] == "scatterplot":
                    # showing the plot
                    sns.scatterplot(x=X, y=Y, data=df)
                    plt.show()
                elif t.children[0] == "barplot":
                    # showing the plot
                    sns.barplot(x=X, y=Y, data=df)
                    plt.show()
            # in case only 1 column was specified
            else:
                print("WARNING! Columns X and Y need to be specified!")

        # in case type of the plot needs only x column specified
        elif t.children[0] == "displot" or t.children[0] == "countplot":
            if t.children[2].data == "column":

                # getting the column name
                X = t.children[2].children[0]

                # showing the plots
                if t.children[0] == "displot":
                    sns.displot(x=X, data=df)
                    plt.show()
                elif t.children[0] == "countplot":
                    sns.countplot(x=X, data=df)
                    plt.show()
            else:
                # in case 2 columns were specified
                print("WARNING! Only X column needs to be specified!")

    def run_instruction(self, t):
        """
            Function for detecting instructions to be interpreted
                :param t:lark tree
        """
        if t.data == 'affirmation':
            self.run_instruction(t.children[0])

            # plot dataframe
            if t.children[0].data == "plot":
                self.plot_df(t.children[0])

            # print dataframe
            elif t.children[0].data == "show":
                key = t.children[0].children[0].children[0]
                try:
                    print("Value of", key, ":")
                    print(globals()[key].value)
                    print()
                except:
                    print("WARNING! No variable named", key)

            # saving dataframe
            elif t.children[0].data == "save":
                # getting the dataframe
                data = self.get_df(t.children[0].children[0])

                # getting the saving format
                f = t.children[0].children[1].children[0]

                # getting the specified name
                name = t.children[0].children[2].children[0]
                save_name = name + "." + f

                if f == "csv":
                    data.to_csv(save_name, index=False)
                elif f == "xlsx":
                    data.to_excel(save_name, index=False)

        # assigning value to a variable
        elif t.data == 'assignment':

            # getting the name of the variable
            key = t.children[0].children[0]

            # initializing an empty variable for the value which would be stored with the specified key name
            value = int()

            # functionality for data exctraction to be added
            if t.children[1].data == 'data_extraction':
                print("data extraction")

            # in case a computation needs to be performed
            elif t.children[1].data == 'computation':
                # assigning value with the result of the computation
                value = self.computation(t.children[1])

            # assigning value to the key
            globals()[key] = Variable(key, value)

    def run_interpreter(self):
        """
            Function to run the interpreter
        """
        # iterating trough the subtrees og the lark tree and running each instruction
        for inst in self.tree.children:
            self.run_instruction(inst)
