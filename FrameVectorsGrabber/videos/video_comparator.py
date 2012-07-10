__author__ = 'luca'

from videos.video import Video
from images.image_comparator import ImageComparator


class VideoComparator(object):

    def __init__(self, video, searcher):
        self._video = video
        self._searcher = searcher

    def compared_frames_statuses(self, motion_threshold, MAD_threshold):

        holden_frames = [0] #start with the first frame
        discarded_frames = []

        i = 0
        j = 1

        while i < self._video.frames_count()-2 and j < self._video.frames_count()-1:

            #controllo il frame successivo per vedere se sono sotto la soglia
                #si lo sono, posso aggiungere il frame alla lista di quelli da non considerare
                #no non lo sono, il frame e necessario

            if i is j:
                print "CYCLE COMPARISON ERROR"

            print "\nComparing frame #%d with frame #%d" %(i, j)

            frame_1 = self._video.frames[i].grayscaled_image()
            frame_2 = self._video.frames[j].grayscaled_image()

            comp = ImageComparator(frame_1)
            vectors = comp.get_motion_vectors(frame_2, self._searcher, MAD_threshold)

            longest_vector, max_distance = ImageComparator.longest_motion_vector(vectors)

            print "Max distance found: %f" %max_distance
            print "Longest vector is: "+ str(longest_vector)

            if max_distance < motion_threshold:
                print "Frame #%d discared.. :-) " %j
                discarded_frames.append(j) #the compared frame contains only short motion vectors, so I can discard that frame
                j += 1 #the I frame is same, the frame to be compared is the j+1 so the search continue
            else:
                print "Frame #%d holden... :-(" %j
                holden_frames.append(j) #the compared frame contains a very long motion vector, so the frame will be rendered as frame I
                i = j
                j = i+1

        holden_frames.append(self._video.frames_count()-1) #keep the last frame

        return holden_frames, discarded_frames
