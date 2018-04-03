from bs4 import BeautifulSoup
import requests
import re

def getVideoId(itemName):

    query = itemName
    url = "https://www.youtube.com/results?search_query=" + query + " movie trailer"

    resp = requests.get(url)
    html_data = resp.text
    soup = BeautifulSoup(html_data, 'html.parser')
    numScrape = 1
    tags = soup.find_all("a", attrs={'class':'yt-uix-tile-link'}, limit=numScrape)
    # print(tags)
    # print("--------------------")

    # for tag in tags:
    #     print('TAG:', tag)
    #     print('URL:', tag.get('href', None))

    videoURL = tags[0].get('href', None)
    # print(videoURL)
    # videoURL="/watch?v=yHfLyMAHrQE"

    # print(videoURL)
    # print(type(videoURL ))
    videoIds = re.findall('v\=(.+)', videoURL)
    # if not videoIds:
    #     videoId = "iG_KZxLHozI" # welcome movie company intros
    # else:
    #     videoId = videoIds[0]

    if videoIds:
        videoId = videoIds[0]
    else:
        videoIds = re.findall('video_id=(.+)&client', videoURL)
        if videoIds:
            videoId = videoIds[0]
        else:
            videoId = "iG_KZxLHozI" # welcome movie company intros




    return videoId

def getVideoURL(videoId):
    videoURL = "https://www.youtube.com/embed/" + videoId + "?rel=0&amp;showinfo=0&amp;"
    return videoURL


if __name__=="__main__":
    videoId = getVideoId("coco")
    print(videoId)

