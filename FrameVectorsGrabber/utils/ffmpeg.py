__author__ = 'luca'

from PyQt4.QtCore import QProcess

class FFMpegWrapper(object):

    @classmethod
    def generate_frames(cls, me, input_file_path, output_dir, finish_callbak, frame_extension = "png"):

        frames_output_path = output_dir+'/video_name/Frame_%07d.'+frame_extension

        def _check_callback_status(code, code2):
            print "Processo FFMpeg finito, chiamo la callback"
            finish_callbak(code==0, frames_output_path)

        process = QProcess(me)
        process.finished.connect(_check_callback_status)

        process.start("/usr/local/bin/ffmpeg", ['-i', input_file_path,'-t', '5', '-ss', '00:01:30', frames_output_path])
        #process.startDetached("/usr/local/bin/ffmpeg", ['-i', input_file_path,'-t', '2', output_dir+'/video_name/Frame_%07d.'+frame_extension])
        #process.startDetached("/usr/local/bin/ffmpeg", ['-h'])

       # process = subprocess.Popen(['/usr/local/bin/ffmpeg',  '-i', input_file_path,'-t 5', '-ss 00:01:30', output_dir+'/video_name/Frame_%07d.'+frame_extension], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #process = subprocess.Popen(['/usr/local/bin/ffmpeg', '-h'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #process = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #stdout, stderr = process.communicate()
        #print stdout
        #matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

        #print matches['hours']
        #print matches['minutes']
        #print matches['seconds']

       # finish_callbak()


