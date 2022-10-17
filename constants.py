from enum import Enum

version = '0.2.1'

comment_width = 550
comment_height = 380

submission_width = 540
submission_height = 625

data_width = 310
data_height = 350

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

comment_return_fields = [
                    'all_awardings',
                    'archived',
                    'author',
                    'author_flair_text',
                    'body',
                    'collapsed',
                    'comment_type',
                    'controversiality',
                    'created_utc',
                    'datetime',
                    'gilded',
                    'is_submitter',
                    'link_id',
                    'locked',
                    'parent_id',
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

submission_return_fields = [
                    'all_awardings',
                    'allow_live_comments',
                    'author',
                    'author_flair_text',
                    'awarders',
                    'can_mod_post',
                    'contest_mode',
                    'created_utc',
                    'datetime',
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