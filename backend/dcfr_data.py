import pandas as pd
import numpy as np
from backend.search_pmaw import CallPmaw
from backend.constants import FileType


class Data():

    # returns the sum of entries that match every field
    def sum_fields(df: pd.DataFrame, fields: list):
        sum_df = df.groupby(fields, sort=False).sum()

        # names the headers 'total field_name'
        headers = []
        for i in range(len(sum_df.columns)):
            headers.append ('total ' + sum_df.columns[i])
        sum_df.columns = headers
        return sum_df

    # saves the output of sum_fields() to a file
    def save_sum_fields(df: pd.DataFrame, fields: list, file, file_type: FileType, output):
        file = CallPmaw.add_file_type(file, file_type)
        if file_type == FileType.CSV.value:
            Data.sum_fields(df, fields).to_csv(file)
        elif file_type == FileType.XLSX.value:
            Data.sum_fields(df, fields).to_excel(file)
        print('Aggregate Sum saved to ' + file)
        output.send_message(f'Aggregate Sum saved to {file}')

    # returns the number of entries that match every field
    def count_fields(df: pd.DataFrame, fields: list):
        count_df = df.groupby(fields, sort=False).count().iloc[:, 0:len(fields)]
        count_df.columns = ['frequency']
        return count_df

    # saves the output of count_fields() to a file
    def save_count_fields(df: pd.DataFrame, fields: list, file, file_type: FileType, output):
        file = CallPmaw.add_file_type(file, file_type)
        if file_type == FileType.CSV.value:
            Data.count_fields(df, fields).to_csv(file)
        elif file_type == FileType.XLSX.value:
            Data.count_fields(df, fields).to_excel(file)
        print('Frequency saved to ' + file)
        output.send_message(f'Frequency saved to {file}')

    # returns the gini coeff of the entries of the first element of field
    def gini_coefficient(df: pd.DataFrame, field: list):
        x = df[field[0]].to_numpy()
        sorted_x = np.sort(x)
        n = len(x)
        cumx = np.cumsum(sorted_x, dtype=float)
        return (n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n

    # saves the output of gini_coefficient() to a file
    def save_gini_coefficient(df: pd.DataFrame, fields: list, file, file_type: FileType, output):
        file = CallPmaw.replace_file_type(file, file_type)
        gini = Data.gini_coefficient(df, fields)
        if file_type == FileType.CSV.value:
            pd.DataFrame({fields[0]+' Gini Coefficient': [gini]}).to_csv(file)
        elif file_type == FileType.XLSX.value:
            pd.DataFrame({fields[0]+' Gini Coefficient': [gini]}).to_excel(file)
        elif file_type == FileType.TXT.value:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(str(gini))
        print('Gini Coefficient of: '+str(gini)+' saved to ' + file)
        output.send_message(f'Gini Coefficient of: {str(gini)} saved to {file}')

    # verifies one field is selected and the first element is a number
    def gini_rule(df: pd.DataFrame, fields: list):
        if len(fields) != 1:
            return 'Only one group may be selected'
        try:
            int(df[fields[0]][0])
        except:
            return 'The group selected doesn\'t contain numbers'
        return True

    def true_rule(df: pd.DataFrame, fields: list):
        return True