from pmaw import PushshiftAPI
import pandas as pd
import os


class CallPmaw:

    def __init__(self) -> None:
        self.api = PushshiftAPI()

    def get_df(self, dict):
        q = dict['q']
        limit = dict['limit']
        fields = dict['fields']
        author = dict['author']
        subreddit = dict['subreddit']
        after = dict['after']
        before = dict['before']

        if isinstance(after, int) and isinstance(before, int):
            comments = self.api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before)
        elif isinstance(after, int):
            comments = self.api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after)
        elif isinstance(before, int):
            comments = self.api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before)
        else:
            comments = self.api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit)

        comment_list = [comment for comment in comments]

        return pd.DataFrame(comment_list)

        

    
    def save_csv(self, dict, file):
        self.get_df(dict).to_csv(file)

        print('\nData saved to ' + file)