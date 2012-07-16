__author__ = 'luca'

import os
import shutil
from images.image_comparator import ImageComparator

class VideoInterpolator(object):
    def __init__(self, video):
        self._oldvideo = video

    def interpolate(self, discarded_frames, searcher, block_size, MAD_threshold):

        new_video_path = "/tmp/%s.interpolated/" % self._oldvideo.videoname()

        if os.path.exists(new_video_path):
            shutil.rmtree(new_video_path)

        os.makedirs(new_video_path)
        i=0

        while i < self._oldvideo.frames_count():
            if not i in discarded_frames:
                #The frame must me copied in the folder
                frame = self._oldvideo.frames[i]

                shutil.copyfile(frame.path(), "%s/Frame%07d.png" %(new_video_path, i))
                i+=1

            else:
                #the frame must be interpolated

                #check which other adiacent frames must me interpolated
                new_frames = [i]

                for j in range(i+1, self._oldvideo.frames_count()):
                    if j in discarded_frames:
                        new_frames.append(j)
                    else:
                        #The adiacent frame is an I frame, so stop searching
                        i = j
                        break

                #interpolate the frames
                print "I have to interpolate these frames: "+ str(new_frames)

                left_frame_index = new_frames[0] - 1
                right_frame_index = new_frames[-1] + 1

                print "Left I frame: %s" %self._oldvideo.frames[left_frame_index].path()
                print "Right I frame: %s" %self._oldvideo.frames[right_frame_index].path()

                frame_1 = self._oldvideo.frames[left_frame_index]  #the frame on the LEFT of the first frame to be interpolated
                frame_2 = self._oldvideo.frames[right_frame_index] #the frame on the RIGHT of the last frame to be interpolated

                comp = ImageComparator(frame_1.grayscaled_image())
                vectors = comp.get_motion_vectors(frame_2.grayscaled_image(), searcher, MAD_threshold)

                print vectors
                subvectors = VideoInterpolator.sub_motion_vectors(vectors, len(new_frames))
                print subvectors


                #TODO: check len(subvectors) MUST be equal to len(new_frames)
                for k in range(len(new_frames)):
                    frame_num = new_frames[k]
                    frame_path = "%s/Frame%07d.png" % (new_video_path, frame_num)
                    print "Devo interpolare %d" % frame_num

                    image1 = frame_1.image()

                    image_new = image1.copy()
                    #image_new.paste((0,0,0))

                    #First copy the background from the frame_2 to the image_new
                    #image2 = frame_2.image()
                    #for v in subvectors[k]:
                    #    background_block_image = image2.crop( (v["x"], v["y"], v["x"]+block_size, v["y"]+block_size) )
                    #    image_new.paste(background_block_image, (v["x"], v["y"], v["x"]+block_size, v["y"]+block_size) )

                    #Then copy the moved blocks
                    print "------------"
                    for v in subvectors[k]:
                        #print "Copying the block (%d, %d) from frame: %d to (%d, %d) to the new frame %d" %(v["x"], v["y"], left_frame_index, v["to_x"], v["to_y"], frame_num)
                        moved_block_image = image1.crop( (v["x"], v["y"], v["x"]+block_size, v["y"]+block_size) )
                        image_new.paste(moved_block_image, (v["to_x"], v["to_y"], v["to_x"]+block_size, v["to_y"]+block_size) )
                        #image_new.paste((255, 0, 0), (v["to_x"], v["to_y"], v["to_x"]+block_size, v["to_y"]+block_size) )

                    image_new.save(frame_path)
                    #print "Saved new frame: "+ frame_path

                #print "---"
        return new_video_path

    @classmethod
    def sub_motion_vectors(cls, vectors, num):
        subvectors = []

        for i in range(num):
            subvectors.append([])


        print "Creating subvectors"
        for v in vectors:
            for i in xrange(num):
                #if something is changed
                new_x = int( v['x'] + (v['to_x'] - v['x']) * (i+1)/(num+1) )
                new_y = int( v['y'] + (v['to_y'] - v['y']) * (i+1)/(num+1) )

                #print "I: %d new_x: %d new_y: %d" %(i, new_x, new_y)

                new_vector = { 'x': v['x'], 'y': v['y'], 'to_x' : new_x, 'to_y': new_y}
                subvectors[i].append( new_vector )

            print "Done, subvectors created."
        return subvectors

