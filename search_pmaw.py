from sqlite3 import Row
from pmaw import PushshiftAPI
import pandas as pd
import numpy as np
from constants import FileType
import praw


class CallPmaw:

    def get_comment_df(dict):
        print("Running...")

        username = dict['username']
        q = dict['q']
        limit = dict['limit']
        fields = dict['fields']
        author = dict['author']
        subreddit = dict['subreddit']
        after = dict['after']
        before = dict['before']

        fields.append('id')

        reddit = praw.Reddit(
                            client_id='zoRBoAT4ZIBxyoY6iq7GNg',
                            client_secret=None,
                            user_agent=f'python: PMAW request enrichment (by u/'+username+')' #TODO make this an entered username
                            )
        api = PushshiftAPI(praw=reddit)

        if isinstance(after, int) and isinstance(before, int):
            comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before)
        elif isinstance(after, int):
            comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after)
        elif isinstance(before, int):
            comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before)
        else:
            comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit)

        print('Organizing collected data...')

        df = pd.DataFrame([comment for comment in comments])
        if 'datetime' in fields:
            df['datetime'] = pd.to_datetime(df.loc[:, 'created_utc'], unit='s', origin='unix')
        df = CallPmaw.remove_extra_fields(df, fields)

        return df

    def get_submission_df(dict):
        print("Running...")

        username = dict['username']
        q = dict['q']
        #q_not = dict['q:not']
        title = dict['title']
        #title_not = dict['title:not']
        selftext = dict['selftext']
        #selftext_not = dict['selftext:not']
        limit = dict['limit']
        fields = dict['fields']
        author = dict['author']
        subreddit = dict['subreddit']
        after = dict['after']
        before = dict['before']
        over_18 = dict['over_18']
        is_video = dict['is_video']
        locked = dict['locked']
        stickied = dict['stickied']
        spoiler = dict['spoiler']
        contest_mode = dict['contest_mode']

        fields.append('id')

        reddit = praw.Reddit(
                            client_id='zoRBoAT4ZIBxyoY6iq7GNg',
                            client_secret=None,
                            user_agent=f'python: PMAW request enrichment (by u/'+username+')'
                            )
        api = PushshiftAPI(praw=reddit)

        if isinstance(after, int) and isinstance(before, int):
            submissions = api.search_submissions(q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
        elif isinstance(after, int):
            submissions = api.search_submissions(q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
        elif isinstance(before, int):
            submissions = api.search_submissions(q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
        else:
            submissions = api.search_submissions(q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)

        print('Organizing collected data...')

        df = pd.DataFrame([s for s in submissions])
        if 'datetime' in fields:
            df['datetime'] = pd.to_datetime(df.loc[:, 'created_utc'], unit='s', origin='unix')
        df = CallPmaw.remove_extra_fields(df, fields)

        return df


    def save_comment_file(dict, file, file_type:FileType):
        df = CallPmaw.get_comment_df(dict)
        file = CallPmaw.add_file_type(file, file_type)
        CallPmaw.save_df_to_file(df, file, file_type)
        print('\nComment data saved to ' + file)
        
    def save_submission_file(dict, file, file_type:FileType):
        df = CallPmaw.get_submission_df(dict)
        file = CallPmaw.add_file_type(file, file_type)
        CallPmaw.save_df_to_file(df, file, file_type)
        print('\nSubmission data saved to ' + file)

    def save_df_to_file(df, file, file_type:FileType):
        print('Saving organized data...')
        if file_type == FileType.CSV.value:
            df.to_csv(file)
        elif file_type == FileType.XLSX.value:
            df.to_excel(file, index=False, engine='xlsxwriter')
        else:
            raise ValueError('file_type was not an accepted value. Value was: '+ file_type)


    def remove_extra_fields(df: pd.DataFrame, fields: list):
        return df[fields]

    def add_datetime(epoch_col):
        print(np.datetime64(epoch_col, 's'))

    def get_csv_cols(file):
        with open(file, encoding="utf-8") as f:
            line = f.readline()

        headers = line.split(',')
        headers.pop(0)
        headers[-1] = headers[-1].strip()
        return headers

    def get_xlsx_cols(file):
        df = pd.read_excel(file)
        return df.columns

    def add_file_type(file, file_type):
        if not file.endswith(file_type):
            file += file_type
        return file