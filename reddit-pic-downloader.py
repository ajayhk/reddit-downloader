import requests
import json
from pprint import pprint
import datetime
import os
 
##Set constants for script
 
DL_LIMIT = 5
 
##Download and load the JSON information for the Gallery
 
#get json object from imgur gallery. can be appended with /month or /week for
# more recent entries
r = requests.get(r'http://imgur.com/r/pics/top.json')
#creates a python dict from the JSON object
j = json.loads(r.text)
 
#prints the dict, if necessary. Used for debug mainly
pprint(j)
 
#get the list of images from j['gallery']
#image_list = j['gallery']
 
#print the number of images found
#print len(image_list), 'images found in the gallery'
 
#debugging, examine the first image in the gallery, confirm no errors
#pprint(image_list[0])
 
## Create a dynamically named folder
 
#get the time object for today
folder = datetime.datetime.today()
#turn it into a printable string
string_folder = str(folder)
#replace some illegal chars
legal_folder = string_folder.replace(':', '.')
#create the folder using the name legal_folder
os.mkdir(str(legal_folder))
 
## Extract image info from the gallery
 
#list of pairs containing the image name and file extension
image_pairs = []
#extract image and file extension from dict
for image in image_list:
    #get the raw image name
    img_name = image['hash']
    #get the image extension(jpg, gif etc)
    img_ext = image['ext']
    #append pair to list
    image_pairs.append((img_name, img_ext))
 
## Download images from imgur.com
 
#current image number, for looping limits
current = 0
#run download loop, until DL_LIMIT is reached
for name, ext in image_pairs:
    #so long as we haven't hit the download limit:
    if current < DL_LIMIT:
        #this is the image URL location
        url = r'http://imgur.com/{name}{ext}'.format(name=name, ext=ext)
        #print the image we are currently downloading
        print 'Current image being downloaded:', url
 
        #download the image data
        response = requests.get(url)
        #set the file location
        path = r'./{fldr}/{name}{ext}'.format(fldr=legal_folder,
                                              name=name,
                                              ext=ext)
        #open the file object in write binary mode
        fp = open(path, 'wb')
        #perform the write operation
        fp.write(response.content)
        #close the file
        fp.close()
        #advance the image count
        current += 1
 
#print off a completion string
print 'Finished downloading {cnt} images to {fldr}!'.format(cnt=current,
                                                            fldr=legal_folder)
