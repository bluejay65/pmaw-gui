from pmaw import PushshiftAPI
import pandas as pd
import platform
from constants import FileType, SearchType, VERSION, APP_NAME
from app_info import AppInfo
import praw, prawcore
from prawcore import auth, requestor
import secret_constants
from concurrent.futures import ThreadPoolExecutor


class CallPmaw:
    def __init__(self, output=None, executor=None, main_thread=None):
        self.praw = None
        self.output = output
        self.executor = executor
        self.main_thread = main_thread



    def get_comment_df(self, dict, search_type:SearchType):
        print("\nRunning...")

        q = dict['q']
        limit = dict['limit']
        fields: list = dict['fields']
        author = dict['author']
        subreddit = dict['subreddit']
        after = dict['after']
        before = dict['before']

        keep_fields = fields.copy()
        if 'created_datetime' in fields and 'created_utc' not in fields:
            fields.append('created_utc')
        if 'retrieved_datetime' in fields and 'retrieved_utc' not in fields:
            fields.append('retrieved_utc')

        print('here')

        if search_type == SearchType.PRAW.value:
            fields.append('id')
            if self.can_multithread():
                api = PushshiftAPI(praw=self.get_praw(), output=self.output, executor=self.executor, main_thread=self.main_thread)
            else:
                api = PushshiftAPI(praw=self.get_praw(), output=self.output)
        else:
            if self.can_multithread():
                api = PushshiftAPI(output=self.output, executor=self.executor, main_thread=self.main_thread)
            else:
                api = PushshiftAPI(output=self.output)

        if self.can_multithread():
            print('multithread')
            if isinstance(after, int) and isinstance(before, int):
                comments = self.executor.submit(api.search_comments, q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before)
            elif isinstance(after, int):
                comments = self.executor.submit(api.search_comments, q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after)
            elif isinstance(before, int):
                comments = self.executor.submit(api.search_comments, q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before)
            else:
                comments = self.executor.submit(api.search_comments, q=q, limit=limit, fields=fields, author=author, subreddit=subreddit)

            df = pd.DataFrame([comment for comment in comments.result()])
            print(df)
            print('Organizing collected data...')
            self.output.append('Organizing collected data...')
            
        else:
            print('not multithread')
            if isinstance(after, int) and isinstance(before, int):
                comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before)
            elif isinstance(after, int):
                comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after)
            elif isinstance(before, int):
                comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before)
            else:
                comments = api.search_comments(q=q, limit=limit, fields=fields, author=author, subreddit=subreddit)

            print('Organizing collected data...')
            self.output.append('Organizing collected data...')
            df = pd.DataFrame([comment for comment in comments])
            print(df)
            

        if df.empty:
            print('ERROR: No data returned. Pushshift may be offline, or your search filters may be too specific.')
            self.output.append('ERROR: No data returned. Pushshift may be offline, or your search filters may be too specific.')
            return df

        if 'created_datetime' in fields:
            df['created_datetime'] = pd.to_datetime(df.loc[:, 'created_utc'], unit='s', origin='unix')
        if 'retrieved_datetime' in fields and search_type == SearchType.PMAW.value:
            try:
                df['retrieved_datetime'] = pd.to_datetime(df.loc[:, 'retrieved_utc'], unit='s', origin='unix')
            except:
                pass
        df = self.remove_extra_fields(df, keep_fields)

        return df

    def get_submission_df(self, dict, search_type: SearchType):
        print("\nRunning...")
        self.output.new_append("Running...")

        q = dict['q']
        #q_not = dict['q:not']
        title = dict['title']
        #title_not = dict['title:not']
        selftext = dict['selftext']
        #selftext_not = dict['selftext:not']
        limit = dict['limit']
        fields: list = dict['fields']
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

        keep_fields = fields.copy()
        if 'created_datetime' in fields:
            fields.append('created_utc')
        if 'retrieved_datetime' in fields:
            fields.append('retrieved_on')

        if search_type == SearchType.PRAW.value:
            fields.append('id')

            api = PushshiftAPI(praw=self.get_praw())
        else:
            api = PushshiftAPI()

        if isinstance(after, int) and isinstance(before, int):
            submissions = api.search_submissions(q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
        elif isinstance(after, int):
            submissions = api.search_submissions(q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
        elif isinstance(before, int):
            submissions = api.search_submissions(q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
        else:
            submissions = api.search_submissions(q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)

        print('Organizing collected data...')
        self.output.append('Organizing collected data...')

        df = pd.DataFrame([s for s in submissions])
        if df.empty:
            print('ERROR: No data returned. Pushshift may be offline, or your search filters may be too specific.')
            self.output.append('ERROR: No data returned. Pushshift may be offline, or your search filters may be too specific.')
            return df

        if 'created_datetime' in fields:
            df['created_datetime'] = pd.to_datetime(df.loc[:, 'created_utc'], unit='s', origin='unix')
        if 'retrieved_datetime' in fields and search_type == SearchType.PMAW.value:
            try:
                df['retrieved_datetime'] = pd.to_datetime(df.loc[:, 'retrieved_on'], unit='s', origin='unix')
            except:
                pass
        df = self.remove_extra_fields(df, keep_fields)

        return df


    def save_comment_file(self, dict, file, file_type:FileType, search_type:SearchType):
        self.output.set_title('Downloading Comments')
        self.output.start_progress_bar()
        df = self.get_comment_df(dict, search_type)
        if not df.empty:
            file = CallPmaw.add_file_type(file, file_type)
            error = self.save_df_to_file(df, file, file_type)
            if not error:
                print('Comment data saved to ' + file)
                self.output.append('Comment data saved to ' + file)
        self.output.stop_progress_bar()
        
    def save_submission_file(self, dict, file, file_type:FileType, search_type:SearchType):
        df = self.get_submission_df(dict, search_type)
        if not df.empty:
            file = CallPmaw.add_file_type(file, file_type)
            error = self.save_df_to_file(df, file, file_type)
            if not error:
                print('Submission data saved to ' + file)
                self.output.append('Submission data saved to ' + file)

    def save_df_to_file(self, df, file, file_type:FileType):
        print('Saving organized data...')
        self.output.append('Saving organized data...')
        if file_type == FileType.CSV.value:
            try:
                df.to_csv(file)
            except:
                print('ERROR: Unable to save to file. Check if file is open in another program.')
                self.output.append('ERROR: Unable to save to file. Check if file is open in another program.')
                return -1
        elif file_type == FileType.XLSX.value:
            try:
                df.to_excel(file, index=False, engine='xlsxwriter')
            except:
                print('ERROR: Unable to save to file. Check if file is open in another program.')
                self.output.append('ERROR: Unable to save to file. Check if file is open in another program.')
                return -1
        else:
            raise ValueError('file_type was not an accepted value. Value was: '+ file_type)
        return None


    def remove_extra_fields(self, df: pd.DataFrame, fields: list):
        try:
            return df[fields]
        except:
            cols = df.columns
            safe_cols = []
            err_cols = []
            for field in fields:
                if field in cols:
                    safe_cols.append(field)
                else:
                    err_cols.append(field)
            print('WARNING: Requested Data '+str(err_cols)+' is not available')
            self.output.append('WARNING: Requested Data '+str(err_cols)+' is not available')
            return df[safe_cols]


    def get_praw(self):
        if self.praw is None:
            user_agent = 'User-Agent: '+platform.system()+': '+APP_NAME+' v'+VERSION+'(by u/'+secret_constants.USERNAME+')'
            reddit = praw.Reddit(
                        client_id=secret_constants.CLIENT_ID,
                        client_secret=None,
                        user_agent=user_agent,
                        check_for_updates=False,
                        comment_kind="t1",
                        message_kind="t4",
                        redditor_kind="t2",
                        submission_kind="t3",
                        subreddit_kind="t5",
                        trophy_kind="t6",
                        oauth_url="https://oauth.reddit.com",
                        reddit_url="https://www.reddit.com",
                        short_url="https://redd.it",
                        ratelimit_seconds=5,
                        timeout=16
                        )
            reddit._read_only_core = prawcore.session(
                                                    auth.DeviceIDAuthorizer(
                                                        authenticator=auth.UntrustedAuthenticator(
                                                            requestor=requestor.Requestor(
                                                                user_agent=user_agent,
                                                                timeout=16
                                                            ), 
                                                            client_id=secret_constants.CLIENT_ID, 
                                                            redirect_uri='http://localhost:8080'), 
                                                        device_id=AppInfo.get_device_id()
                                                        )
                                                    )
            self.praw = reddit

        return self.praw

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

    def add_file_type(file, file_type: str):
        if not file.endswith(file_type):
            file += file_type
        return file

    def can_multithread(self):
        if self.main_thread is not None and self.executor is not None:
            return True
        return False

"""
api = PushshiftAPI()
comments = api.search_comments(q='hello', subreddit='beauty', limit=500)
"""
