from enum import Enum

VERSION = '0.3.0'
APP_NAME = 'Dataset Collector for Reddit'
GUIDE_URL = 'https://docs.google.com/document/d/1ED5SsBsmFxjePdBnY-1NYSxkkXIOgKRVz4O0BIWQDFc/edit?usp=sharing'

CRITICAL_MESSAGE = 'Report bugs to https://docs.google.com/forms/d/e/1FAIpQLSdEpWlfaD0TLDqUC8P58PUNMy_4wQdn-SMzfnD2gaH9vqkvAw/viewform. Please include this log in your report.'

COMMENT_WIDTH = 520
COMMENT_HEIGHT = 370

SUBMISSION_WIDTH = 550
SUBMISSION_HEIGHT = 620

DATA_WIDTH = 410
DATA_HEIGHT = 360

OUTPUT_WIDTH = 520
OUTPUT_HEIGHT = 160

NOTEBOOK_WRAP = 15
TEXT_WRAP = 40
OUTPUT_WRAP = 100

class NotebookPage(Enum):
    COMMENT_PAGE = 0
    SUBMISSION_PAGE = 1
    DATA_PAGE = 2
    OUTPUT_PAGE = 3
    GUIDE_PAGE = 4

class FileType(Enum):
    CSV = '.csv'
    XLSX = '.xlsx'
    TXT = '.txt'

class ExportFileType(Enum):
    CSV = '.csv'
    TXT = '.txt'

class ImportFileType(Enum):
    CSV = '.csv'
    XLSX = '.xlsx'

class SearchType(Enum):
    PMAW = 'Archived Data'
    PRAW = 'Reddit Data'

class DataType(Enum):
    AGGREGATE_SUM = 'Aggregate Sum'
    FREQUENCY = 'Frequency'
    GINI_COEFFICIENCT = 'Gini Coefficient'

COMMENT_RETURN_FIELDS = [
                    'all_awardings',
                    'archived',
                    'author',
                    'author_flair_text',
                    'body',
                    'collapsed',
                    'comment_type',
                    'controversiality',
                    'created_datetime',
                    'created_utc',
                    'gilded',
                    'is_submitter',
                    'link_id',
                    'locked',
                    'parent_id',
                    'retrieved_datetime',
                    'retrieved_utc',
                    'score',
                    'score_hidden',
                    'send_replies',
                    'stickied',
                    'subreddit',
                    'subreddit_id',
                    'subreddit_name_prefixed',
                    'subreddit_type',
                    'total_awards_received',
                    'treatment_tags'
    ]

SUBMISSION_RETURN_FIELDS = [
                    'all_awardings',
                    'allow_live_comments',
                    'author',
                    'author_flair_text',
                    'awarders',
                    'can_mod_post',
                    'contest_mode',
                    'created_datetime',
                    'created_utc',
                    'domain',
                    'full_link',
                    'is_created_from_ads_ui',
                    'is_crosspostable',
                    'is_meta',
                    'is_original_content',
                    'is_reddit_media_domain',
                    'is_robot_indexable',
                    'is_self',
                    'is_video',
                    'link_flair_text',
                    'locked',
                    'media_only',
                    'num_comments',
                    'num_crossposts',
                    'over_18',
                    'pinned',
                    'preview',
                    'retrieved_datetime',
                    'retrieved_on',
                    'score',
                    'selftext',
                    'send_replies',
                    'spoiler',
                    'stickied',
                    'subreddit',
                    'subreddit_subscribers',
                    'subreddit_type',
                    'title',
                    'total_awards_received',
                    'treatment_tags',
                    'upvote_ratio',
                    'url'
    ]