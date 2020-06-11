#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import cv2 as cv
import glob
import re


# In[ ]:


folder = "anger"


# In[ ]:


def read_images():
    names = glob.glob("*.jpg")
    names.extend(glob.glob("*.png"))
    names.sort(key=lambda name: [int(s) for s in re.findall(r'\d+', name)][0])
    return names


# In[ ]:


def get_nth_image(images, idx):
    
    dim = (416, 416)
    
    new_img = cv.imread(images[idx], cv.IMREAD_COLOR)
    new_img = cv.resize(new_img, dim)
    
    return new_img


# In[ ]:


def save_image(image, name):
    base_folder = (folder + "/")
    cv.imwrite((base_folder + name + ".jpg"), image)


# In[ ]:


img_names = read_images()

for i in range(len(img_names)):
    
    img = get_nth_image(img_names, i)
    save_image(img, (folder + str(i + 1)))

