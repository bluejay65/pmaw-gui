import argparse 
from backend.search_pmaw import CallPmaw


parser = argparse.ArgumentParser()
parser.add_argument('--q', type=str)
#parser.add_argument('--ids', type=str, required=True, nargs='+') TODO add ids
parser.add_argument('--limit', type=int)
parser.add_argument('--fields', type=str, nargs='+')
parser.add_argument('--author', type=str)
parser.add_argument('--subreddit', type=str)
parser.add_argument('--after', type=int)
parser.add_argument('--before', type=int)
parser.add_argument('--file' , type=str)

args = parser.parse_args()
args_dict = vars(args)

api = CallPmaw()
api.get_df(args_dict)