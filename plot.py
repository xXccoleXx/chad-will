import csv
import matplotlib.pyplot as plt
import numpy as np

frame = []
left = []
right = []

with open('processed\\recording.csv', mode ='r')as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        frame.append(row['frame'])
        left.append(row[' gaze_0_x'])
        right.append(row[' gaze_1_x'])

left = left[1:10]
frame = frame[1:10]

frame = np.array(frame)
left = np.array(left)

plt.plot(frame, left, 'o', color='black')
plt.show()
