import requests
import json
import re 
import praw
import os
#import glob
import sys
from os import listdir
from os.path import isfile, join

RESPONSE_OK = 200
MIN_KARMA = 35
chunk_size = 4096
number_of_posts = 1000
NO_OF_SUBREDDITS = 50
TESTING = False
NO_SAVE = False
INPUT_FILE = "all_links.txt"
DIR = "general"

subreddits = []
images = []
saved_files = []

# Read the file (for now)
# In future, read directly from reddit or command line
# Depending on the type, download image and save it

def saveImage(url, subreddit, filename):
	if TESTING or NO_SAVE:
		return
	else:
		r = requests.get(url)
		if r.status_code == RESPONSE_OK:
			# if status is ok, then save the image
			filename = subreddit + "/" + filename
			print "Saving as %s" %(filename)
			try:
				with open(filename, 'wb') as fd:
					for chunk in r.iter_content(chunk_size):
						fd.write(chunk)
			except:
				pass

def get_urls(sr_to_process):
	# Read the url links
	fp_input = open(INPUT_FILE, 'r')
	for line in fp_input:
		sr_to_process = sr_to_process - 1
		subreddits.append(line.rstrip('\n'))
		if sr_to_process <= 0:
				break
	fp_input.close()


def long_filename(subreddit, url):
	filename = 'reddit_%s_%s' %(subreddit,url.split('/')[-1])
	return filename
	
if TESTING:
	subreddits.append("pics")
else:
	get_urls(NO_OF_SUBREDDITS)

def make_saved_list(sr_dir):
	all_files = [ f for f in listdir(sr_dir) if isfile(join(sr_dir,f)) ]
	for each_file in all_files:
		# remove all extensions
		each_file = each_file.split('.')[0]
		# remove all appendages
		each_file = each_file.split('_')[-1]
		saved_files.append(each_file)

for each_subreddit in subreddits:
	# for each subreddit, create a directory
	# First make the directory, since make_saved_list uses it
	if not os.path.exists(each_subreddit):
		os.makedirs(each_subreddit)
	make_saved_list(each_subreddit)

reddit_agent = praw.Reddit(user_agent='aggregator')
for each_subreddit in subreddits:
	print each_subreddit
	submissions = reddit_agent.get_subreddit(each_subreddit).get_hot(limit=number_of_posts)
	for submission in submissions:
		if submission.score < MIN_KARMA:	
			continue
		# Check if already downloaded. If so, skip
		last_word = submission.url.split('/')[-1]
		last_word = last_word.split('.')[0]
		if last_word in saved_files:
			continue
		# Album submissions
		if 'imgur.com/a/' in submission.url:
			htmlSource = requests.get(submission.url).text
			images = re.findall('<img src="(\/\/i\.imgur\.com\/([a-zA-Z0-9]+\.(jpg|jpeg|png|gif)))(\?[0-9]+)?"', htmlSource)
			for image in images:
				url = "http:" + image[0]
				# Check if already downloaded. If so, skip
				# need to do it again for Albums since individual photos have different names
				last_word = url.split('/')[-1]
				last_word = last_word.split('.')[0]
				if last_word in saved_files:
					continue
				else:
					saveImage(url, each_subreddit, long_filename(each_subreddit, url))
			del images[:]
		# Not album
		elif 'imgur.com/' in submission.url:
         # This is an Imgur page with a single image.
			url = vars(submission)['url']
 			last_word = url.split('/')[-1]
 			ext = last_word.split('.')[-1]
	 		website = url.split('/')[2]
	 		if not ext or ext == last_word:
 			 	url = url + ".jpg"
	 		r = requests.get(url)
 			if r.status_code == RESPONSE_OK:
	 			filename = long_filename(each_subreddit, url)
				saveImage(url, each_subreddit, filename)
		# Do gfycat
		elif 'gfycat.com' in submission.url:
			# query using this format http://gfycat.com/cajax/get/ScaryGrizzledComet
			name = submission.url.split('/')[-1]
			gyfcat_url_query = "http://gfycat.com/cajax/get/" + name
			r = requests.get(gyfcat_url_query)
			try:
				if r.status_code == RESPONSE_OK:
					r_json = r.json()
					url = r_json['gfyItem']['mp4Url']
					filename = long_filename(each_subreddit, url)
					saveImage(url, each_subreddit, filename)
			except:
				pass
		# Tumbler and others. See if extension is a gif, if so, try and save
		elif 'gif' in submission.url:
			name = submission.url.split('/')[-1]
			ext = name.split('.')[-1]
			if ext == "gif":
				try:
					r = requests.get(submission.url)
					if r.status_code == RESPONSE_OK:
		 				saveImage(url, each_subreddit, filename)		
				except:
					continue
		else: 
			# what are not covered
			print submission.url
print "Done!"
