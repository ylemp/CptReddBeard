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
while True:
	submissions = r.get_subreddit('all').get_hot(limit=10)
	for sub in submissions:
		#print the title of the submission
		pprint.pprint(sub.title) 
		#gets 200 comments, the rest are 'more comments objects'
		all_comments = sub.comments 
		#replaces the more comment objects with comment objects, every 200 comments take additional 2 seconds
		sub.replace_more_comments(limit=None) 
		#flattens the comments tree to make it iterable 
		flat_comments = praw.helpers.flatten_tree(sub.comments)
		#for all of the comments for that submission
		for comment in flat_comments:
			#dictionary stores the submission with the body as the key and karma as the value
			#holds comment for current submission
			local_karma_by_comment[comment.body] = (local_karma_by_comment.get(comment.body, 0) + comment.score)
			#holds comments for all the submissions
			karma_by_comment[comment.body] = (karma_by_comment.get(comment.body, 0) + comment.score)
		#find and print the top comment for the currnet submission	
		local_max_comment = max( local_karma_by_comment.iteritems(),  key=itemgetter(1) )
		print('The top comment for this submission was')
		pprint.pprint(local_max_comment)
		local_karma_by_comment.clear()
	#find and print the top comment in all the submissions
	max_comment = max( karma_by_comment.iteritems(), key=itemgetter(1) )
	print('The top comment was')
	pprint.pprint(max_comment)
	karma_by_comment.clear()
	time.sleep(1800/2)