import time
import praw
import pprint
from datetime import timedelta
from operator import itemgetter
from praw.handlers import MultiprocessHandler

handler = MultiprocessHandler()
r = praw.Reddit('User-Agent: Finds the top comment by /u/ylemp v 1.0. '
                            'https://github.com/ylemp/CptReddBeard'
                            )
r.login()
local_karma_by_comment = {}
karma_by_comment = {}
pp = pprint.PrettyPrinter(indent=4)
while True:
	submissions = r.get_subreddit('all').get_hot(limit=10)
	for sub in submissions:
		pp.pprint(sub.title) 
		all_comments = sub.comments 
		sub.replace_more_comments(limit=0) 
		flat_comments = praw.helpers.flatten_tree(sub.comments)
		for comment in flat_comments:
			local_karma_by_comment[comment.body] = (local_karma_by_comment.get(comment.body, 0) + comment.score)
			karma_by_comment[comment.body] = (karma_by_comment.get(comment.body, 0) + comment.score)
		local_max_comment = max( local_karma_by_comment.iteritems(),  key=itemgetter(1) )
		print('THE TOP COMMENT FOR THIS THREAD WAS')
		pprint.pprint(local_max_comment)
		local_karma_by_comment.clear()
	max_comment = max( karma_by_comment.iteritems(), key=itemgetter(1) )
	print('THE TOP COMMENT WAS')
	pprint.pprint(max_comment)
	time.sleep(1800/2)