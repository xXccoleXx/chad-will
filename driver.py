"""
Main driver to run dot simulation and record video at
the same time using multithreading.

@author Chase Coleman
@version 11/22/22
"""
import cv2
import os
import pygame
import time
import threading

name = 'w'

def dot():
    pygame.init()
    screen = pygame.display.set_mode((1700, 1000))
    dot = pygame.transform.scale(pygame.image.load("dot.jpeg"), (20, 20))

    def  move(clock, positions):
        for position in positions:
            clock.tick(60)
            screen.fill((255, 255, 255))
            screen.blit(dot, (position, 50)) 
            pygame.display.update()

    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))
    screen.blit(dot, (840, 50))
    pygame.display.update()

    pygame.time.delay(2000)
    move(clock, [*range(840, 1, -7)])  
    pygame.time.delay(4000)  
    move(clock, [*range(1, 1680, 7)])
    pygame.time.delay(4000)
    move(clock, [*range(1680, 1, -7)])
    pygame.time.delay(4000)
    move(clock, [*range(1, 1680, 7)])
    pygame.time.delay(4000)
    move(clock, [*range(1680, 840, -7)])
    pygame.time.delay(2000)

    pygame.quit()    


def record():
    # Create an object to read 
    # from camera
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    clock = time.time()
    
    # We need to set resolutions.
    # so, convert them from float to integer.
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    size = (frame_width, frame_height)
    
    # Below VideoWriter object will create
    # a frame of above defined The output 
    # is stored in 'filename.avi' file.
    result = cv2.VideoWriter('output\\' + name + '.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, size)
        
    while(True):
        ret, frame = video.read()
        print(time.time() - clock)
        if ret == True: 
            # Write the frame into the
            # file 'filename.avi'
            result.write(frame)
            
    
            # Press S on keyboard 
            # to stop the process
            if time.time() - clock > 35 or 0xFF == ord('q'):
                break
        # Break the loop
        else:
            break
    
    # When everything done, release 
    # the video capture and video 
    # write objects
    video.release()
    result.release()  
    print("The video was successfully saved")





t1 = threading.Thread(target=dot, args=())
t2 = threading.Thread(target=record, args=())
 
# starting thread 1
t1.start()
# starting thread 2
t2.start()
 
# wait until thread 1 is completely executed
t1.join()
# wait until thread 2 is completely executed
t2.join()
 
# both threads completely executed
print("Done!")





# sending to openface to create analytics

inputVideo = "C:\\Users\\chase\\OneDrive\\Desktop\\HGN\\output\\" + name + ".avi"
featureExtractionApp = "C:\\Users\\chase\\WEBSITE\\OpenFace\\OpenFace_2.2.0_win_x64\\FeatureExtraction.exe"
command = featureExtractionApp + " -f " + inputVideo + " -gaze"
os.system(command)

