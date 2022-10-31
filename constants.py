from enum import Enum

VERSION = '0.2.3'
APP_NAME = 'Dataset Collector for Reddit'
GUIDE_URL = 'https://docs.google.com/document/d/1ED5SsBsmFxjePdBnY-1NYSxkkXIOgKRVz4O0BIWQDFc/edit?usp=sharing'

COMMENT_WIDTH = 550
COMMENT_HEIGHT = 370

SUBMISSION_WIDTH = 540
SUBMISSION_HEIGHT = 620

DATA_WIDTH = 310
DATA_HEIGHT = 350

NOTEBOOK_WRAP = 15
TEXT_WRAP = 40

class FileType(Enum):
    CSV = '.csv'
    XLSX = '.xlsx'

class ExportFileType(Enum):
    CSV = '.csv'

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