__author__ = 'luca'

import os
from videos.frame import Frame
from utils.ffmpeg import FFMpegWrapper

class Video(object):

    def __init__(self, video_path=None, frames_path=None):
        if not video_path and not frames_path:
            raise Exception("Canno create the Video object: you must set either video path or frames_path")

        self.frames = []
        self.name = None
        self._filepath = video_path
        self._frames_path = frames_path

    def videoname(self):
        if not self.name:
            self.name = self._filepath[self._filepath.rindex("/"):].replace(" ", "_").replace("/", "")

        return self.name

    def setVideoName(self, name):
        self.name = name

    def __video_loaded(self, success, frames_output_path):
        #Get the frames
        if success:
            print "I frame sono stati creati in %s." %frames_output_path
        else:
            print "Impossibile creare il video."

        for file_name in os.listdir(frames_output_path):
            if file_name.endswith(".png") or file_name.endswith(".jpg"):
                self.frames.append( Frame(frames_output_path+"/"+file_name) )

        if self._video_loaded_callback:
            self._video_loaded_callback(success)

    def load(self, video_loaded_callback=None):
        self._video_loaded_callback = video_loaded_callback

        if self._filepath:
            FFMpegWrapper.generate_frames(self._filepath, "/tmp", self.__video_loaded)
        elif self._frames_path:
            self.__video_loaded(True, self._frames_path)


    def frames_count(self):
        return len(self.frames)

    def width(self):
        return self.frames[0].width()

    def height(self):
        return self.frames[0].height()