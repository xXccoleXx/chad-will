import csv
import matplotlib.pyplot as plt
import statistics
# take in data from all 5 simulations
# split data into each section
# make linear regression model for each 
# output the mse

# masterdata[data[left[stable[la[], lc[], e[], g[]], moving[lb[], ld[], lf[]]], right[stable[], moving[]]], 2..., k]
filenames = ["1", "2", "3", "4", "5"]
masterdata = []
x = list(range(1:2))

f = {list(range(115:216)), list(range(215:316)), list(range(340:441)), list(range(470:561)), list(range(580:681)), list(range(705:791)), list(range(810:911))}
frames = [list(range(115:216)), [*range(215:316)], [*range(340:441)], [*range(470:561)], [*range(580:681)], [*range(705:791)], [*range(810:911)]]
for name in filenames:
    left = []
    right = []
    path = 'processed\\' + name + '.csv'
    with open(path, mode ='r')as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            left.append(float(row[' gaze_0_x']))
            right.append(float(row[' gaze_1_x']))
    data = [left, right]
    count = 0
    for eye in data:
        stable = []
        stable.append(eye[115:215])
        stable.append(eye[340:440])
        stable.append(eye[580:680])
        stable.append(eye[810:910])
        moving = []
        moving.append(eye[215:315])
        moving.append(eye[470:560])
        moving.append(eye[705:790])
        eye = [stable, moving]
        data[count] = [stable, moving]
        count = count + 1
    masterdata.append(data)


def getLine(section):
    mu = list(range(len(section)))
    for i in range(len(mu)):
        mu[i] = statistics.mean(section)
    return mu




# all,file,eye,test,order,frame
section = masterdata[2][0][0][1]
mu = getLine(section)
x = [*range(1, len(section) + 1, 1)]
plt.plot(x, section, 'o', color='red')
plt.plot(x, mu, "-", color='blue')
plt.show()

print(frames)