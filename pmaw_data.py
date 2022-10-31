import pandas as pd
import numpy as np
from search_pmaw import CallPmaw
from constants import FileType


class Data():
    def sum_fields(df: pd.DataFrame, fields: list):
        sum_df = df.groupby(fields, sort=False).sum()

        headers = []
        for i in range(len(sum_df.columns)):
            headers.append ('total ' + sum_df.columns[i])
        sum_df.columns = headers
        return sum_df

    def save_sum_fields(df: pd.DataFrame, fields: list, file, file_type: FileType):
        file = CallPmaw.add_file_type(file, file_type)
        if file_type == FileType.CSV.value:
            Data.sum_fields(df, fields).to_csv(file)
        elif file_type == FileType.XLSX.value:
            Data.sum_fields(df, fields).to_excel(file)
        print('Aggregate Sum saved to ' + file)


    def count_fields(df: pd.DataFrame, fields: list):
        count_df = df.groupby(fields, sort=False).count().iloc[:, 0:len(fields)]
        count_df.columns = ['frequency']
        return count_df

    def save_count_fields(df: pd.DataFrame, fields: list, file, file_type: FileType):
        file = CallPmaw.add_file_type(file, file_type)
        if file_type == FileType.CSV.value:
            Data.count_fields(df, fields).to_csv(file)
        elif file_type == FileType.XLSX.value:
            Data.count_fields(df, fields).to_excel(file)
        print('Frequency saved to ' + file)

    
    def gini_coefficient(df: pd.DataFrame, fields: list):
        x = df[fields[0]].to_numpy()
        sorted_x = np.sort(x)
        n = len(x)
        cumx = np.cumsum(sorted_x, dtype=float)
        return (n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n

    def save_gini_coefficent(df: pd.DataFrame, fields: list, file, file_type: FileType):
        file = CallPmaw.add_file_type(file, file_type)
        gini = Data.gini_coefficient(df, fields)
        if file_type == FileType.CSV.value:
            pd.DataFrame({fields[0]+' Gini Coefficient': [gini]}).to_csv(file)
        elif file_type == FileType.XLSX.value:
            pd.DataFrame({fields[0]+' Gini Coefficient': [gini]}).to_excel(file)
        print('Gini Coefficient of: '+str(gini)+' saved to ' + file)

#TODO: fix error when not selecting file
#TODO: make gini coefficient save in file?
#TODO: make it more clear which data thing is selected
#TODO: move data file button
#TODO: add human readable data field

"""
a = random.random()*10000
b = random.random()*10000
c = random.random()*10000
d = random.random()*10000
e = random.random()*10000
f = random.random()*10000

print(str(a)+', '+str(b)+', '+str(c)+', '+str(d)+', '+str(e)+', '+str(f))

test_df = pd.DataFrame([['user1', a],
                        ['user2', b],
                        ['user3', c],
                        ['user2', d],
                        ['user3', e],
                        ['user3', f]],
                        columns=['author', 'frequency'])


print(Data.gini_coefficient(test_df, ['frequency']))
"""
