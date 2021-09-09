import pytube
import os
import time
from pyyoutube import Api

class Downloader:
    def __init__(self, aSearchQuery):
        self.query = aSearchQuery
        self.folder = os.getcwd() + "\\icons\\temp"
        self.api = Api(api_key="AIzaSyD-H811LKwCG-4Mp71IOKa2MHK82Ss9uzs")


    def searchUrl(self):
        request = self.api.search_by_keywords(q=self.query,
                                              search_type="video",
                                              count=1,
                                              limit=1)
        video_url_id = request.items[0].id.videoId
        return "https://youtube.com/watch?v=" + video_url_id


    def download(self):
        try:
            start = time.time()

            url = self.searchUrl()
            youtube_video = pytube.YouTube(url).streams.first()
            end = time.time()
            print("search: " + str(end-start) + "s")

            start = time.time()
            if not self.fileExists(youtube_video.default_filename):
                youtube_video.download(self.folder)
            end = time.time()

            print("download: " + str(end-start) + "s")
        except Exception as e:
            print(e)


    def fileExists(self, aName):
        files = os.listdir(self.folder)
        for file in files:
            if file == aName:
                return True
        return False

    def getFile(self):
        files = os.listdir(self.folder)
        for file in files:
            if file.endswith(".mp4"):
                if self.hacky(file):
                    return self.folder + "\\" + file

    def hacky(self, name):
        name1 = name.lower()
        q1 = self.query.lower()
        if name1[:2] == q1[:2]:
            return True


    def deleteFile(self):
        try:
            os.remove(self.getFile())
        except Exception as e:
            print(e)