__author__ = 'luca'

from PyQt4.QtCore import QProcess, QObject
from PyQt4.QtGui import QApplication
import os
import time
from utils.string import str_insert

class FFMpegWrapper(object):

    @classmethod
    def generate_frames(cls, input_file_path, output_dir, finish_callbak, frame_extension = "png"):
        file_name = input_file_path[input_file_path.rindex("/"):].replace(" ", "_")

        frames_output_path = output_dir+'/'+file_name

        if os.path.exists(frames_output_path):
            print "La cartella dei frame esiste gia, non avvio ffmpeg"
            finish_callbak(True, frames_output_path)

        else:
            #Create the folder
            os.makedirs(frames_output_path)


            #Execute FFMPEG
            def _check_callback_status(code, code2):
                print "Processo FFMpeg finito, chiamo la callback"
                finish_callbak(code==0, frames_output_path)

            process = QProcess(QApplication.instance())
            process.finished.connect(_check_callback_status)

            #process.start("/usr/local/bin/ffmpeg", ['-i', input_file_path,'-t', '5', frames_output_path+'/Frame_%07d.'+frame_extension])
            #process.start("/usr/local/bin/ffmpeg", ['-i', input_file_path, '-r', '30', '-t', '3', '-s', '213x120',  '-ss', '00:01:30', frames_output_path+'/Frame_%07d.'+frame_extension])
            process.start("/usr/local/bin/ffmpeg", ['-i', input_file_path, '-r', '15', '-t', '5', '-ss', '00:00:50', frames_output_path+'/Frame_%07d.'+frame_extension])


    @classmethod
    def generate_video(cls, input_frames_folder, file_name, frames_pattern= "Frame_%07d.png", finish_callbak = None, bitrate=1800, fps = 30):

        input_frames_pattern = "%s/%s" % (input_frames_folder, frames_pattern)
        video_name = str_insert(file_name, "_%f" % time.time(), file_name.rfind("."))

        video_output_path = "/tmp/%s" %video_name

        #Execute FFMPEG
        def _check_callback_status(code, code2):
            print "Processo FFMpeg finito, chiamo la callback"
            if finish_callbak:
                finish_callbak(code==0, video_output_path)

        process = QProcess(QApplication.instance())
        process.finished.connect(_check_callback_status)

        process.start("/usr/local/bin/ffmpeg", ['-r', str(fps), '-b', str(bitrate), '-i', input_frames_pattern, video_output_path])

