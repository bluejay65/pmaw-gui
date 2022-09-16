import pandas as pd


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

    def save_sum_fields_csv(self, fields: list, file):
        self.sum_fields(fields).to_csv(file)
        print('Aggregate Sum saved to ' + file)


    def count_fields(self, fields: list):
        fields_tuple = tuple(fields)
        if fields_tuple not in self.group_dict:
            self.group_dict[fields_tuple] = self.df.groupby(fields, sort=False)
        count_df = self.group_dict[fields_tuple].count().iloc[:, 0:len(fields)]
        count_df.columns = ['frequency']
        return count_df

    def save_count_fields_csv(self, fields: list, file):
        self.count_fields(fields).to_csv(file)
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
