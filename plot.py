import csv
import matplotlib.pyplot as plt
import statistics

frame = []
left = []
right = []

with open('processed\\w.csv', mode ='r')as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        frame.append(row['frame'])
        left.append(float(row[' gaze_0_x']))
        right.append(float(row[' gaze_1_x']))


left = [item * 100 for item in left]
mu = statistics.mean(left)
print(mu)
MSE = 0
for num in left:
    MSE += (num - mu)**2
print(MSE)

plt.plot(frame, left, 'o', color='black')
plt.show()

