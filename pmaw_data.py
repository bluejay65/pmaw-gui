from search_pmaw import CallPmaw
import pandas as pd
from pmaw import PushshiftAPI
import numpy as np


class Data():
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.group_dict = {}

        print(df)

    def sum_fields(self, fields: list):
        fields_tuple = tuple(fields)
        if fields_tuple not in self.group_dict:
            self.group_dict[fields_tuple] = self.df.groupby(fields, sort=False)
        return self.group_dict[fields_tuple].sum()

    def count_fields(self, fields: list):
        fields_tuple = tuple(fields)
        if fields_tuple not in self.group_dict:
            self.group_dict[fields_tuple] = self.df.groupby(fields, sort=False)
        return self.group_dict[fields_tuple].count()


"""
test_df = pd.DataFrame([['user1', 4, 5],
                        ['user2', 1, 2],
                        ['user3', 3, 4],
                        ['user2', 4, 5],
                        ['user3', 30, 31],
                        ['user3', -200, -199]],
                        columns=['author', 'score', 'controversiality'])

data = Data(test_df)

print(data.sum_field('author'))
print(data.count_field('author'))
"""