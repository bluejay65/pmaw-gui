from pmaw import PushshiftAPI
import pandas as pd
import platform
from constants import FileType, SearchType, VERSION, APP_NAME, CRITICAL_MESSAGE
from app_info import AppInfo
import praw, prawcore
from prawcore import auth, requestor
import secret_constants
import logging

log = logging.getLogger(__name__)

class CallPmaw:
    def __init__(self, gui=None, output=None, executor=None, main_thread=None):
        self.praw = None
        self.gui = gui
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

        if search_type == SearchType.PRAW.value:
            fields.append('id')
            if self.can_multithread():
                api = PushshiftAPI(praw=self.get_praw(), output=self.output, executor=self.executor, main_thread=self.main_thread, shards_down_behavior=None)
            else:
                api = PushshiftAPI(praw=self.get_praw(), output=self.output, shards_down_behavior=None)
        else:
            if self.can_multithread():
                api = PushshiftAPI(output=self.output, executor=self.executor, main_thread=self.main_thread, shards_down_behavior=None)
            else:
                api = PushshiftAPI(output=self.output, shards_down_behavior=None)

        if self.can_multithread():
            if isinstance(after, int) and isinstance(before, int):
                comments = self.executor.submit(api.search_comments, q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before)
            elif isinstance(after, int):
                comments = self.executor.submit(api.search_comments, q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after)
            elif isinstance(before, int):
                comments = self.executor.submit(api.search_comments, q=q, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before)
            else:
                comments = self.executor.submit(api.search_comments, q=q, limit=limit, fields=fields, author=author, subreddit=subreddit)

            df = pd.DataFrame([comment for comment in comments.result()])
            if self.output.cancel_task:
                self.output.set_title('Download Cancelled')
                return
            self.output.update_progress_bar(1,1)
            print('Organizing collected data...')
            self.output.set_title('Organizing Collected Comments')
            
        else:
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

        if df.empty:
            log.warning('Returned empty dataframe from PMAW', exc_info=True)
            self.output.send_error('ERROR: No data returned. Your search filters may be too specific or Pushshift may be missing data.')
            return df

        if 'created_datetime' in fields:
            df['created_datetime'] = pd.to_datetime(df.loc[:, 'created_utc'], unit='s', origin='unix')
        if 'retrieved_utc' in df.columns and 'retrieved_datetime' in fields and search_type == SearchType.PMAW.value:
            df['retrieved_datetime'] = pd.to_datetime(df.loc[:, 'retrieved_utc'], unit='s', origin='unix')
        df = self.remove_extra_fields(df, keep_fields)

        return df

    def get_submission_df(self, dict, search_type: SearchType):
        print("\nRunning...")

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
            if self.can_multithread():
                api = PushshiftAPI(praw=self.get_praw(), output=self.output, executor=self.executor, main_thread=self.main_thread, shards_down_behavior=None)
            else:
                api = PushshiftAPI(praw=self.get_praw(), output=self.output, shards_down_behavior=None)
        else:
            if self.can_multithread():
                api = PushshiftAPI(output=self.output, executor=self.executor, main_thread=self.main_thread, shards_down_behavior=None)
            else:
                api = PushshiftAPI(output=self.output, shards_down_behavior=None)

        if self.can_multithread():
            if isinstance(after, int) and isinstance(before, int):
                submissions = self.executor.submit(api.search_submissions, q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, before=before, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
            elif isinstance(after, int):
                submissions = self.executor.submit(api.search_submissions, q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, after=after, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
            elif isinstance(before, int):
                submissions = self.executor.submit(api.search_submissions, q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, before=before, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
            else:
                submissions = self.executor.submit(api.search_submissions, q=q, title=title, selftext=selftext, limit=limit, fields=fields, author=author, subreddit=subreddit, over_18=over_18, is_video=is_video, locked=locked, stickied=stickied, spoiler=spoiler, contest_mode=contest_mode)
        
            df = pd.DataFrame([submission for submission in submissions.result()])
            if self.output.cancel_task:
                self.output.set_title('Download Cancelled')
                return
            self.output.update_progress_bar(1,1)
            print('Organizing collected data...')
            self.output.set_title('Organizing Collected Submissions')

        else:
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

        if df.empty:
            print('ERROR: No data returned. Your search filters may be too specific or Pushshift may be missing data.')
            self.output.send_error('ERROR: No data returned. Your search filters may be too specific or Pushshift may be missing data.')
            return df

        if 'created_datetime' in fields:
            df['created_datetime'] = pd.to_datetime(df.loc[:, 'created_utc'], unit='s', origin='unix')
        if 'retrieved_utc' in df.columns and 'retrieved_datetime' in fields and search_type == SearchType.PMAW.value:
            df['retrieved_datetime'] = pd.to_datetime(df.loc[:, 'retrieved_on'], unit='s', origin='unix')
        df = self.remove_extra_fields(df, keep_fields)

        return df


    def save_comment_file(self, dict, file, file_type:FileType, search_type:SearchType):
        log.info('Starting comment search of %s for %s', search_type, str(dict))
        try:
            self.gui.disable_run()
            self.output.reset()
            self.output.set_title('Searching for Comments')
            self.output.start_progress_bar()
            df = self.get_comment_df(dict, search_type)
            if self.output.cancel_task:
                self.gui.enable_run()
                return
            if not df.empty:
                file = CallPmaw.add_file_type(file, file_type)
                error = self.save_df_to_file(df, file, file_type)
                if not error:
                    print('Comment data saved to ' + file)
                    self.output.set_save_file(file)
                    self.output.set_title('Comments Saved')
            self.gui.enable_run()
        except:
            log.critical(CRITICAL_MESSAGE, exc_info=True)
                
        
    def save_submission_file(self, dict, file, file_type:FileType, search_type:SearchType):
        log.info('Starting submission search of %s for %s', search_type, str(dict))
        try:
            self.gui.disable_run()
            self.output.reset()
            self.output.set_title('Searching for Submissions')
            self.output.start_progress_bar()
            df = self.get_submission_df(dict, search_type)
            if self.output.cancel_task:
                self.gui.enable_run()
                return
            if not df.empty:
                file = CallPmaw.add_file_type(file, file_type)
                error = self.save_df_to_file(df, file, file_type)
                if not error:
                    print('Submission data saved to ' + file)
                    self.output.set_save_file(file)
                    self.output.set_title('Submissions Saved')
            self.gui.enable_run()
        except:
            log.critical(CRITICAL_MESSAGE, exc_info=True)


    def save_df_to_file(self, df, file, file_type:FileType):
        print('Saving organized data...')
        if file_type == FileType.CSV.value:
            try:
                df.to_csv(file)
            except:
                log.debug('Unable to save dataframe to file.', exc_info=True)
                self.output.send_error('ERROR: Unable to save to file. Check if file is open in another program.')
                return -1
        elif file_type == FileType.XLSX.value:
            try:
                df.to_excel(file, index=False, engine='xlsxwriter')
            except:
                log.debug('Unable to save dataframe to file.', exc_info=True)
                self.output.send_error('ERROR: Unable to save to file. Check if file is open in another program.')
                return -1
        else:
            log.error('file_type was not an accepted value. Value was: %s', file_type, exc_info=True)
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
            log.warning('Requested Data %s is not available', str(err_cols), exc_info=True)
            self.output.send_error('WARNING: Requested Data '+str(err_cols)+' is not available')
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

    def remove_file_type(file):
        file_type_list = [member.value for member in FileType]
        while True:
            for file_type in file_type_list:
                if file.endswith(file_type):
                    file = file[:file.rfind(file_type)]
                    continue
            break
        return file

    def replace_file_type(file, file_type):
        file = CallPmaw.remove_file_type(file)
        return CallPmaw.add_file_type(file, file_type)

    def can_multithread(self):
        if self.main_thread is not None and self.executor is not None:
            return True
        return False

"""
api = PushshiftAPI()
comments = api.search_comments(q='hello', subreddit='beauty', limit=500)
"""
