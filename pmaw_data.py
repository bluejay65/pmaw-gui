from msilib.schema import File
import pandas as pd
from search_pmaw import CallPmaw
from constants import FileType


class Data():
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.group_dict = {}

    def sum_fields(self, fields: list):
        fields_tuple = tuple(fields)
        if fields_tuple not in self.group_dict:
            self.group_dict[fields_tuple] = self.df.groupby(fields, sort=False)
        sum_df = self.group_dict[fields_tuple].sum()

        headers = []
        for i in range(len(sum_df.columns)):
            headers.append ('total ' + sum_df.columns[i])
        sum_df.columns = headers
        return sum_df

    def save_sum_fields(self, fields: list, file, file_type: FileType):
        file = CallPmaw.add_file_type(file, file_type)
        if file_type == FileType.CSV.value:
            self.sum_fields(fields).to_csv(file)
        elif file_type == FileType.XLSX.value:
            df = self.sum_fields(fields)
            df.to_excel(file)
        print('Aggregate Sum saved to ' + file)


    def count_fields(self, fields: list):
        fields_tuple = tuple(fields)
        if fields_tuple not in self.group_dict:
            self.group_dict[fields_tuple] = self.df.groupby(fields, sort=False)
        count_df = self.group_dict[fields_tuple].count().iloc[:, 0:len(fields)]
        count_df.columns = ['frequency']
        return count_df

    def save_count_fields(self, fields: list, file, file_type: FileType):
        file = CallPmaw.add_file_type(file, file_type)
        if file_type == FileType.CSV.value:
            self.count_fields(fields).to_csv(file)
        elif file_type == FileType.XLSX.value:
            self.count_fields(fields).to_excel(file)
        else:
            print
        print('Frequency saved to ' + file)


"""
test_df = pd.DataFrame([['user1', 4, 5],
                        ['user2', 1, 2],
                        ['user3', 3, 4],
                        ['user2', 4, 5],
                        ['user3', 30, 31],
                        ['user3', -200, -199]],
                        columns=['author', 'score', 'controversiality'])

data = Data(test_df)

print(data.sum_fields('author'))
print(data.count_fields('author'))
"""
