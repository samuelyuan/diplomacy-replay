from multiprocessing.pool import ThreadPool
import argparse
import glob
import os
import sys
import time
import urllib

def downloadAllTurns(gameID, maxTurns, directory, largeMode):
    def downloadTurnImage(turnNum):
        # Get image url of each turn
        urlLink = "https://webdiplomacy.net/map.php?gameID={}&turn={}".format(str(gameID), str(turnNum))
        # If largeMode is specified, modify url to get image with increased resolution
        if largeMode:
            urlLink += "&mapType=large"        
        # Path of image on disk
        savedImageFilename = "{}/turn_{}.png".format(directory, str(turnNum))
        # Connect to url link and download image
        urllib.urlretrieve(urlLink, savedImageFilename)
        
        print("Downloaded image for turn {}, written to {}".format(turnNum, savedImageFilename))

    # Create new folder to store all images for this game
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    start = time.time()
        
    numThreads = 4
    pool = ThreadPool(numThreads)
    pool.map(downloadTurnImage, range(maxTurns + 1))
    
    end = time.time()
    
    print "Download complete. {} seconds elapsed.".format(end - start)

def generateGIF(gameID, directory):
    print "Generating GIF..."

    # Get all the png files in the new directory
    fileList = glob.glob(directory + '/*.png')

    # Sort images by turn number
    list.sort(fileList, key=lambda x: int(x.split('_')[-1].split('.png')[0]))
    
    # Write all the image filenames to a new text file
    with open('image_list.txt', 'w') as file:
        for item in fileList:
            file.write("%s\n" % item)

    # Run ImageMagick to generate gif
    gifName = "{}/game{}".format(directory, gameID)
    os.system('magick -delay 200 @image_list.txt {}.gif'.format(gifName))
    print("Written output to {}.gif".format(gifName))

def main():      
    parser = argparse.ArgumentParser()
    parser.add_argument('-game', '--gameId', type=int, required=True)
    parser.add_argument('-max', '--maxTurns', type=int, required=True)
    parser.add_argument('--largeMode', action='store_true')
    args = parser.parse_args()
    
    gameID = int(args.gameId)
    maxTurns = int(args.maxTurns)
    largeMode = args.largeMode
    
    if not os.path.exists("output"):
        os.mkdir("output")
    
    if largeMode:
        directory = "./output/{}_large".format(gameID)
    else:
        directory = "./output/{}".format(gameID)
    
    print("Getting image data for game {}".format(gameID))
    print("Max turns is {}".format(maxTurns))
    print("Large mode is {}".format(largeMode))
    print("Output directory: {}".format(directory))
    
    downloadAllTurns(gameID, maxTurns, directory, largeMode)
    generateGIF(gameID, directory)
    
if __name__ == "__main__":
    main()    