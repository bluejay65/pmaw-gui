from pmaw import PushshiftAPI
import pandas as pd
import os


class CallPmaw:

    def get_df(dict):
        api = PushshiftAPI()

        q = dict['q']
        limit = dict['limit']
        fields = dict['fields']
        author = dict['author']
        subreddit = dict['subreddit']
        after = dict['after']
        before = dict['before']

        if isinstance(after, int) and isinstance(before, int):
            comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before)
        elif isinstance(after, int):
            comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after)
        elif isinstance(before, int):
            comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before)
        else:
            comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit)

        comment_list = [comment for comment in comments]

        return pd.DataFrame(comment_list)

    
    def save_csv(dict, file):
        CallPmaw.get_df(dict).to_csv(file)

        print('\nData saved to ' + file)


    def get_csv_cols(file):
        with open(file, encoding="utf-8") as f:
            line = f.readline()

        headers = line.split(',')
        headers.pop(0)
        headers[-1] = headers[-1].strip()
        return headers