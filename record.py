# Python program to save a 
# video using OpenCV
   
if __name__ == '__main__': 
    import cv2
    import time  

    # Create an object to read 
    # from camera
    video = cv2.VideoCapture(0)
    clock = time.time()
    
    # We need to set resolutions.
    # so, convert them from float to integer.
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    size = (frame_width, frame_height)
    
    # Below VideoWriter object will create
    # a frame of above defined The output 
    # is stored in 'filename.avi' file.
    result = cv2.VideoWriter('output\filename.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, size)
        
    while(True):
        ret, frame = video.read()
        print(time.time() - clock)
        if ret == True: 
            # Write the frame into the
            # file 'filename.avi'
            result.write(frame)
            
    
            # Press S on keyboard 
            # to stop the process
            if time.time() - clock > 10 or 0xFF == ord('q'):
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