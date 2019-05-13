Reddit Picture Downloader
========


This python script downloads pictures from posts in sub-reddits like /r/pics that include links from websites like Imgur, gfycat and others  
 
The project has three versions that have evolved over time  
reddit-downloader-praw.py is the latest and most maintained version and is based on the excellent [PRAW python library] (https://praw.readthedocs.io/en/latest/)  


How to run
--------

Create a text file named `all_links.txt` .  
The text file should contain subreddit names from which you want to download pics, one per line
For e.g.

> pics   
> aww   
> goldenretrievers   

  
   
Now run  
`python reddit-downloader-praw.py`  
   
The program creates subdirectories, one per subreddit and downloads pictures, gifs, etc into the directory   

   
You can set the following in the python file itself . 

1.  Minimum karma needed to include a post (default is 35)   
2.  Number of posts to check and download (default is 1000)   

   
Enjoy!!   
