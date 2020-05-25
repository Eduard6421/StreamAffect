import os

emotions = {
    "0": "anger",
    "1": "fear",
    "2": "happy",
    "3": "horny",
    "4": "sad"
}


root_path = "./dataset/"
count = [0, 0, 0, 0, 0]

for i, key in enumerate(emotions):
    emotion_path = root_path + emotions[key] + "/"
    image_names = os.listdir(emotion_path)
    for image_name in image_names:
        count[i] += 1

print(count)

import matplotlib.pyplot as plt

ax = plt.subplot(111)
ax.bar([1, 2, 3, 4, 5], count, width=0.5, color='b', align='center')
plt.xticks([1, 2, 3, 4 , 5], ["Anger", "Fear", "Happiness", "Excitement", "Sadness"])
plt.ylabel('Number of samples')
plt.show()