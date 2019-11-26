import glob
import os
import sys
import urllib

def downloadAllTurns(gameID, maxTurns,  directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    for i in range(maxTurns + 1):
        urlLink = "https://webdiplomacy.net/map.php?gameID=" + str(gameID) + "&turn=" + str(i)
        imageName = directory + "/turn_" + str(i) + ".png"

        if largeMode:
            urlLink += "&mapType=large"
    
        urllib.urlretrieve(urlLink, imageName)
        
        print("Downloaded image for turn {}".format(i))
    
    print "Download complete"

def generateGIF(gameID, directory):
    print "Generating GIF..."

    # Get all the png files in the directory
    fileList = glob.glob(directory + '/*.png')

    # Sort images by turn number
    list.sort(fileList, key=lambda x: int(x.split('_')[-1].split('.png')[0]))
    
    with open('image_list.txt', 'w') as file:
        for item in fileList:
            file.write("%s\n" % item)

    gifName = "game" + directory
    os.system('magick -delay 200 @image_list.txt {}.gif'.format(gifName))
    print("Written output to {}.gif".format(gifName))

if len(sys.argv) != 4:
    print "Usage: python create_reply.py [gameID] [maxTurns] [largeMode]"
    sys.exit()

gameID = int(sys.argv[1])
maxTurns = int(sys.argv[2])
largeMode = sys.argv[3].lower() == "true"

if largeMode:
    directory = str(gameID) + "_large"
else:
    directory = str(gameID)

print("Getting image data for game {}".format(gameID))
print("Max turns is {}".format(maxTurns))
print("Large mode is {}".format(largeMode))

downloadAllTurns(gameID, maxTurns, directory)
generateGIF(gameID, directory)