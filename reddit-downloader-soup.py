from pprint import pprint
import requests
import json
import re, praw, requests, os, glob, sys
from bs4 import BeautifulSoup

imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')


def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print('Downloading %s...' % (localFileName))
        with open(localFileName, 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)

targetSubreddit = "pics"

r = praw.Reddit(user_agent='example')
number_of_posts = 1000
submissions = r.get_subreddit(targetSubreddit).get_hot(limit=number_of_posts)
for submission in submissions:
    # Check for all the cases where we will skip a submission:
    if "imgur.com/" not in submission.url:
        continue # skip non-imgur submissions

    if 'http://imgur.com/a/' in submission.url:
        # This is an album submission.
        albumId = submission.url[len('http://imgur.com/a/'):]
        htmlSource = requests.get(submission.url).text

        soup = BeautifulSoup(htmlSource)
        matches = soup.select('.album-view-image-link a')
        for match in matches:
            imageUrl = match['href']
            if '?' in imageUrl:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
            else:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:]
            localFileName = 'reddit_%s_%s_album_%s_imgur_%s' % (targetSubreddit, submission.id, albumId, imageFile)
            localFileName = localFileName.replace('/', '.')
            localFileName = localFileName.replace('\\', '.')
            downloadImage('http:' + match['href'], localFileName)

    elif 'http://i.imgur.com/' in submission.url:
        # The URL is a direct link to the image.
        mo = imgurUrlPattern.search(submission.url) # using regex here instead of BeautifulSoup because we are pasing a url, not html

        imgurFilename = mo.group(2)
        if '?' in imgurFilename:
            # The regex doesn't catch a "?" at the end of the filename, so we remove it here.
            imgurFilename = imgurFilename[:imgurFilename.find('?')]

        localFileName = 'reddit_%s_%s_album_None_imgur_%s' % (targetSubreddit, submission.id, imgurFilename)
        downloadImage(submission.url, localFileName)

    elif 'http://imgur.com/' in submission.url:
        # This is an Imgur page with a single image.

		url = vars(submission)['url']
		last_word = url.split('/')[-1]
		ext = last_word.split('.')[-1]
		website = url.split('/')[2]
		if not ext:
			url = url + ".jpg"
		#download the image data
		response = requests.get(url)
		name = url.split('/')[-1]
		imageFile = url.split('/')[-1]
		localFileName = 'reddit_%s_%s_album_None_imgur_%s' % (targetSubreddit, submission.id, imageFile)
		downloadImage(url, localFileName)
print "Done"
